function saveSidToCookie(token)
{
	document.cookie = "sid=" + encodeURIComponent(sid)
}

function deleteSidFromCookie()
{
	document.cookie = "sid=";
}

// возвращает cookie с именем name, если есть, если нет, то undefined
function getCookie(name) {
  var matches = document.cookie.match(new RegExp(
    "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
  ));
  return matches ? decodeURIComponent(matches[1]) : undefined;
}

function securityCheck() {
    sid = getCookie('sid');
    if (!sid) {
        window.location="signin.html";
        return;
    }
    
    var request = JSON.stringify(
        {
            type: "check_sid",
            sid:sid
        } );

    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/api/v1/getinfo', true);
    xhr.setRequestHeader('Content-Type', 'application/json');

    xhr.onreadystatechange = function() {
    	if (this.readyState != 4)
		return;

        if (this.status != 200)
        {
            window.location="signin.html";
            return;
        }
        else 
        {
            var obj = JSON.parse(this.responseText);
            if (obj.status !== 'success' || obj.result !== true)
                window.location="signin.html";
            return;
        }
    };

    xhr.send(update_request);
}

