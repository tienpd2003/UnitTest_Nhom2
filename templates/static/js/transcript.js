document.addEventListener("DOMContentLoaded", function () {

  const idStd = document.getElementById("idStd").getAttribute("idStd");


  //tao selectbox hoc ky
  get_semester_std(idStd)
    .then(function (data) {
      const semester_selectbox = document.getElementById("select-semester");
      semester_selectbox.innerHTML = "<option value='all' selected>Tất cả học kỳ</option>";
      data.semesters.forEach(function (semester) {
        const option = document.createElement("option");
        option.value = semester.idSemester;
        option.textContent = semester.nameSemester;
        semester_selectbox.appendChild(option);
      });
      var event = new Event("change");
      semester_selectbox.dispatchEvent(event);
    })
    .catch(function (error) {
      alert(error);
    });




  //selectbox hoc ky
  const semester_selectbox = document.getElementById("select-semester");
  semester_selectbox.addEventListener("change", function () {
    const semester = semester_selectbox.value;
    const idStd = document.getElementById("idStd").getAttribute("idStd");
    const tbody = document.getElementById("tbody-moduleclass");
    tbody.innerHTML = "";
    if (semester != -1) {
      get_transcript_semester(idStd, semester)
        .then(function (data) {
          if (semester == "all") {
            for (var i = 0; i < data.transcripts.length; i++) {
              var transcript = data.transcripts[i];
              var overall = {};
              if (data.overall[i] && data.overall[i].overall) {
                overall = data.overall[i].overall;
              }
              else {
                overall = {
                  average_semester_10: "",
                  average_semester_4: "",
                  average_10: "",
                  average_4: "",
                  all_credits: "",
                  collected_credits: "",
                  passed_credits: "",
                  owe_credits: "",
                };
              };
              const nameSemester = transcript.semester;
              fill_transcript_std_to_table(tbody, nameSemester, transcript, overall);
            };
          }
          else {
            const nameSemester = semester_selectbox.selectedOptions[0].textContent;

            if (data.overall) {
              overall = {
                average_semester_10: data.overall.average_10,
                average_semester_4: data.overall.average_4,
                average_10: "",
                average_4: "",
                all_credits: data.overall.all_credits,
                collected_credits: "",
                passed_credits: data.overall.credits_pass,
                owe_credits: data.overall.owe_credits,
              };
            }
            else {
              overall = {
                average_semester_10: "",
                average_semester_4: "",
                average_10: "",
                average_4: "",
                all_credits: "",
                collected_credits: "",
                passed_credits: "",
                owe_credits: "",
              };
            };
            fill_transcript_std_to_table(tbody, nameSemester, data, overall);

          };
        })
        .catch(function (error) {
          alert(error);
        });
    };
  });




  //nut in bang diem theo sinh vien
  const export_table_moduleclass = document.getElementById("btn-print-transcript");
  export_table_moduleclass.addEventListener("click", function () {
    const nameStd = document.getElementById("idStd").getAttribute("nameStd");
    const idStd = document.getElementById("idStd").getAttribute("idStd");
    const semester_selected = document.getElementById("select-semester");
    const semester = semester_selected.selectedOptions[0].textContent;
    const name_file = idStd + "_" + nameStd + "_" + semester;
    const table_export = document.getElementById("tb-list-module");
    var tableInfo = [
      ["Bảng điểm sinh viên"],
      ["Họ tên:", nameStd, "MSSV:", idStd],
      ["Học kỳ:", semester],
      [],
    ];
    export_to_excel(table_export, name_file, tableInfo);
  });





});








//lay danh sach ky cua sinh vien
function get_semester_std(idStd) {
  return new Promise(function (resolve, reject) {
    $.ajax({
      url: 'get-semester-std/' + idStd + '/',
      method: 'get',
      dataType: 'json',
      success: function (data) {
        if (data.semesters) {
          resolve(data);
        }
        else {
          reject(data.error);
        }
      },
      error: function () {
        alert("Có lỗi trong quá trình xử lý");
      }
    });
  });
}


