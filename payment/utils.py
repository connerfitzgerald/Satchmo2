from decimal import Decimal
from livesettings import config_get
from livesettings import config_get_group
from payment import active_gateways
from satchmo_store.shop.models import Order, OrderItem, OrderItemDetail
from satchmo_store.shop.signals import satchmo_post_copy_item_to_order
from shipping.utils import update_shipping
import logging

log = logging.getLogger('payment.utils')

def capture_authorizations(order):
    """Capture all outstanding authorizations on this order"""
    if order.authorized_remaining > Decimal('0'):
        for authz in order.authorizations.filter(complete=False):
            processor = get_processor_by_key('PAYMENT_%s' % authz.payment)
            processor.capture_authorized_payments(order)

def get_or_create_order(request, working_cart, contact, data):
    """Get the existing order from the session, else create using
    the working_cart, contact and data"""
    shipping = data.get('shipping', None)
    discount = data.get('discount', None)
    notes = data.get('notes', None)
    try:
        order = Order.objects.from_request(request)
        if order.status != '':
            # This order is being processed. We should not touch it!
            order = None
    except Order.DoesNotExist:
        order = None

    update = bool(order)
    if order:
        # make sure to copy/update addresses - they may have changed
        order.copy_addresses()
        order.save()
    else:
        order = Order(contact=contact)

    pay_ship_save(order, working_cart, contact,
        shipping=shipping, discount=discount, notes=notes, update=update)
    request.session['orderID'] = order.id
    
    return order

def get_gateway_by_settings(gateway_settings, settings={}):
    log.debug('getting gateway by settings: %s', gateway_settings.key)
    processor_module = gateway_settings.MODULE.load_module('processor')
    gateway_settings = get_gateway_settings(gateway_settings, settings=settings)
    return processor_module.PaymentProcessor(settings=gateway_settings)

def get_processor_by_key(key):
    """
    Returns an instance of a payment processor, referred to by *key*.

    :param key: A string of the form 'PAYMENT_<PROCESSOR_NAME>'.
    """
    payment_module = config_get_group(key)
    processor_module = payment_module.MODULE.load_module('processor')
    return processor_module.PaymentProcessor(payment_module)

def pay_ship_save(new_order, cart, contact, shipping, discount, notes, update=False):
    """
    Save the order details, first removing all items if this is an update.
    """
    if shipping:
        update_shipping(new_order, shipping, contact, cart)

    if not update:
        # Temp setting of the tax and total so we can save it
        new_order.total = Decimal('0.00')
        new_order.tax = Decimal('0.00')
        new_order.sub_total = cart.total
        new_order.method = 'Online'

    if discount:
        new_order.discount_code = discount
    else:
        new_order.discount_code = ""
    if notes:
        new_order.notes = notes
    update_orderitems(new_order, cart, update=update)


def update_orderitems(new_order, cart, update=False):
    """Update the order with all cart items, first removing all items if this
    is an update.
    """
    if update:
        new_order.remove_all_items()
    else:
        # have to save first, or else we can't add orderitems
        new_order.site = cart.site
        new_order.save()
    # Add all the items in the cart to the order
    for item in cart.cartitem_set.all():
        new_order_item = OrderItem(order=new_order,
            product=item.product,
            duration=item.duration)
            
#            unit_price=item.unit_price,
#            line_item_price=item.line_total)
        new_order_item.save()
        # Send a signal after copying items
        # External applications can copy their related objects using this
        satchmo_post_copy_item_to_order.send(
                cart,
                cartitem=item,
                order=new_order, orderitem=new_order_item
                )
    new_order.recalculate_total()