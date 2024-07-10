let control_charts_uploaded_file =
		document.getElementById("control_chart_file"),
	control_chart_uploaded_file_card = document.querySelector(
		"#control_charts_sec .upload_file_sec .uploaded_file"
	),
	control_chart_file_submit_btn = document.querySelector(
		"#control_charts_sec .upload_file_sec .submit_file"
	),
	control_charts_files_holder = document.querySelector(
		"#control_charts_sec .upload_file_sec .upload_side .files_holder"
	),
	control_charts_menu = document.querySelector(".control_charts_menu");

let control_charts_data_ret = {
	from_example: false,
	file_num: 0,
	file_input_data: "",
	file_name: "",
};

document
	.querySelector(
		"#control_charts_sec .upload_file_sec .upload_side .browse_files_btn"
	)
	.addEventListener("click", (_) => control_charts_uploaded_file.click());
// Show files holder
document
	.querySelector(
		"#control_charts_sec .upload_file_sec .upload_side .show_more_files"
	)
	.addEventListener("click", (_) => {
		control_charts_files_holder.classList.add("active");
	});
// Remove files holder
control_charts_files_holder
	.querySelector(".remove_files_holder")
	.addEventListener("click", (_) =>
		control_charts_files_holder.classList.remove("active")
	);

control_charts_uploaded_file.addEventListener("input", (e) => {
	if (e.target.value != "") {
		let file_info = e.target.files[0],
			name = file_info.name.split(".")[0];

		if (file_info.type != "text/csv") {
			alert("Please upload only csv files only!");
			control_chart_uploaded_file_card.classList.remove("active");
			control_chart_file_submit_btn.classList.add("inactive");
			return;
		}

		let reader = new FileReader();
		reader.onload = (_) => {
			let url = reader.result;
			file_content = url;
			control_charts_data_ret.file_input_data = url;
			control_charts_data_ret.file_num = 0;
			control_charts_data_ret.from_example = false;
			control_charts_data_ret.file_name = name;
			control_charts_files_holder
				.querySelector(".files ul li.selected")
				?.classList.remove("selected");

			if (control_charts_workspace_opened) {
				ApplyControlCharts(control_charts_data_ret);
			} else {
				ActivateControlChartFileCard(name, file_info.size);
			}
			e.target.value = "";
		};

		reader.readAsDataURL(file_info);
	}
});

control_chart_uploaded_file_card
	.querySelector(".delete_file")
	.addEventListener("click", (_) => {
		control_charts_uploaded_file.value = "";
		control_chart_uploaded_file_card.classList.remove("active");
		control_chart_uploaded_file_card.classList.remove("active");
		control_chart_file_submit_btn.classList.add("inactive");
		control_charts_files_holder
			.querySelector(".files ul li.selected")
			?.classList.remove("selected");

		control_charts_data_ret.file_input_data = "";
		control_charts_data_ret.file_num = 0;
		control_charts_data_ret.from_example = false;
		control_charts_data_ret.file_name = "";
	});

control_chart_uploaded_file_card
	.querySelector(".delete_file")
	.addEventListener("mouseover", (e) =>
		e.target.parentNode.classList.add("hover")
	);

control_chart_uploaded_file_card
	.querySelector(".delete_file")
	.addEventListener("mouseout", (e) =>
		e.target.parentNode.classList.remove("hover")
	);

// Choose file from example files
control_charts_files_holder.querySelectorAll(".files li").forEach((li) =>
	li.addEventListener("click", (_) => {
		control_charts_files_holder
			.querySelector(".files ul li.selected")
			?.classList.remove("selected");
		li.classList.add("selected");
		let name_size_cont = li.querySelector(".name-size");
		ActivateControlChartFileCard(
			name_size_cont.getAttribute("title"),
			parseFloat(name_size_cont.querySelector("i").innerText) * 1024
		);

		control_charts_data_ret.file_input_data = "";
		control_charts_data_ret.file_num = parseInt(li.getAttribute("file_num"));
		control_charts_data_ret.from_example = true;
		control_charts_data_ret.file_name = name_size_cont.getAttribute("title");

		ActivateControlChartGraphMenu();
	})
);

control_chart_file_submit_btn.addEventListener("click", (_) => {
	ApplyControlCharts(control_charts_data_ret);
});

