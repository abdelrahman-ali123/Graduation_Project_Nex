let hospitals_comparison_uploaded_file = document.getElementById(
		"hospital_comparison_file"
	),
	hospitals_comparison_uploaded_file_card = document.querySelector(
		"#hospital_assessment_sec .upload_file_sec .uploaded_file"
	),
	hospitals_comparison_file_submit_btn = document.querySelector(
		"#hospital_assessment_sec .upload_file_sec .submit_file"
	),
	hospitals_comparison_files_holder = document.querySelector(
		"#hospital_assessment_sec .upload_file_sec .upload_side .files_holder"
	),
	hospital_comparison_menu = document.querySelector(
		".hospital_comparison_menu"
	);

let hospitals_comparison_data_ret = {
	from_example: false,
	file_num: 0,
	file_input_data: "",
	file_name: "",
};

document
	.querySelector(
		"#hospital_assessment_sec .upload_file_sec .upload_side .browse_files_btn"
	)
	.addEventListener("click", (_) => hospitals_comparison_uploaded_file.click());

// Show files holder
document
	.querySelector(
		"#hospital_assessment_sec .upload_file_sec .upload_side .show_more_files"
	)
	.addEventListener("click", (_) => {
		hospitals_comparison_files_holder.classList.add("active");
	});

// Remove files holder
hospitals_comparison_files_holder
	.querySelector(".remove_files_holder")
	.addEventListener("click", (_) =>
		hospitals_comparison_files_holder.classList.remove("active")
	);

hospitals_comparison_uploaded_file.addEventListener("input", (e) => {
	if (e.target.value != "") {
		let file_info = e.target.files[0],
			name = file_info.name.split(".")[0];

		if (
			file_info.type !=
			"application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
		) {
			alert("Please upload only xlsx files only!");
			hospitals_comparison_uploaded_file_card.classList.remove("active");
			hospitals_comparison_file_submit_btn.classList.add("inactive");
			return;
		}

		let reader = new FileReader();
		reader.onload = (_) => {
			let url = reader.result;
			file_content = url;
			hospitals_comparison_data_ret.file_input_data = url;
			hospitals_comparison_data_ret.file_num = 0;
			hospitals_comparison_data_ret.from_example = false;
			hospitals_comparison_data_ret.file_name = name;
			hospitals_comparison_files_holder
				.querySelector(".files ul li.selected")
				?.classList.remove("selected");
			if (hospital_comparison_workspace_opened) {
				ApplyHospitalComparison(hospitals_comparison_data_ret);
			} else {
				ActivateHospitalComparisonFileCard(name, file_info.size);
			}
			e.target.value = "";
		};

		reader.readAsDataURL(file_info);
	}
});

hospitals_comparison_uploaded_file_card
	.querySelector(".delete_file")
	.addEventListener("click", (_) => {
		hospitals_comparison_uploaded_file.value = "";
		hospitals_comparison_uploaded_file_card.classList.remove("active");
		hospitals_comparison_uploaded_file_card.classList.remove("active");
		hospitals_comparison_file_submit_btn.classList.add("inactive");
		hospitals_comparison_files_holder
			.querySelector(".files ul li.selected")
			?.classList.remove("selected");

		hospitals_comparison_data_ret.file_input_data = "";
		hospitals_comparison_data_ret.file_num = 0;
		hospitals_comparison_data_ret.from_example = false;
		hospitals_comparison_data_ret.file_name = "";
	});

hospitals_comparison_uploaded_file_card
	.querySelector(".delete_file")
	.addEventListener("mouseover", (e) =>
		e.target.parentNode.classList.add("hover")
	);

hospitals_comparison_uploaded_file_card
	.querySelector(".delete_file")
	.addEventListener("mouseout", (e) =>
		e.target.parentNode.classList.remove("hover")
	);

