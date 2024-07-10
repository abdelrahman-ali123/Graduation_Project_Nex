let outpatient_department_uploaded_file = document.getElementById(
		"outpatinet_department_file"
	),
	outpatient_department_uploaded_file_card = document.querySelector(
		"#outpatient_dep_sec .upload_file_sec .uploaded_file"
	),
	outpatient_department_file_submit_btn = document.querySelector(
		"#outpatient_dep_sec .upload_file_sec .submit_file"
	),
	outpatient_department_files_holder = document.querySelector(
		"#outpatient_dep_sec .upload_file_sec .upload_side .files_holder"
	),
	outpatient_department_menu = document.querySelector(
		".outpatient_department_menu"
	),
	clinics_names = document.getElementById("clinics_names"),
	simulation_window_info = document.querySelector(
		"#outpatient_dep_sec .simulation_graphs"
	);

let outpatient_department_data_ret = {
		from_example: false,
		file_num: 0,
		file_input_data: "",
		file_name: "",
	},
	outpatient_department_result = {},
	booking_ret = {
		mean_patient_num: 0,
		appointments_time: 0,
		mean_interarrival_time: 0,
	},
	simulated_clinic_ex = {};

document
	.querySelector(
		"#outpatient_dep_sec .upload_file_sec .upload_side .browse_files_btn"
	)
	.addEventListener("click", (_) =>
		outpatient_department_uploaded_file.click()
	);

// / Show files holder
document
	.querySelector(
		"#outpatient_dep_sec .upload_file_sec .upload_side .show_more_files"
	)
	.addEventListener("click", (_) => {
		outpatient_department_files_holder.classList.add("active");
	});

// Remove files holder
outpatient_department_files_holder
	.querySelector(".remove_files_holder")
	.addEventListener("click", (_) =>
		outpatient_department_files_holder.classList.remove("active")
	);

outpatient_department_uploaded_file.addEventListener("input", (e) => {
	if (e.target.value != "") {
		let file_info = e.target.files[0],
			name = file_info.name.split(".")[0];

		if (file_info.type != "text/csv") {
			alert("Please upload only csv files only!");
			outpatient_department_uploaded_file_card.classList.remove("active");
			outpatient_department_file_submit_btn.classList.add("inactive");
			return;
		}

		let reader = new FileReader();
		reader.onload = (_) => {
			let url = reader.result;
			file_content = url;
			outpatient_department_data_ret.file_input_data = url;
			outpatient_department_data_ret.file_num = 0;
			outpatient_department_data_ret.from_example = false;
			outpatient_department_data_ret.file_name = name;
			outpatient_department_files_holder
				.querySelector(".files ul li.selected")
				?.classList.remove("selected");
			if (outpatient_department_workspace_opened) {
				ApplyOutpatientDepartment(outpatient_department_data_ret);
			} else {
				ActivateOutpatientDepartmentFileCard(name, file_info.size);
			}
			e.target.value = "";
		};

		reader.readAsDataURL(file_info);
	}
});

outpatient_department_uploaded_file_card
	.querySelector(".delete_file")
	.addEventListener("click", (_) => {
		outpatient_department_uploaded_file.value = "";
		outpatient_department_uploaded_file_card.classList.remove("active");
		outpatient_department_uploaded_file_card.classList.remove("active");
		outpatient_department_file_submit_btn.classList.add("inactive");
		outpatient_department_files_holder
			.querySelector(".files ul li.selected")
			?.classList.remove("selected");

		outpatient_department_data_ret.file_input_data = "";
		outpatient_department_data_ret.file_num = 0;
		outpatient_department_data_ret.from_example = false;
		outpatient_department_data_ret.file_name = "";
	});

outpatient_department_uploaded_file_card
	.querySelector(".delete_file")
	.addEventListener("mouseover", (e) =>
		e.target.parentNode.classList.add("hover")
	);

outpatient_department_uploaded_file_card
	.querySelector(".delete_file")
	.addEventListener("mouseout", (e) =>
		e.target.parentNode.classList.remove("hover")
	);

