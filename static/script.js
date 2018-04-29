function runTesting()
{
	var xhr = new XMLHttpRequest();

	var button = document.getElementById('submit');
	var code_field = document.getElementById('source_code');
	var descr_field = document.getElementById('tests_description');
	var ver_script_field = document.getElementById('verification_script');

	var prim_request = '{primary:true,type:\'run_tests\',data:{code:\'' + code_field.value + '\',options:{optimization_level:\'3\'},tests:[{' + descr_field.value + '}],verifier:\'' + ver_script_field.value + '\',response_type:\'raw_data\'}}';

	xhr.open('POST', 'api/v1/test', true);
	xhr.setRequestHeader('Content-Type', 'application/json');

	button.innerHTML = '<font size="5">Sending...</font>';
	button.disabled = true;
	code_field.disabled = true;
	descr_field.disabled = true;
	ver_script_field.disabled = true;

	xhr.onreadystatechange = function()
	{
		if (this.readyState != 4)
			return;

		button.innerHTML = '<font size="5">Send</font>';
		button.disabled = false;
		code_field.disabled = false;
		descr_field.disabled = false;
		ver_script_field.disabled = false;

		if (this.status != 200)
		{
			alert(this.status + ': ' + this.statusText);
			return;
		}
		else
		{
			button.innerHTML = '<font size="5">Running...</font>';

			var token = this.responseText.match(/token: '(.*)'/)[1];

			var update_request = 'primary:false,type:\'update_status\',token:\'' + token + '\'}';

			var xhr = new XMLHttpRequest();
			xhr.open('POST', 'api/v1/test', true);
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

					button.innerHTML = '<font size="5">Send</font>';
					button.disabled = false;
					code_field.disabled = false;
					descr_field.disabled = false;
					ver_script_field.disabled = false;

					return;
				}
				else
				{
					status = this.responseText.match(/status: '(.*)'/)[1];

					if (status === 'failed')
					{
						document.getElementById('output').innerHTML = 'Failed\nError: ' + this.responseText.match(/data: '(.*)'/)[1];
						return;
					}
					if (status === 'finished')
					{
						//TODO в протоколе два возсожных ответа, поэтому я пока не стал ответ парсить, а просто вывожу его
						document.getElementById('output').innerHTML = this.responseText;
						return;
					}
				}
			}

			while (status === 'run')
			{
				setTimeout(function() { xhr.send(request) }, 1000);
			}
		}
	}
				
	xhr.send(prim_request);
}

// import code from file
function loadFile()
{
	var text_field = document.getElementById('source_code');
	if (text_field.value !== '') alert('Code in the field will be lost!');

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
			alert('Error: ' + event.target.error);
		};

		reader.readAsText(input.files[0]);		
	}, false);
}