//lay bang diem theo   ky hoc
function get_transcript_semester(idStd, semester) {
  return new Promise(function (resolve, reject) {
    $.ajax({
      url: 'get-transcript-semester/' + idStd + '/' + semester + '/',
      method: 'GET',
      dataType: 'json',
      success: function (data) {
        if (data.transcripts) {
          resolve(data);
        }
        else {
          reject(data.error);
        }
      },
      error: function () {
        alert("Có lỗi trong quá trình xử lý");
      }
    });
  });
}



//ham dien bang diem cua sinh vien theo ky vao bang
function fill_transcript_std_to_table(tbody, nameSemester, data, overall) {
  const row_title = document.createElement("tr");
  const td_colspan = document.createElement("td");
  td_colspan.colSpan = 11;
  td_colspan.textContent = nameSemester;
  row_title.appendChild(td_colspan);
  row_title.classList.add("name-semester-row", "not-data");
  tbody.appendChild(row_title);
  data.transcripts.forEach(function (transcript) {
    const row = document.createElement("tr");

    const cell1 = document.createElement("td");
    row.appendChild(cell1);

    const cell2 = document.createElement("td");
    cell2.textContent = transcript.idModule;
    row.appendChild(cell2);

    const cell3 = document.createElement("td");
    cell3.textContent = transcript.nameModule;
    row.appendChild(cell3);

    const cell4 = document.createElement("td");
    cell4.textContent = transcript.moduleclass;
    row.appendChild(cell4);

    const cell5 = document.createElement("td");
    cell5.textContent = transcript.credit;
    row.appendChild(cell5)

    const cell6 = document.createElement("td");
    cell6.textContent = transcript.process_grade;
    row.appendChild(cell6);

    const cell7 = document.createElement("td");
    cell7.textContent = transcript.final_grade;
    row.appendChild(cell7);

    const cell8 = document.createElement("td");
    cell8.textContent = transcript.overall_grade;
    row.appendChild(cell8);

    const cell9 = document.createElement("td");
    cell9.textContent = transcript.overall_grade_4;
    row.appendChild(cell9);

    const cell10 = document.createElement("td");
    cell10.textContent = transcript.overall_grade_text;
    row.appendChild(cell10);

    const cell11 = document.createElement("td");
    cell11.textContent = transcript.is_pass;
    row.appendChild(cell11);

    tbody.appendChild(row);
  });


  const td_sub1 = document.createElement('td');
  td_sub1.colSpan = 5;
  td_sub1.classList.add("average-transcript");
  const row1 = document.createElement("tr");
  const td1 = document.createElement("td");
  td1.colSpan = 6;
  td1.textContent = "Điểm trung bình học kỳ hệ 10: " + overall.average_semester_10;
  td1.classList.add("average-transcript");
  row1.appendChild(td1);
  row1.appendChild(td_sub1);
  row1.classList.add("not-data");
  tbody.appendChild(row1);

  const td_sub2 = document.createElement('td');
  td_sub2.colSpan = 5;
  td_sub2.classList.add("average-transcript");
  const row2 = document.createElement("tr");
  const td2 = document.createElement("td");
  td2.colSpan = 6;
  td2.textContent = "Điểm trung bình học kỳ hệ 4: " + overall.average_semester_4;
  td2.classList.add("average-transcript");
  row2.appendChild(td2);
  row2.appendChild(td_sub2);
  row2.classList.add("not-data");
  tbody.appendChild(row2);

  const row3 = document.createElement("tr");
  const td3 = document.createElement("td");
  td3.colSpan = 6;
  td3.textContent = "Điểm trung bình tích lũy: " + overall.average_10;
  td3.classList.add("average-transcript");
  row3.appendChild(td3);
  const td_sub3 = document.createElement('td');
  td_sub3.colSpan = 5;
  td_sub3.classList.add("average-transcript");
  row3.appendChild(td_sub3);
  row3.classList.add("not-data");
  tbody.appendChild(row3);

  const row4 = document.createElement("tr");
  const td4 = document.createElement("td");
  td4.colSpan = 6;
  td4.textContent = "Điểm trung bình tích lũy (hệ 4): " + overall.average_4;
  td4.classList.add("average-transcript");
  row4.appendChild(td4);
  const td_sub4 = document.createElement('td');
  td_sub4.colSpan = 5;
  td_sub4.classList.add("average-transcript");
  row4.appendChild(td_sub4);
  row4.classList.add("not-data");
  tbody.appendChild(row4);

  const row5 = document.createElement("tr");
  const td5 = document.createElement("td");
  td5.colSpan = 6;
  td5.textContent = "Tổng số tín chỉ đã đăng ký: " + overall.all_credits;
  td5.classList.add("average-transcript");
  row5.appendChild(td5);
  const td_sub5 = document.createElement('td');
  td_sub5.colSpan = 5;
  td_sub5.classList.add("average-transcript");
  row5.appendChild(td_sub5);
  row5.classList.add("not-data");
  tbody.appendChild(row5);

  const row6 = document.createElement("tr");
  const td6 = document.createElement("td");
  td6.colSpan = 6;
  td6.textContent = "Tổng số tín chỉ tích lũy: " + overall.collected_credits;
  td6.classList.add("average-transcript");
  row6.appendChild(td6);
  const td_sub6 = document.createElement('td');
  td_sub6.colSpan = 5;
  td_sub6.classList.add("average-transcript");
  row6.appendChild(td_sub6);
  row6.classList.add("not-data");
  tbody.appendChild(row6);

  const row7 = document.createElement("tr");
  const td7 = document.createElement("td");
  td7.colSpan = 6;
  td7.textContent = "Tổng số tín chỉ đạt: " + overall.passed_credits;
  td7.classList.add("average-transcript");
  row7.appendChild(td7);
  const td_sub7 = document.createElement('td');
  td_sub7.colSpan = 5;
  td_sub7.classList.add("average-transcript");
  row7.appendChild(td_sub7);
  row7.classList.add("not-data");
  tbody.appendChild(row7);

  const row8 = document.createElement("tr");
  const td8 = document.createElement("td");
  td8.colSpan = 6;
  td8.textContent = "Tổng số tín chỉ nợ tính đến hiện tại: " + overall.owe_credits;
  td8.classList.add("average-transcript");
  row8.appendChild(td8);
  const td_sub8 = document.createElement('td');
  td_sub8.colSpan = 5;
  td_sub8.classList.add("average-transcript");
  row8.appendChild(td_sub8);
  row8.classList.add("not-data");
  tbody.appendChild(row8);


  auto_number(tbody);
}


//ham auto danh so thu tu
function auto_number(tbody) {
  const rows = tbody.querySelectorAll("tr");
  index = 0;
  rows.forEach(function (row) {
    if (!row.classList.contains("not-data")) {
      const numberCell = row.querySelector("td:first-child");
      numberCell.textContent = index + 1;
      index += 1;
    };
  });
}




//xuat ra file excel
function export_to_excel(table, name_file, tableInfo) {

  for (var i = 0; i < table.rows.length; i++) {
    var rowData = [];
    for (var j = 0; j < table.rows[i].cells.length; j++) {
      rowData.push(table.rows[i].cells[j].textContent);
    }
    tableInfo.push(rowData);
  }
  var wb = XLSX.utils.book_new();
  var ws = XLSX.utils.aoa_to_sheet(tableInfo);
  XLSX.utils.book_append_sheet(wb, ws, "Table Data");
  var wbout = XLSX.write(wb, { bookType: "xlsx", type: "array" });
  var blob = new Blob([wbout], { type: "application/octet-stream" });
  var url = URL.createObjectURL(blob);
  var a = document.createElement('a');
  a.href = url;
  a.download = name_file + ".xlsx";
  a.click();

  URL.revokeObjectURL(url);

}