// Choose file from example files
outpatient_department_files_holder.querySelectorAll(".files li").forEach((li) =>
	li.addEventListener("click", (_) => {
		outpatient_department_files_holder
			.querySelector(".files ul li.selected")
			?.classList.remove("selected");
		li.classList.add("selected");
		let name_size_cont = li.querySelector(".name-size");
		ActivateOutpatientDepartmentFileCard(
			name_size_cont.getAttribute("title"),
			parseFloat(name_size_cont.querySelector("i").innerText) * 1024
		);

		outpatient_department_data_ret.file_input_data = "";
		outpatient_department_data_ret.file_num = parseInt(
			li.getAttribute("file_num")
		);
		outpatient_department_data_ret.from_example = true;
		outpatient_department_data_ret.file_name =
			name_size_cont.getAttribute("title");
	})
);
outpatient_department_menu
	.querySelector(".close_outpatient_department_workspace")
	.addEventListener("click", (_) => {
		// Activate upload section
		document
			.querySelector("#outpatient_dep_sec .upload_file_sec")
			.classList.add("active");

		// Inactivate workspace section
		document
			.querySelector("#outpatient_dep_sec .workspace_sec")
			.classList.remove("active");

		// Inactivate control chart menu
		outpatient_department_menu.classList.remove("active");
		outpatient_department_workspace_opened = false;
	});
//
outpatient_department_menu
	.querySelectorAll(".outpatient_department_icons li")
	.forEach((li) => {
		li.addEventListener("click", (_) => {
			outpatient_department_menu
				.querySelector(".outpatient_department_icons li.active")
				.classList.remove("active");
			li.classList.add("active");
			ActivateOutpatientDepartmentSections(li.getAttribute("sec_type"));
		});
	});

outpatient_department_menu
	.querySelector(".upload_outpatient_department_file")
	.addEventListener("click", (_) =>
		outpatient_department_uploaded_file.click()
	);

outpatient_department_file_submit_btn.addEventListener("click", (_) => {
	ApplyOutpatientDepartment(outpatient_department_data_ret);
});
// Main summary graph buttons
document
	.querySelectorAll(
		"#outpatient_dep_sec .full_summary .graph .outpatient_graph_btns button"
	)
	.forEach((btn) => {
		btn.addEventListener("click", (_) => {
			document
				.querySelector(
					"#outpatient_dep_sec .full_summary .graph .outpatient_graph_btns button.active"
				)
				.classList.remove("active");
			btn.classList.add("active");
			get_main_analysis_data(
				btn.getAttribute("data_type"),
				btn.getAttribute("data_title")
			);
		});
	});

document
	.getElementById("simulate_two_clinics")
	.addEventListener("click", (_) => {
		ActivateSimulationWindow(simulated_clinic_ex);
	});

document.getElementById("try_booking_btn").addEventListener("click", (_) => {
	console.log(outpatient_department_data_ret);
	console.log(booking_ret);
	ApplyBookingSystem(booking_ret, outpatient_department_data_ret);
});
document
	.getElementById("booking_period")
	.addEventListener(
		"change",
		(e) => (booking_ret.appointments_time = e.target.value)
	);
document
	.querySelectorAll("#outpatient_dep_sec .cl_graph_btns button")
	.forEach((btn) =>
		btn.addEventListener("click", (_) => {
			document
				.querySelector("#outpatient_dep_sec .cl_graph_btns button.active")
				?.classList.remove("active");
			btn.classList.add("active");
			prepareClinicGraphData(
				btn.getAttribute("data_type"),
				btn.getAttribute("data_title")
			);
		})
	);
function ActivateOutpatientDepartmentFileCard(name, size) {
	outpatient_department_uploaded_file_card.querySelector(
		".name-size"
	).innerHTML = `${
		name.length > 20 ? `${name.substring(0, 20)}...` : name
	}<i>${(size / 1024).toFixed(2)} kb</i>`;

	outpatient_department_uploaded_file_card
		.querySelector(".name-size")
		.setAttribute("title", name);

	outpatient_department_uploaded_file_card.classList.add("active");

	outpatient_department_file_submit_btn.classList.remove("inactive");
}