// Choose file from example files
hospitals_comparison_files_holder.querySelectorAll(".files li").forEach((li) =>
	li.addEventListener("click", (_) => {
		hospitals_comparison_files_holder
			.querySelector(".files ul li.selected")
			?.classList.remove("selected");
		li.classList.add("selected");
		let name_size_cont = li.querySelector(".name-size");
		ActivateHospitalComparisonFileCard(
			name_size_cont.getAttribute("title"),
			parseFloat(name_size_cont.querySelector("i").innerText) * 1024
		);

		hospitals_comparison_data_ret.file_input_data = "";
		hospitals_comparison_data_ret.file_num = parseInt(
			li.getAttribute("file_num")
		);
		hospitals_comparison_data_ret.from_example = true;
		hospitals_comparison_data_ret.file_name =
			name_size_cont.getAttribute("title");
	})
);

// Inactivate workspace section
hospital_comparison_menu
	.querySelector(".close_hospital_comparison_workspace")
	.addEventListener("click", (_) => {
		// Activate upload section
		document
			.querySelector("#hospital_assessment_sec .upload_file_sec")
			.classList.add("active");

		// Inactivate workspace section
		document
			.querySelector("#hospital_assessment_sec .workspace_sec")
			.classList.remove("active");

		// Inactivate control chart menu
		hospital_comparison_menu.classList.remove("active");
		hospital_comparison_workspace_opened = false;
	});

//
hospital_comparison_menu
	.querySelectorAll(".hospitals_comparison_icons li")
	.forEach((li) => {
		li.addEventListener("click", (_) => {
			hospital_comparison_menu
				.querySelector(".hospitals_comparison_icons li.active")
				.classList.remove("active");
			li.classList.add("active");
			ActivateHospitalComparisonSections(li.getAttribute("sec_type"));
			// ActivateControlChartGraphMenu();
			// console.log(li.getAttribute("sec_type"));
		});
	});

hospital_comparison_menu
	.querySelector(".upload_hospital_comparison_file")
	.addEventListener("click", (_) => hospitals_comparison_uploaded_file.click());

hospitals_comparison_file_submit_btn.addEventListener("click", (_) => {
	ApplyHospitalComparison(hospitals_comparison_data_ret);
});

function ActivateHospitalComparisonFileCard(name, size) {
	hospitals_comparison_uploaded_file_card.querySelector(
		".name-size"
	).innerHTML = `${
		name.length > 20 ? `${name.substring(0, 20)}...` : name
	}<i>${(size / 1024).toFixed(2)} kb</i>`;

	hospitals_comparison_uploaded_file_card
		.querySelector(".name-size")
		.setAttribute("title", name);

	hospitals_comparison_uploaded_file_card.classList.add("active");

	hospitals_comparison_file_submit_btn.classList.remove("inactive");
}

// Activate control charts secitons (charts and analysis summary)
function ActivateHospitalComparisonSections(sec_type) {
	document
		.querySelector("#hospital_assessment_sec .wrk-sections.active")
		.classList.remove("active");
	document.getElementById(sec_type).classList.add("active");
}

function ApplyHospitalComparison(hospitals_comparison_data_ret) {
	// Send data to server to apply control charts on in
	let loader = document.querySelector(".loader");
	loader.classList.add("active");
	fetch(`${window.origin}/apply_hospitals_comparison`, {
		method: "POST",
		credentials: "include",
		body: JSON.stringify(hospitals_comparison_data_ret),
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

			if (!hospital_comparison_workspace_opened) {
				// Inactivate upload section
				document
					.querySelector("#hospital_assessment_sec .upload_file_sec")
					.classList.remove("active");

				// Activate workspace section
				document
					.querySelector("#hospital_assessment_sec .workspace_sec")
					.classList.add("active");

				// Activate hospital comparison menu
				hospital_comparison_menu.classList.add("active");

				hospital_comparison_workspace_opened = true;
			}

			HandleHospitalComparisonData(data);
			return;
		});
	});
}

