document.addEventListener("DOMContentLoaded", function(){
    //tao selectbox hoc ky
  get_semester_std()
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
    const tbody = document.getElementById("tbody-tuitionfee");
    const semester_selectbox = document.getElementById("select-semester");
    semester_selectbox.addEventListener("change", function () {
        const semester = semester_selectbox.value;
        tbody.innerHTML = "";
        if(semester == "all"){
            get_tuitionfee()
            .then(function (data) {
                data.semester_tuitionfees.forEach(function(semester_tuitionfee) {
                    fill_data_to_table(tbody, semester_tuitionfee);
                });
            });
        }
        else{
            get_tuitionfee()
            .then(function (data) {
                data.semester_tuitionfees.forEach(function(semester_tuitionfee) {
                    const idSemester = semester_tuitionfee.idSemester;
                    if(idSemester == semester) {
                    fill_data_to_table(tbody, semester_tuitionfee);
                    };
                });
            });
        };
    });



     //nut in bang diem theo sinh vien
    const export_table_moduleclass = document.getElementById("btn-print-tuitionfee");
    export_table_moduleclass.addEventListener("click", function () {
        const nameStd = document.getElementById("idStd").getAttribute("nameStd");
        const idStd = document.getElementById("idStd").getAttribute("idStd");
        const semester_selected = document.getElementById("select-semester");
        const semester = semester_selected.selectedOptions[0].textContent;
        const name_file = idStd + "_" + nameStd + "_" + semester;
        const table_export = document.getElementById("tb-list-module");
        var tableInfo = [
        ["Học phí sinh viên"],
        ["Họ tên:", nameStd, "MSSV:", idStd],
        ["Học kỳ:", semester],
        [],
        ];
        export_to_excel(table_export, name_file, tableInfo);
    });


        


});



//lay du lieu ve hoc phi
function get_tuitionfee() {
    return new Promise(function (resolve, reject) {
        $.ajax({
            url: 'get_tuitionfee/',
            method: 'GET',
            dataType: 'json',
            success: function (data) {
                resolve(data);
            },
            error: function (){
                alert("Có lỗi trong quá trình xử lý");
            }
        }); 
    });
}


//dien du lieu vao bang
function fill_data_to_table(tbody, data) {
    const semester = data.semester;
    const moduleclasses = data.moduleclasses;
    const tuitionfee = data.tuitionfee;
    const tuitionfee_scale = data.tuitionfee_scale;

    const row_title = document.createElement("tr");
    const td_colspan = document.createElement("td");
    td_colspan.colSpan = 8;
    td_colspan.textContent = semester;
    row_title.appendChild(td_colspan);
    row_title.classList.add("name-semester-row", "not-data");
    tbody.appendChild(row_title);
    moduleclasses.forEach(function (moduleclass) {
        const row = document.createElement("tr");

        const cell1 = document.createElement("td");
        row.appendChild(cell1);
    
        const cell2 = document.createElement("td");
        cell2.textContent = moduleclass.idModule;
        row.appendChild(cell2);
    
        const cell3 = document.createElement("td");
        cell3.textContent = moduleclass.nameModule;
        row.appendChild(cell3);
    
        const cell4 = document.createElement("td");
        cell4.textContent = moduleclass.idClass;
        row.appendChild(cell4);
    
        const cell5 = document.createElement("td");
        cell5.textContent = moduleclass.credit;
        row.appendChild(cell5)
    
        const cell6 = document.createElement("td");
        cell6.textContent = (moduleclass.credit * tuitionfee_scale).toLocaleString();
        row.appendChild(cell6); 

        const cell7 = document.createElement("td");
        cell7.textContent = "";
        row.appendChild(cell7);

        const cell8 = document.createElement("td");
        cell8.textContent = "";
        row.appendChild(cell8);

        tbody.appendChild(row);
    });
    const row = document.createElement("tr");

    const cell1 = document.createElement("td");
    row.appendChild(cell1);

    const cell2 = document.createElement("td");
    cell2.textContent = "";
    row.appendChild(cell2);

    const cell3 = document.createElement("td");
    cell3.textContent = "";
    row.appendChild(cell3);

    const cell4 = document.createElement("td");
    cell4.textContent = "";
    row.appendChild(cell4);

    const cell5 = document.createElement("td");
    cell5.textContent = tuitionfee.totalcredit;
    row.appendChild(cell5)

    const cell6 = document.createElement("td");
    cell6.textContent = addCommasToNumberString(tuitionfee.total_tuitionfee);
    row.appendChild(cell6); 

    const cell7 = document.createElement("td");
    cell7.textContent = addCommasToNumberString(tuitionfee.paid_tuitionfee);
    row.appendChild(cell7);

    const cell8 = document.createElement("td");
    cell8.textContent = addCommasToNumberString(tuitionfee.unpaid_tuitionfee);
    row.appendChild(cell8);

    row.classList.add("not-data");

    tbody.appendChild(row);
    
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


function addCommasToNumberString(numberString) {
    const number = parseInt(numberString, 10);
    const formattedNumberString = number.toLocaleString();
    return formattedNumberString;
}


//lay danh sach ky cua sinh vien
function get_semester_std() {
    return new Promise(function (resolve, reject) {
      $.ajax({
        url: 'get-semester-std/',
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