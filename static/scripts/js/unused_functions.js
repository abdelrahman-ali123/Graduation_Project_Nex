function SendDate(control_charts_data_ret) {
	fetch(`${window.origin}/update_example_files`, {
		method: "POST",
		credentials: "include",
		body: JSON.stringify(control_charts_data_ret),
		cache: "no-cache",
		headers: new Headers({
			"content-type": "application/json",
		}),
	}).then((response) => {
		if (response.status !== 200) {
			console.log(`Response status was not 200: ${response.status}`);
			alert(`Response status was not 200: ${response.status}`);
			return;
		}
		response.json().then((data) => {
			console.log(data);
			return;
		});
	});
}
