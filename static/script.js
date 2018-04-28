// send request
function sendRequest()
{
	alert('You tried to send request.');
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
