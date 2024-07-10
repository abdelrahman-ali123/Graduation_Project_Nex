let control_charts_workspace_opened = false,
	hospital_comparison_workspace_opened = false,
	outpatient_department_workspace_opened = false;

// Main menu buttons activation
document.querySelectorAll(".main-menu li").forEach((li) => {
	li.addEventListener("click", (_) => {
		document.querySelector(".main-menu li.active").classList.remove("active");
		li.classList.add("active");
		activateSection(li.getAttribute("sec_id"));
		ActivateControlChartGraphMenu();
	});
});

// Activate tools section when click navigate tools button in home section
document.querySelector(".navigate_tools").addEventListener("click", (_) => {
	document.querySelectorAll(".main-menu li").forEach((li) => {
		if (li.getAttribute("sec_id") == "tools_sec") {
			li.click();
		}
	});
});

// Activate tools sections with select tool icon
document.querySelectorAll("#tools_sec .tools_list li").forEach((li) =>
	li.addEventListener("click", (_) => {
		activateSection(li.getAttribute("sec_id"));
		ActivateControlChartGraphMenu();
	})
);

// Activate tools sections with select tool icon from tools menu
document.querySelectorAll(".tools_menu li").forEach((li) => {
	li.addEventListener("click", (_) => {
		document.querySelector(".tools_menu li.active")?.classList.remove("active");
		li.classList.add("active");
		activateSection(li.getAttribute("sec_id"));

		if (
			li.getAttribute("sec_id") == "control_charts_sec" &&
			control_charts_workspace_opened
		) {
			document.querySelector(".control_charts_menu").classList.add("active");
		} else {
			document.querySelector(".control_charts_menu").classList.remove("active");
		}

		if (
			li.getAttribute("sec_id") == "hospital_assessment_sec" &&
			hospital_comparison_workspace_opened
		) {
			document
				.querySelector(".hospital_comparison_menu")
				.classList.add("active");
		} else {
			document
				.querySelector(".hospital_comparison_menu")
				.classList.remove("active");
		}
		if (
			li.getAttribute("sec_id") == "outpatient_dep_sec" &&
			outpatient_department_workspace_opened
		) {
			document
				.querySelector(".outpatient_department_menu")
				.classList.add("active");
		} else {
			document
				.querySelector(".outpatient_department_menu")
				.classList.remove("active");
		}
		// document
		// 	.querySelectorAll(".tls-sec")
		// 	.forEach((tls) =>
		// 		tls.classList.contains("active") ? tls.classList.remove("active") : null
		// 	);
		ActivateControlChartGraphMenu();
	});
});

document
	.querySelector(".header_menu .user_btn")
	.addEventListener("click", (_) => {
		document.querySelector(".header_menu .user_btn").classList.toggle("active");
		document.querySelector(".user-menu").classList.toggle("active");
		ActivateControlChartGraphMenu();
	});

// Activate selected section when click main menu button
function activateSection(sec_id) {
	document.querySelector("section.active").classList.remove("active");
	document.getElementById(sec_id).classList.add("active");

	// Control the tools menu and tools list and their response
	let tools_menu = document.querySelector(".tools_menu");
	// Check if the id is in the the following list to activate the tools menu
	if (
		[
			"outpatient_dep_sec",
			"control_charts_sec",
			"hospital_assessment_sec",
		].includes(sec_id)
	) {
		tools_menu.classList.contains("active")
			? null
			: tools_menu.classList.add("active");
		tools_menu.querySelector("li.active")?.classList.remove("active");

		tools_menu.querySelectorAll("li").forEach((li) => {
			if (li.getAttribute("sec_id") == sec_id) {
				li.classList.add("active");
				if (li.getAttribute("sec_id") == "control_charts_sec") {
					if (control_charts_workspace_opened) {
						document
							.querySelector("#control_charts_sec .workspace_sec")
							.classList.add("active");

						document
							.querySelector(".control_charts_menu")
							.classList.add("active");
					} else {
						document
							.querySelector("#control_charts_sec .upload_file_sec")
							.classList.add("active");
					}
				}
				if (li.getAttribute("sec_id") == "hospital_assessment_sec") {
					if (hospital_comparison_workspace_opened) {
						document
							.querySelector("#hospital_assessment_sec .workspace_sec")
							.classList.add("active");

						document
							.querySelector(".hospital_comparison_menu")
							.classList.add("active");
					} else {
						document
							.querySelector("#hospital_assessment_sec .upload_file_sec")
							.classList.add("active");
					}
				}
				if (li.getAttribute("sec_id") == "outpatient_dep_sec") {
					if (outpatient_department_workspace_opened) {
						document
							.querySelector("#outpatient_dep_sec .workspace_sec")
							.classList.add("active");

						document
							.querySelector(".outpatient_department_menu")
							.classList.add("active");
					} else {
						document
							.querySelector("#outpatient_dep_sec .upload_file_sec")
							.classList.add("active");
					}
				}
			}
		});
	} else {
		tools_menu.classList.remove("active");
		document.querySelector(".control_charts_menu").classList.remove("active");
		document
			.querySelector(".hospital_comparison_menu")
			.classList.remove("active");
		document
			.querySelector(".outpatient_department_menu")
			.classList.remove("active");
	}
	ActivateControlChartGraphMenu();
}

function ActivateControlChartGraphMenu() {
	let control_charts_graph_menu = document.querySelector(
		".control_charts_graph_menu"
	);
	if (
		control_charts_menu.classList.contains("active") &&
		control_charts_menu.querySelector("li.ccw").classList.contains("active") &&
		document.getElementById("graph_02").classList.contains("exist")
	) {
		control_charts_graph_menu.classList.contains("active")
			? null
			: control_charts_graph_menu.classList.add("active");
	} else {
		control_charts_graph_menu.classList.contains("active")
			? control_charts_graph_menu.classList.remove("active")
			: null;

		document.getElementById("graph_02").classList.contains("active")
			? document.getElementById("graph_02").classList.remove("active")
			: null;

		document.getElementById("graph_01").classList.contains("active")
			? null
			: document.getElementById("graph_01").classList.add("active");
	}
	let control_charts_graph_menu_icon_list =
		control_charts_graph_menu.querySelectorAll("li");
	control_charts_graph_menu_icon_list.forEach((li) =>
		li.classList.contains("active") ? li.classList.remove("active") : null
	);
	control_charts_graph_menu_icon_list[0].classList.add("active");
}
