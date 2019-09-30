document.addEventListener('DOMContentLoaded', submitConfig);

//*******************************************
//AJAX function so form can submit config
//Pastes response into webpage
//*******************************************
function submitConfig() {
	let add = document.getElementById('config');
	add.addEventListener("submit", function (event) {
		let req = new XMLHttpRequest();

		//store data from form
		let payload = document.getElementById('conf').value;
		console.log(payload)

		//open POST request
		req.open('POST', "/config", true);
		req.setRequestHeader('Content-Type', 'text/plain');

		//async send of POST
		req.addEventListener('load', function () {
			if (req.status == 200) {
				//create a table row with necessary form data
				let data = req.responseText;
				console.log(data);
				document.getElementById('Results').innerText = data
			}
		});

		req.send(payload);
		event.preventDefault();
	});
}
