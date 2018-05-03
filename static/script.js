var send_button = document.getElementById('submit');
var code_field = document.getElementById('source_code');
var tests_description_field = document.getElementById('tests_description');
var verificator_field = document.getElementById('verification_script');
var file_button = document.getElementById('load_file');
var output_field = document.getElementById('output');

function disablePage()
{
	send_button.disabled = true;
	code_field.disabled = true;
	tests_description_field.disabled = true;
	verificator_field.disabled = true;
	file_button.disabled = true;
}

function enablePage()
{
	send_button.disabled = false;
	code_field.disabled = false;
	tests_description_field.disabled = false;
	verificator_field.disabled = false;
	file_button.disabled = false;
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
			tests: ["{" + tests_description_field.value + "}"],
			verifier: verificator_field.value,
			response_type: "raw_data"
		}
	} );

	xhr.onreadystatechange = function()
	{
		if (this.readyState != 4)
			return;

		if (this.status != 200)
		{
			output_field.innerHTML = this.status + ': ' + this.statusText;
			enablePage();
			return;
		}
		else
		{
			send_button.innerHTML = '<font size="5">Running...</font>';

			output_field.innerHTML = this.responseText;  //отладка

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

			xhr.onreadystatechange = function()
			{
				if (this.readyState != 4)
					return;

				if (this.status != 200)
				{
					output_field.innerHTML = this.status + ': ' + this.statusText;

					clearInterval(timerID);
					send_button.innerHTML = '<font size="5">Send</font>';
					enablePage();
					return;
				}
				else  //здесь происходит вывод результатов
				{
					var status = this.responseText.match(/"status": "([^"]*)"/)[1];
					if (status == 'failed')
					{
						output_field.innerHTML = 'Failed\nError: ' + this.responseText.match(/data: '(.*)'/)[1];
						clearInterval(timerID);
						send_button.innerHTML = '<font size="5">Send</font>';
						enablePage();
						return;
					}
					if (status == 'finished')  //TODO в протоколе два возможных ответа, поэтому я пока не стал ответ парсить, а просто вывожу его
					{
						output_field.innerHTML = this.responseText;
						clearInterval(timerID);
						send_button.innerHTML = '<font size="5">Send</font>';
						enablePage();
						return;
					}
					if (status != 'run')  //не знаю, что делать, когда приходит статус не failed, не finished и не run
					{ 
						output_field.innerHTML = this.responseText;
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