// Inactivate workspace section
control_charts_menu
	.querySelector(".close_control_chart_workspace")
	.addEventListener("click", (_) => {
		// Activate upload section
		document
			.querySelector("#control_charts_sec .upload_file_sec")
			.classList.add("active");

		// Inactivate workspace section
		document
			.querySelector("#control_charts_sec .workspace_sec")
			.classList.remove("active");

		// Inactivate control chart menu
		control_charts_menu.classList.remove("active");
		control_charts_workspace_opened = false;
		ActivateControlChartGraphMenu();
	});

//
control_charts_menu.querySelectorAll(".chart_icons li").forEach((li) => {
	li.addEventListener("click", (_) => {
		control_charts_menu
			.querySelector(".chart_icons li.active")
			.classList.remove("active");
		li.classList.add("active");
		ActivateControlChartsSections(li.getAttribute("sec_type"));
		ActivateControlChartGraphMenu();
	});
});

control_charts_menu
	.querySelector(".upload_control_chart_file")
	.addEventListener("click", (_) => control_charts_uploaded_file.click());

document.querySelectorAll(".control_charts_graph_menu li").forEach((li) => {
	li.addEventListener("click", (_) => {
		document
			.querySelector(".control_charts_graph_menu li.active")
			.classList.remove("active");
		li.classList.add("active");
		ActivateControlChartGraph(li.getAttribute("sec_type"));
	});
});

ActivateControlChartGraphMenu();

// Activation file card when uplaoding or selecting file for applying control chart
function ActivateControlChartFileCard(name, size) {
	control_chart_uploaded_file_card.querySelector(".name-size").innerHTML = `${
		name.length > 20 ? `${name.substring(0, 20)}...` : name
	}<i>${(size / 1024).toFixed(2)} kb</i>`;

	control_chart_uploaded_file_card
		.querySelector(".name-size")
		.setAttribute("title", name);

	control_chart_uploaded_file_card.classList.add("active");

	control_chart_file_submit_btn.classList.remove("inactive");
}

// Activate control charts secitons (charts and analysis summary)
function ActivateControlChartsSections(sec_type) {
	document
		.querySelector("#control_charts_sec .wrk-sections.active")
		.classList.remove("active");
	document.getElementById(sec_type).classList.add("active");
}

// Send data to server to apply control charts on in
function ApplyControlCharts(control_charts_data_ret) {
	let loader = document.querySelector(".loader");
	loader.classList.add("active");

	fetch(`${window.origin}/apply_control_charts`, {
		method: "POST",
		credentials: "include",
		body: JSON.stringify(control_charts_data_ret),
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

			if (!control_charts_workspace_opened) {
				// Inactivate upload section
				document
					.querySelector("#control_charts_sec .upload_file_sec")
					.classList.remove("active");

				// Activate workspace section
				document
					.querySelector("#control_charts_sec .workspace_sec")
					.classList.add("active");

				// Activate control chart menu
				control_charts_menu.classList.add("active");

				control_charts_workspace_opened = true;
			}

			HandleControlChartData(data);

			return;
		});
	});
}

// Creaitng data for the plot
function GetControlChartPlotData(result) {
	let graph_coordinates = result.graph_coordinates,
		lcl_line = result.lcl_line,
		ucl_line = result.ucl_line,
		mean_line = result.mean_line,
		svc_trend_points = result.scv_with_pattern,
		scv_out_limits_points = result.scv_out_of_limits;

	let graph = {
			mode: "lines+markers",
			x: graph_coordinates.x,
			y: graph_coordinates.y,
			line: {
				color: "#80FFB380",
				dash: "solid",
			},
			name: result.y_label,
			hoverinfo: "x+y",
			showlegend: true,
		},
		lcl = {
			mode: "lines",
			x: lcl_line.x,
			y: lcl_line.y,
			line: {
				color: "#FFB38080",
				dash: "dash",
			},
			name: "Low control level",
			hoverinfo: "x+y",
		},
		ucl = {
			mode: "lines",
			x: ucl_line.x,
			y: ucl_line.y,
			line: {
				color: "#FFB38080",
				dash: "dash",
			},
			name: "Upper control level",
			hoverinfo: "x+y",
		},
		mean = {
			mode: "lines",
			x: mean_line.x,
			y: mean_line.y,
			line: {
				color: "#80BFFF80",
				dash: "dash",
			},
			name: "Mean",
			hoverinfo: "x+y",
		},
		svc_trend = {
			mode: "markers",
			x: svc_trend_points.x,
			y: svc_trend_points.y,
			line: {
				color: "#FF808080",
			},
			name: "Trends",
			hoverinfo: "x+y",
		},
		svc_out_limits = {
			mode: "markers",
			x: scv_out_limits_points.x,
			y: scv_out_limits_points.y,
			line: {
				color: "#FF808080",
			},
			name: "Special control variation",
			hoverinfo: "x+y",
		};

	return [graph, mean, lcl, ucl, svc_trend, svc_out_limits];
}