function HandleHospitalComparisonData(result) {
	// console.log(result);
	let result_data = result.result,
		sum_cont = document.querySelector(
			"#hospital_assessment_sec .workspace_sec #hospital_comparison_summary_window .cnt"
		),
		hospital_detailes = document.querySelector(
			"#hospital_assessment_sec .hospital_detailes"
		);

	sum_cont.innerHTML = result_data.analysis_summary;
	hospital_detailes.querySelector("h2").innerText = "";
	hospital_detailes.querySelector(".hos_data_cont").innerHTML = "";
	document.querySelector(
		"#hospital_assessment_sec .hospitals_header .hos_nums"
	).innerText = result_data.combined_methods.length;
	document.querySelector(
		"#hospital_assessment_sec .hospitals_header .inef_hos_nums"
	).innerText = result_data.ineff_ent.length;
	AddHospitalsCardToContainer(result_data.combined_methods);

	document
		.querySelectorAll(
			"#hospital_assessment_sec .hospitals_container ul li.hospital_card .show_more_detailes_btn"
		)
		.forEach((li) =>
			li.addEventListener("click", (_) =>
				GetHospitalData(
					li.getAttribute("hosp_name"),
					result_data.det_data,
					result_data.combined_methods
				)
			)
		);
}

function AddHospitalsCardToContainer(hospital_list) {
	let hospitals_cont = document.querySelector(
		"#hospital_assessment_sec .hospitals_container ul"
	);
	hospitals_cont.innerHTML = "";
	for (let i = 0; i < hospital_list.length; i++) {
		let hospital = hospital_list[i];
		hospitals_cont.innerHTML += `<li class="hospital_card ${hospital.stat}">
								<span class="num">${i + 1}</span>
								<p class="name-det">
									<span class="name">${hospital.type}</span>
									<span
										><i>Mean: ${hospital.mean}</i>, <i>Standard deviation: ${hospital.std}</i>,
										<i>E: ${hospital.E}</i></span
									>
								</p>
								<span
									class="show_more_detailes_btn material-symbols-outlined"
									hosp_name="${hospital.type}"
									title="Show more detailes">
									quick_reference
								</span>
							</li>`;
	}
}

function GetHospitalData(hospital_name, hospitals_data, norm_dea_data) {
	let ip = hospitals_data[0],
		op = hospitals_data[1];

	let hospital_detailes = document.querySelector(
		"#hospital_assessment_sec .hospital_detailes"
	);
	hospital_detailes.querySelector("h2").innerText = hospital_name;
	hospital_detailes.querySelector(".hos_data_cont").innerText = "";
	norm_dea_data.forEach((ent) =>
		ent.type == hospital_name
			? (hospital_detailes.querySelector(
					".hos_data_cont"
			  ).innerHTML += `<h3>Data Envelopment Analysis (DEA)</h3>
								<p>
									<span class="material-symbols-outlined">
										arrow_forward_ios </span
									><span
										>Fraction of the hospitals's input available to the group
										composit hospital (E)</span
									>
									<span>${ent.E}</span>
								</p>
								<h3>Normalized statistics</h3>
								<p>
									<span class="material-symbols-outlined">
										arrow_forward_ios </span
									><span>Mean</span> <span>${ent.mean}</span>
								</p>
								<p>
									<span class="material-symbols-outlined">
										arrow_forward_ios </span
									><span>Standard deviation</span> <span>${ent.std}</span>
								</p>`)
			: null
	);
	hospital_detailes.querySelector(".hos_data_cont").innerHTML +=
		"<h3>Inputs</h3>";
	for (let i = 0; i < ip[hospital_name].length; i++)
		hospital_detailes.querySelector(".hos_data_cont").innerHTML += `<p>
									<span class="material-symbols-outlined">
										arrow_forward_ios </span
									><span>${ip.attributes[i]}</span> <span>${ip[hospital_name][i]}</span>
								</p>`;

	hospital_detailes.querySelector(".hos_data_cont").innerHTML +=
		"<h3>Outputs</h3>";

	for (let i = 0; i < op[hospital_name].length; i++)
		hospital_detailes.querySelector(".hos_data_cont").innerHTML += `<p>
									<span class="material-symbols-outlined">
										arrow_forward_ios </span
									><span>${op.attributes[i]}</span> <span>${op[hospital_name][i]}</span>
								</p>`;
}
