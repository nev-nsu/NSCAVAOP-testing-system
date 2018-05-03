var send_button = document.getElementById('submit');
var code_field = document.getElementById('source_code');
var tests_description = document.getElementById('tests_description');
var verificator = document.getElementById('verification_script');
var file_send_button = document.getElementById('load_file');

function disablePage()
{
	send_button.disabled = true;
	code_field.disabled = true;
	tests_description.disabled = true;
	verificator.disabled = true;
	file_send_button.disabled = true;
}

function enablePage()
{
	send_button.disabled = false;
	code_field.disabled = false;
	tests_description.disabled = false;
	verificator.disabled = false;
	file_send_button.disabled = false;
}

function runTesting()
{
	var xhr = new XMLHttpRequest();
	xhr.open('POST', '/api/v1/test', true);
	xhr.setRequestHeader('Content-Type', 'application/json');

	send_button.innerHTML = '<font size="5">Sending...</font>';
	disablePage();

	var primary_request = JSON.stringify(
	{
		primary: true,
		type: "run_tests",
		data:
		{
			code: code_field.value,
			options:
			{
				optimization_level: 3
			},
			tests: ["{" + tests_description.value + "}"],
			verifier: verificator.value,
			response_type: "raw_data"
		}
	} );

	xhr.onreadystatechange = function()
	{
		if (this.readyState != 4)
			return;

		if (this.status != 200)
		{
			document.getElementById('output').innerHTML = this.status + ': ' + this.statusText;
			enablePage();
			return;
		}
		else
		{
			send_button.innerHTML = '<font size="5">Running...</font>';

			document.getElementById('output').innerHTML = this.responseText;  //отладка

			var token = this.responseText.match(/"token": "([^"]*)"/)[1];
			var update_request = JSON.stringify(
			{
				primary: false,
				type: "update_status",
				token: token
			} );

			var xhr = new XMLHttpRequest();
			xhr.open('POST', '/api/v1/test', true);
			xhr.setRequestHeader('Content-Type', 'application/json');

			var status = 'run';
			xhr.onreadystatechange = function()
			{
				if (this.readyState != 4)
					return;

				if (this.status != 200)
				{
					alert(this.status + ': ' + this.statusText);
					status = 'error';

					clearInterval(timerID);
					send_button.innerHTML = '<font size="5">Send</font>';
					enablePage();
					return;
				}
				else  //здесь происходит вывод результатов
				{
					status = this.responseText.match(/"status": "([^"]*)"/)[1];
					if (status == 'failed')
					{
						document.getElementById('output').innerHTML = 'Failed\nError: ' + this.responseText.match(/data: '(.*)'/)[1];
						clearInterval(timerID);
						send_button.innerHTML = '<font size="5">Send</font>';
						enablePage();
						return;
					}
					if (status == 'finished')  //TODO в протоколе два возможных ответа, поэтому я пока не стал ответ парсить, а просто вывожу его
					{
						document.getElementById('output').innerHTML = this.responseText;
						clearInterval(timerID);
						send_button.innerHTML = '<font size="5">Send</font>';
						enablePage();
						return;
					}
					if (status != 'run')  //не знаю, что делать, когда приходит статус не failed, не finished и не run
					{ 
						document.getElementById('output').innerHTML = this.responseText;
						clearInterval(timerID);
						send_button.innerHTML = '<font size="5">Send</font>';
						enablePage();
						return;
					}
				}
			}

			var timerID = setInterval( function() { xhr.send(update_request) }, 2000);
		}
	}
	xhr.send(primary_request);
}

// import code from file
function loadFile()
{
	var text_field = document.getElementById('source_code');
	var input = document.getElementById('load_file');
	input.addEventListener("change", function(event)
	{
		var reader = new FileReader();

		reader.onload = function(event)
		{
			var content = event.target.result;
			text_field.value = content;
		};

		reader.onerror = function(event)
		{
			alert('Can\'t read the file. Error code: ' + event.target.error.code);
		};

		reader.readAsText(input.files[0]);		
	}, false);
}