// Data plotting
function PlotControlChart(graph_cont, plot_data, plot_title, x_label, y_label) {
	const config = { responsive: true };

	let new_data = plot_data,
		new_layout = {
			title: plot_title.toUpperCase(),
			paper_bgcolor: "#00010000",
			plot_bgcolor: "#00010000",
			showlegend: true,
			legend: { orientation: "h" },
			margin: {
				l: 30,
				r: 10,
				b: 30,
				t: 30,
				pad: 1,
			},
			xaxis: {
				type: "data",
				title: x_label,
				showgrid: false,
			},
			yaxis: {
				type: "linear",
				title: y_label,
				showgrid: false,
			},
			height: 210,
			width: 320,
			font: { color: "#fff", size: "7" },
			hoverlabel: {
				bgcolor: "black",
				font: { color: "white" },
			},
		};
	// const animationConfig = {
	// 	transition: {
	// 		duration: 500,
	// 		easing: "cubic-in-out",
	// 	},
	// 	frame: {
	// 		duration: 500,
	// 	},
	// };
	Plotly.newPlot(graph_cont, new_data, new_layout, config);
	// Plotly.animate(graph_cont, { data: new_data }, { ...animationConfig });
}

// Preparing for displaying return data form control charts api
function HandleControlChartData(result) {
	let result_data = result.result,
		sum_cont = document.querySelector(
			"#control_charts_sec .workspace_sec #summary_window .cnt"
		),
		charts_cont = document.querySelector(
			"#control_charts_sec .workspace_sec #control_charts_window .charts_cont"
		),
		fix_button = control_charts_menu.querySelector("ul li.fix_chart_btn");
	// Add summary to summary container
	sum_cont.innerHTML = result_data.res_text;

	document.getElementById("graph_02").classList.contains("active")
		? document.getElementById("graph_02").classList.remove("active")
		: null;

	document.getElementById("graph_01").classList.contains("active")
		? null
		: document.getElementById("graph_01").classList.add("active");

	if (
		result_data.hasOwnProperty("chart_01") &&
		result_data.hasOwnProperty("chart_02")
	) {
		// fix_button.style.display = "none";
		fix_button.classList.contains("active")
			? fix_button.classList.remove("active")
			: null;

		PlotChart(
			"graph_01",
			PrepareChartsInfo(result_data.chart_01),
			result_data.chart_01.chart_used,
			" ",
			result_data.chart_01.y_label
		);
		PlotChart(
			"graph_02",
			PrepareChartsInfo(result_data.chart_02),
			result_data.chart_02.chart_used,
			" ",
			result_data.chart_02.y_label
		);

		document.getElementById("graph_02").classList.contains("exist")
			? null
			: document.getElementById("graph_02").classList.add("exist");

		ActivateControlChartGraphMenu();
	} else {
		PlotChart(
			"graph_01",
			PrepareChartsInfo(result_data),
			result_data.chart_used,
			" ",
			result_data.y_label
		);

		document.getElementById("graph_02").classList.contains("exist")
			? document.getElementById("graph_02").classList.remove("exist")
			: null;
		ActivateControlChartGraphMenu();

		if (!result_data.is_controlled && result_data.can_be_fixed) {
			fix_button.classList.contains("active")
				? null
				: fix_button.classList.add("active");

			document.getElementById("graph_02").classList.contains("exist")
				? document.getElementById("graph_02").classList.remove("exist")
				: null;
			ActivateControlChartGraphMenu();

			fix_button.addEventListener("click", (_) => {
				sum_cont.innerHTML = `\n${result_data.new_res_text}`;
				// fix_button.style.display = "none";

				fix_button.classList.contains("active")
					? fix_button.classList.remove("active")
					: null;

				PlotChart(
					"graph_01",
					PrepareChartsInfo(result_data),
					result_data.chart_used,
					" ",
					result_data.y_label
				);

				PlotChart(
					"graph_02",
					PrepareChartsInfo(result_data.new_res),
					`Fixed ${result_data.new_res.chart_used}`,
					" ",
					result_data.y_label
				);

				document.getElementById("graph_02").classList.contains("exist")
					? null
					: document.getElementById("graph_02").classList.add("exist");

				ActivateControlChartGraphMenu();
			});
		} else {
			fix_button.classList.contains("active")
				? fix_button.classList.remove("active")
				: null;

			document.getElementById("graph_02").classList.contains("exist")
				? document.getElementById("graph_02").classList.remove("exist")
				: null;

			ActivateControlChartGraphMenu();
		}
	}
	return;
}

