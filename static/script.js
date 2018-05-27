var send_button = document.getElementById('submit');
var code_field = document.getElementById('source_code');
var tests_description_field = document.getElementById('tests_description');
var verificator_field = document.getElementById('verification_script');
var file_button = document.getElementById('load_file');
var output_field = document.getElementById('output');
var optimization_lvl_selector = document.getElementById('optimization_level_selector');

function disablePage()
{
	send_button.disabled = true;
	code_field.disabled = true;
	tests_description_field.disabled = true;
	verificator_field.disabled = true;
	file_button.disabled = true;
	optimization_lvl_selector.disabled = true;
}

function enablePage()
{
	send_button.disabled = false;
	code_field.disabled = false;
	tests_description_field.disabled = false;
	verificator_field.disabled = false;
	file_button.disabled = false;
	optimization_lvl_selector.disabled = false;
}

function saveTokenToCookie(token)
{
	var date = new Date(new Date().getTime() + 3600 * 1000);
	document.cookie = "token=" + encodeURIComponent(token) + "; expires=" + date.toUTCString();
	//alert('token:\n' + token + '\n\ncookie:\n' + document.cookie + '\n\ndecoded cookie:\n' + decodeURIComponent(document.cookie));
}

function deleteTokenFromCookie()
{
	var date = new Date(0);
	document.cookie = "token=; expires=" + date.toUTCString();
}

function updateRequestReadystatechangeHandler()
{
	if (this.readyState != 4)
		return;

	if (this.status != 200)
	{
		output_field.innerHTML = this.status + ': ' + this.statusText;
		send_button.innerHTML = '<font size="5">Send</font>';
		enablePage();
		return;
	}
	else  //здесь происходит вывод результатов
	{
		//var status = this.responseText.match(/"status": "([^"]*)"/)[1];
		var response = JSON.parse(this.responseText);
		if (response.status === 'failed')
		{
			//error = this.responseText.match(/"data": "([^"]*)"/)[1];
			output_field.innerHTML = '<p>Failed</p><p>Error: ' + response.data + '</p>';
		}
		else
		{
			if (Array.isArray(response.result))
			{					
				var newWin = window.open();
				var n = response.result.length;
				var str = '';
				for (var i = 0; i < n; i++)
				{
					if (response.result[i].status === 'ok\n')
						str += '<p><font color="green">status: ok</font></p>';
					else
						str += '<p><font color="red">status: ' + response.result[i].status + '</font></p>';

					str += '<p>input: ' + response.result[i].input + '</p>';
					str += '<p>output: ' + response.result[i].output + '</p>';
					str += '<p>---------------------------------</p>';
				}
				newWin.document.write(str);
			}
			else
			{
				var str = '';
				for (var key in response.result)
				{
					str += '<p>' + key + ': ' + response.result[key] + '</p>';
				}
				output_field.innerHTML = str;
			}
		}
		send_button.innerHTML = '<font size="5">Send</font>';
		deleteTokenFromCookie();
		enablePage();
		return;
	}
}

function sendUpdateRequest(token)
{
	var update_request = JSON.stringify(
	{
		type: "update_status",
		token: token
	} );

	var xhr = new XMLHttpRequest();
	xhr.open('POST', '/api/v1/test', true);
	xhr.setRequestHeader('Content-Type', 'application/json');

	xhr.onreadystatechange = updateRequestReadystatechangeHandler;

	xhr.send(update_request);
}

function primaryRequestReadystatechangeHandler()
{
	if (this.readyState != 4)
		return;

	if (this.status != 200)
	{
		output_field.innerHTML = this.status + ': ' + this.statusText;
		send_button.innerHTML = '<font size="5">Send</font>';
		enablePage();
		return;
	}
	else
	{
		send_button.innerHTML = '<font size="5">Running...</font>';
		//output_field.innerHTML = this.responseText;  //отладка

		//var token = this.responseText.match(/"token": "([^"]*)"/)[1];
		var token = JSON.parse(this.responseText).token;
		saveTokenToCookie(token);

		sendUpdateRequest(token);
	}
}

function deleteSpacesExceptQuotes(str)
{
	var n = str.length;
	var substrings = [];
	var c, li = 0;
	for (var i = 0; i < n; i++)
	{
		res = str.slice(li).match(/["']/);
		if (!res)
		{
			substrings.push(str.slice(li).replace(/[ \n\t]/g, ''));
			break;
		}
		c = res[0];
		substrings.push(str.slice(li, li + res.index + 1).replace(/[ \n\t]/g, ''));
		li += res.index + 1;

		i++;

		res = str.slice(li).match(new RegExp(c));
		if (!res)
			throw new Error('Incorrect number of quotation marks.');
		substrings.push(str.slice(li, li + res.index + 1));
		li += res.index + 1;
	}
	return substrings.join('');
}

function sendRunTestingRequest()
{
	try
	{
		output_field.innerHTML = '';
		send_button.innerHTML = '<font size="5">Sending...</font>';
		disablePage();

		//var tests_description = tests_description_field.value.replace(/[ \n\t]/g, '');
		var tests_description = deleteSpacesExceptQuotes(tests_description_field.value);
		tests_description = notes.exec(tests_description, 0).res;  // массив
		//alert( JSON.stringify(tests_description, '', 4) );  // отладка
		var op_lvl = optimization_lvl_selector.value.match(/-O(.*)/)[1];
		var answer_type = document.getElementById('answer_type').value;
		var primary_request = JSON.stringify(
		{
			type: "run_tests",
			data:
			{
				code: code_field.value,
				options:
				{
					optimization_level: op_lvl
				},
				tests: tests_description,
				verifier: verificator_field.value,
				response_type: answer_type
			}
		} );

		var xhr = new XMLHttpRequest();
		xhr.open('POST', '/api/v1/test', true);
		xhr.setRequestHeader('Content-Type', 'application/json');
		xhr.onreadystatechange = primaryRequestReadystatechangeHandler;

		xhr.send(primary_request);
	}
	catch (err)
	{
		alert('Error.\n\n' + err.name + ':' + err.message + '\n\n' + err.stack);
		send_button.innerHTML = '<font size="5">Send</font>';
		enablePage();
	}
}

// import code from file
function loadFile()
{
	if (code_field.value !== '') alert('Text in the "Source code" field will be lost!');
	file_button.addEventListener("change", function(event)
	{
		var reader = new FileReader();

		reader.onload = function(event)
		{
			var content = event.target.result;
			code_field.value = content;
		};

		reader.onerror = function(event)
		{
			alert('Can\'t read the file. Error code: ' + event.target.error.code);
		};

		reader.readAsText(file_button.files[0]);		
	}, false);
}
