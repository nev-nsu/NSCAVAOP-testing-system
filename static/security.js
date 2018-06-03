function saveSidToCookie(sid)
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
    var sid = getCookie('sid');
    if (!sid) {
        document.location.href = "/signin.html";
        return;
    }
    var request = JSON.stringify(
        {
            type: "check_sid",
            sid:sid
        } );

    var xhrsec = new XMLHttpRequest();
    xhrsec.open('POST', '/api/v1/getinfo', true);
    xhrsec.setRequestHeader('Content-Type', 'application/json');

    xhrsec.onreadystatechange = function() {
    	if (this.readyState != 4)
		return;

        if (this.status != 200)
        {
            document.location.href = "/signin.html";
            return;
        }
        else
        {
            var obj = JSON.parse(this.responseText);
            if (obj.status !== 'success' || obj.result !== true){
                document.location.href = "/signin.html";
            }
            return;
        }
    };

    xhrsec.send(request);
}