function PrepareChartsInfo(result) {
	let graph_coordinates = result.graph_coordinates,
		lcl_line = result.lcl_line,
		ucl_line = result.ucl_line,
		mean_line = result.mean_line,
		svc_trend_points = result.scv_with_pattern,
		scv_out_limits_points = result.scv_out_of_limits;

	let graph = {
			mode: "lines+markers",
			x: graph_coordinates.x,
			y: graph_coordinates.y,
			line: {
				color: "#80ffb3",
				dash: "solid",
			},
			name: result.y_label,
			hoverinfo: "x+y",
			showlegend: true,
		},
		lcl = {
			mode: "lines",
			x: lcl_line.x,
			y: lcl_line.y,
			line: {
				color: "#ffb380",
				dash: "dash",
			},
			name: "Low control level",
			hoverinfo: "x+y",
		},
		ucl = {
			mode: "lines",
			x: ucl_line.x,
			y: ucl_line.y,
			line: {
				color: "#ffb380",
				dash: "dash",
			},
			name: "Upper control level",
			hoverinfo: "x+y",
		},
		mean = {
			mode: "lines",
			x: mean_line.x,
			y: mean_line.y,
			line: {
				color: "#80bfff",
				dash: "dash",
			},
			name: "Mean",
			hoverinfo: "x+y",
		},
		svc_trend = {
			mode: "markers",
			x: svc_trend_points.x,
			y: svc_trend_points.y,
			line: {
				color: "#ff662b",
			},
			name: "Trends",
			hoverinfo: "x+y",
		},
		svc_out_limits = {
			mode: "markers",
			x: scv_out_limits_points.x,
			y: scv_out_limits_points.y,
			line: {
				color: "#ff662b",
			},
			name: "Special control variation",
			hoverinfo: "x+y",
		};

	return [graph, mean, lcl, ucl, svc_trend, svc_out_limits];
}

function PlotChart(graph_cont, plot_data, plot_title, x_label, y_label) {
	const config = { responsive: true };

	let new_data = plot_data,
		new_layout = {
			title: plot_title.toUpperCase(),
			paper_bgcolor: "#00010000",
			plot_bgcolor: "#00010000",
			showlegend: true,
			legend: { orientation: "v" },
			margin: {
				l: 70,
				r: 10,
				b: 30,
				t: 30,
				pad: 1,
			},
			xaxis: {
				type: "data",
				title: x_label,
				showgrid: false,
			},
			yaxis: {
				type: "linear",
				title: y_label,
				showgrid: false,
			},
			height: 370,
			width: 1000,
			font: { color: "#f2dabf80", size: "10" },
			hoverlabel: {
				bgcolor: "black",
				font: { color: "#ffffff80" },
			},
		};
	Plotly.newPlot(graph_cont, new_data, new_layout, config);
}

//
function ActivateControlChartGraph(sec_type) {
	document
		.querySelector(
			"#control_charts_sec .charts_cont .control_chart_graph.active"
		)
		.classList.remove("active");
	document.getElementById(sec_type).classList.add("active");
}