function ApplyOutpatientDepartment(outpatient_department_data_ret) {
	// Send data to server to apply outpatient department simulation on in
	let loader = document.querySelector(".loader");
	loader.classList.add("active");
	fetch(`${window.origin}/apply_outpatient_department`, {
		method: "POST",
		credentials: "include",
		body: JSON.stringify(outpatient_department_data_ret),
		cache: "no-cache",
		headers: new Headers({
			"content-type": "application/json",
		}),
	}).then((response) => {
		if (response.status !== 200) {
			alert(`Response status was not 200: ${response.status}`);
			loader.classList.remove("active");

			return;
		}
		response.json().then((data) => {
			loader.classList.remove("active");

			if (!outpatient_department_workspace_opened) {
				// Inactivate upload section
				document
					.querySelector("#outpatient_dep_sec .upload_file_sec")
					.classList.remove("active");

				// Activate workspace section
				document
					.querySelector("#outpatient_dep_sec .workspace_sec")
					.classList.add("active");

				// Activate outpatient department menu
				outpatient_department_menu.classList.add("active");

				outpatient_department_workspace_opened = true;
			}

			HandleOutpatientDepartmentData(data);
			return;
		});
	});
}
function prepareClinicGraphData(data_type, data_title) {
	console.log(parseInt(clinics_names.value.split("-")[1]));

	console.log(outpatient_department_result.main_analysis[data_type]);
	let data_mean = (
			outpatient_department_result.main_analysis[data_type].reduce(
				(accumulator, currentValue) => accumulator + currentValue,
				0
			) / outpatient_department_result.main_analysis[data_type].length
		).toFixed(2),
		data_value =
			outpatient_department_result.main_analysis[data_type][
				parseInt(clinics_names.value.split("-")[1])
			];
	plot_clinic_graph(
		[`${clinics_names.value.split("-")[0].toUpperCase()}`],
		[data_value],
		["OPD"],
		[data_mean],
		data_title,
		`OPD ${data_title}`,
		""
	);
}
function ApplyBookingSystem(booking_ret, outpatient_department_data_ret) {
	// Send data to server to apply outpatient department simulation on in
	let loader = document.querySelector(".loader");
	loader.classList.add("active");
	fetch(`${window.origin}/apply_booking_system`, {
		method: "POST",
		credentials: "include",
		body: JSON.stringify({
			outpatient_dep: outpatient_department_data_ret,
			booking_sys: booking_ret,
		}),
		cache: "no-cache",
		headers: new Headers({
			"content-type": "application/json",
		}),
	}).then((response) => {
		if (response.status !== 200) {
			alert(`Response status was not 200: ${response.status}`);
			loader.classList.remove("active");

			return;
		}
		response.json().then((data) => {
			loader.classList.remove("active");

			console.log(data);
			ActivateSimulationBookingWindow(data.result);
			return;
		});
	});
}

// Activate outpatients departmernt main sections
function ActivateOutpatientDepartmentSections(sec_type) {
	document
		.querySelector("#outpatient_dep_sec .wrk-sections.active")
		.classList.remove("active");
	document.getElementById(sec_type).classList.add("active");
}

