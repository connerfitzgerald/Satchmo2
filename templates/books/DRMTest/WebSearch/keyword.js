function URLDecode(enc)
{
   // Replace + with ' '
   // Replace %xx with equivalent character
   // Put [ERROR] in output if %xx is invalid.
   var HEXCHARS = "0123456789ABCDEFabcdef"; 
   var encoded = enc;
   var plaintext = "";
   var i = 0;
   while (i < encoded.length) {
       var ch = encoded.charAt(i);
	   if (ch == "+") {
	       plaintext += " ";
		   i++;
	   } else if (ch == "%") {
			if (i < (encoded.length-2) 
					&& HEXCHARS.indexOf(encoded.charAt(i+1)) != -1 
					&& HEXCHARS.indexOf(encoded.charAt(i+2)) != -1 ) {
				plaintext += unescape( encoded.substr(i,3) );
				i += 3;
			} else {
				alert( 'Bad escape combination near ...' + encoded.substr(i) );
				plaintext += "%[ERROR]";
				i++;
			}
		} else {
		   plaintext += ch;
		   i++;
		}
	} // while
   return plaintext;
};

function gup(name){  
	name = name.replace(/[\[]/,"\\\[").replace(/[\]]/,"\\\]");  
	var regexS = "[\\?&]"+name+"=([^&#]*)";  
	var regex = new RegExp( regexS );  
	var results = regex.exec(document.referrer);  
	if( results == null )    
		return "";  
	else    
		return results[1];
}

function getKeyWordGoogle()
{
	var keyword = gup('q')
	var decodeKey = URLDecode(keyword)
	
	return decodeKey;
}

function getKeyWordYahoo()
{
	var keyword = gup('p')
	var decodeKey = URLDecode(keyword)
	
	return decodeKey;
}


function getKeyWord()
{

	var searchKeyGoogle = getKeyWordGoogle();
	
	if(searchKeyGoogle == "")
	{
		var searchKeyYahoo = getKeyWordYahoo();
		return searchKeyYahoo.replace(/site:[a-zA-Z0-9_\.]*/i, "").replace(/\"/g, "");
		
	}
	else
	{
		return searchKeyGoogle.replace(/site:[a-zA-Z0-9_\.]*/i, "").replace(/\"/g, "");
	}

}