function HandleOutpatientDepartmentData(data) {
	outpatient_department_result = data.result;
	console.log(outpatient_department_result);

	// Full analysis
	document.querySelector(
		"#outpatient_dep_sec .full_summary .main_summary"
	).innerHTML = outpatient_department_result.summary_report;

	get_main_analysis_data("mean_waiting_times", "Mean waiting time (min.)");

	// For each clinic
	let clinic_types = outpatient_department_result.main_analysis.clinic_types;
	clinics_names.innerHTML = "";
	for (let i = 0; i < clinic_types.length; i++) {
		if (i == 0)
			clinics_names.innerHTML += `<option value="${
				clinic_types[i]
			}-${i}" selected ">${clinic_types[i].toUpperCase()}</option>`;
		else {
			clinics_names.innerHTML += `<option value="${
				clinic_types[i]
			}-${i}" >${clinic_types[i].toUpperCase()}</option>`;
		}
	}

	document.querySelector("#outpatient_dep_sec .clinics_header h1").innerText =
		clinics_names.value.split("-")[0].toUpperCase();

	get_clinic_data(
		clinics_names.value.split("-")[1],
		clinics_names.value.split("-")[0]
	);

	clinics_names.addEventListener("change", (_) => {
		get_clinic_data(
			clinics_names.value.split("-")[1],
			clinics_names.value.split("-")[0]
		);
		document.querySelector("#outpatient_dep_sec .clinics_header h1").innerText =
			clinics_names.value.split("-")[0].toUpperCase();
		prepareClinicGraphData("mean_waiting_times", "Waiting time (min.)");
		document
			.querySelectorAll("#outpatient_dep_sec .cl_graph_btns button")
			.forEach((btn) => btn.classList.remove("active"));
		document
			.querySelectorAll("#outpatient_dep_sec .cl_graph_btns button")[0]
			.classList.add("active");
	});

	prepareClinicGraphData("mean_waiting_times", "Waiting time (min.)");
	document
		.querySelectorAll("#outpatient_dep_sec .cl_graph_btns button")
		.forEach((btn) => btn.classList.remove("active"));
	document
		.querySelectorAll("#outpatient_dep_sec .cl_graph_btns button")[0]
		.classList.add("active");
}

function get_main_analysis_data(data_type, data_title) {
	let main_analysis = outpatient_department_result.main_analysis;
	plot_main_analysis_data(
		main_analysis.clinic_types,
		main_analysis[data_type],
		data_title
	);
	return;
}

function plot_main_analysis_data(x_data, y_data, data_title) {
	let data = [
			{
				x: x_data,
				y: y_data,
				type: "bar",
				name: data_title,
				marker: {
					color: "#f2dabf",
				},
				text: y_data.map(String),
				textposition: "auto",
			},
		],
		layout = {
			title: data_title,
			paper_bgcolor: "#00010000",
			plot_bgcolor: "#00010000",
			// showlegend: true,
			barmode: "group",
			legend: { orientation: "v" },
			margin: {
				l: 30,
				r: 60,
				b: 80,
				t: 30,
				pad: 1,
			},
			xaxis: {
				type: "data",
				showgrid: false,
			},
			yaxis: {
				type: "linear",
				showgrid: false,
			},
			height: 350,
			width: 700,
			font: { color: "#fff", size: "9" },
			hoverlabel: {
				bgcolor: "black",
				font: { color: "white" },
			},
		};

	Plotly.newPlot("outpatient_clinics_graph", data, layout);
}
function plot_simulation_data(
	x1_data,
	y1_data,
	x2_data,
	y2_data,
	data1_title,
	data2_title,
	main_title
) {
	let data = [
			{
				x: x1_data,
				y: y1_data,
				type: "bar",
				name: data1_title,
				marker: {
					color: "#f2dabf",
				},
				text: y1_data.map(String),
				textposition: "auto",
			},
			{
				x: x2_data,
				y: y2_data,
				type: "bar",
				name: data2_title,
				marker: {
					color: "#ff662b",
				},
				text: y2_data.map(String),
				textposition: "auto",
			},
		],
		layout = {
			title: main_title,
			paper_bgcolor: "#00010000",
			plot_bgcolor: "#00010000",
			// showlegend: true,
			barmode: "group",
			legend: { orientation: "h" },
			margin: {
				l: 30,
				r: 60,
				b: 80,
				t: 30,
				pad: 1,
			},
			xaxis: {
				type: "data",
				showgrid: false,
			},
			yaxis: {
				type: "linear",
				showgrid: false,
			},
			height: 300,
			width: 300,
			font: { color: "#fff", size: "9" },
			hoverlabel: {
				bgcolor: "black",
				font: { color: "white" },
			},
			bargroupgap: 0.1,
		};

	Plotly.newPlot("simulation_graph", data, layout);
}
function plot_clinic_graph(
	x1_data,
	y1_data,
	x2_data,
	y2_data,
	data1_title,
	data2_title,
	main_title
) {
	let data = [
			{
				x: x1_data,
				y: y1_data,
				type: "bar",
				name: data1_title,
				marker: {
					color: "#f2dabf",
				},
				text: y1_data.map(String),
				textposition: "auto",
			},
			{
				x: x2_data,
				y: y2_data,
				type: "bar",
				name: data2_title,
				marker: {
					color: "#ff662b",
				},
				text: y2_data.map(String),
				textposition: "auto",
			},
		],
		layout = {
			title: main_title,
			paper_bgcolor: "#00010000",
			plot_bgcolor: "#00010000",
			// showlegend: true,
			barmode: "group",
			legend: { orientation: "h" },
			margin: {
				l: 30,
				r: 60,
				b: 80,
				t: 30,
				pad: 1,
			},
			xaxis: {
				type: "data",
				showgrid: false,
			},
			yaxis: {
				type: "linear",
				showgrid: false,
			},
			height: 350,
			width: 400,
			font: { color: "#fff", size: "9" },
			hoverlabel: {
				bgcolor: "black",
				font: { color: "white" },
			},
			bargroupgap: 0.1,
		};

	Plotly.newPlot("cl_graph", data, layout);
}

function get_clinic_data(clinic_number, clinic_name) {
	let main_analysis = outpatient_department_result.main_analysis,
		simulate_servers = outpatient_department_result.simulate_servers,
		clinics_reports = outpatient_department_result.clinics_reports;
	// Booking
	booking_ret.appointments_time =
		document.getElementById("booking_period").value;
	booking_ret.mean_interarrival_time =
		main_analysis.mean_interarrival_time[parseInt(clinic_number)];
	booking_ret.mean_patient_num =
		main_analysis.mean_number_of_patients[parseInt(clinic_number)];
	console.log(booking_ret);

	// Two clinics
	console.log(clinic_name);
	simulated_clinic_ex = simulate_servers[clinic_name];
	console.log(clinics_reports[clinic_name]);
	// return (
	// 	simulate_servers[parseInt(clinic_number)], clinics_reports[clinic_name]
	// );
	AddClinicReport(clinics_reports[clinic_name]);
	simulation_window_info.classList.contains("active")
		? simulation_window_info.classList.remove("active")
		: null;
}

function AddClinicReport(clinic_report) {
	document.querySelector(
		"#outpatient_dep_sec .clinics_body .clinic_summary .cl_sum"
	).innerHTML = clinic_report;
}

function ActivateSimulationWindow(res) {
	console.log(res);

	simulation_window_info.classList.contains("active")
		? null
		: simulation_window_info.classList.add("active");

	plot_simulation_data(
		[clinics_names.value.split("-")[0]],
		[res.before_after[0]],
		[clinics_names.value.split("-")[0]],
		[res.before_after[1]],
		"Without establishing an additional clinic",
		"With establishing an additional clinic ",
		""
	);

	simulation_window_info.querySelector("p").innerHTML = res.analysis_summary;
	simulation_window_info.querySelector("h1").innerText =
		"Effect of establishing an additional clinic on waiting time for patients";
}
function ActivateSimulationBookingWindow(res) {
	console.log(res);

	simulation_window_info.classList.contains("active")
		? null
		: simulation_window_info.classList.add("active");

	plot_simulation_data(
		[clinics_names.value.split("-")[0]],
		[res.before_after[0]],
		[clinics_names.value.split("-")[0]],
		[res.before_after[1]],
		"Without performing booking system",
		"With performing booking system ",
		""
	);

	simulation_window_info.querySelector("p").innerHTML = res.analysis_summary;
	simulation_window_info.querySelector(
		"h1"
	).innerText = `Effect of performing ${res.times} min. booking system on waiting time for patients`;
}
