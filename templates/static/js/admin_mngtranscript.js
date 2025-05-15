document.addEventListener("DOMContentLoaded", function () {

    const search_classBtn = document.getElementById("search-class-btn");
    const div_list_module = document.getElementById("list-module");
    const inputbox = document.getElementById("search-module-input");
    const moduleclass_area = document.getElementById("moduleclass-area");
    const student_area = document.getElementById("student-area");
    moduleclass_area.style.display = "block";
    student_area.style.display = "none";


    //nut tim lop
    search_classBtn.addEventListener("click", function () {
        const class_value = document.getElementById("search-class-input").value;
        get_search_class(class_value)
            .then(function (data) {
                table_class(data);
            })
            .catch(function (error) {
                alert(error);
            });
    });


    //tim hoc phan
    const searchbox = document.getElementById("search-module-input");
    searchbox.addEventListener("click", function (event) {
        div_list_module.style.display = "block";
        if (inputbox.classList.contains("inputbox-module")) {
            inputbox.classList.remove("inputbox-module");
            inputbox.classList.add("inputbox-module-clicked");
        }
    });


    searchbox.addEventListener("keyup", function () {
        var value = searchbox.value.toLowerCase();
        var options = div_list_module.getElementsByTagName("option");
        for (var i = 0; i < options.length; i++) {
            var text_option = options[i].textContent.toLowerCase();
            if (text_option.indexOf(value) > -1) {
                options[i].style.display = "";
            }
            else {
                options[i].style.display = "none";
            }
        };
    });


    //nut hien danh sach  sinh vien
    const btn_show_list_std = document.getElementById("btn-show-std");
    const tbody_std = document.getElementById("tbody-std");
    btn_show_list_std.addEventListener("click", function () {
        const idClass = document.getElementById("choosen-class").getAttribute("idClass");
        const idModule = document.getElementById("choosen-module").getAttribute("idModule");
        get_list_std(idClass, idModule)
            .then(function (data) {
                fill_transcript_to_table(tbody_std, data);
            })
            .catch(function (error) {
                alert(error);
            });
    });


    //bang danh sach lop
    const tbody_class = document.getElementById("tb-class");
    blank_table(tbody_class, 4, 4);

    //bang danh sach sinh vien
    blank_table(tbody_std, 10, 10);

    //bang diem cua sinh vien
    const tbody_moduleclass = document.getElementById("tbody-moduleclass");
    blank_table(tbody_moduleclass, 10, 11);

    //nut in bang danh sach theo lop
    const export_table = document.getElementById('btn-print-std');
    export_table.addEventListener('click', function () {
        const idClass = document.getElementById("choosen-class").textContent;
        const idModule = document.getElementById("choosen-module").textContent;
        const name_file = idClass + "_" + idModule;
        const table_export = document.getElementById("tb-list-std");
        var tableInfo = [
            ["Bảng điểm sinh viên"],
            ["Lớp:", idClass],
            ["Học phần:", idModule],
            [],
        ];
        export_to_excel(table_export, name_file, tableInfo);
    });


    //nut in bang diem theo sinh vien
    const export_table_moduleclass = document.getElementById("btn-print-moduleclass");
    export_table_moduleclass.addEventListener("click", function () {
        const nameStd = document.getElementById("nameStd").textContent;
        const idStd = document.getElementById("idStd").textContent;
        const semester_selected  = document.getElementById("select-semester");
        const semester = semester_selected.selectedOptions[0].textContent;
        const name_file = idStd + "_" + nameStd + "_" +semester;
        const table_export = document.getElementById("tb-list-module");
        var tableInfo = [
            ["Bảng điểm sinh viên"],
            ["Họ tên:", nameStd, "MSSV:", idStd],
            ["Học kỳ:", semester],
            [],
        ];
        export_to_excel(table_export, name_file, tableInfo);
    });
        


    //tai len file excel
    const file_input = document.getElementById("input-excel-file");
    const btn_upload = document.getElementById("uploadBtn");
    btn_upload.addEventListener("click", function () {
        const action = "upload";
        upload_excel(file_input, action);
    });


    //luu bang vao CSDL
    const save_btn = document.getElementById("commit-save-data");
    save_btn.addEventListener("click", function () {
        const action = "save";
        upload_excel(file_input, action);
        alert("Lưu bảng điểm thành công");
    });


    //tim kiem theo sinh vien
    const search_std_btn = document.getElementById("search-std-btn");
    search_std_btn.addEventListener("click", function () {
        const idStd = document.getElementById("search-student-input").value;
        get_profile_std(idStd)
            .then(function (data) {
                const profile = data.profile;
                document.getElementById("idStd").textContent = profile.idStd;
                document.getElementById("idStd").setAttribute("idStd", profile.idStd);
                document.getElementById("nameStd").textContent = profile.nameStd;
                document.getElementById("birthStd").textContent = profile.datebirthStd;
                document.getElementById("idClass").textContent = profile.idClass;
                document.getElementById("faculty").textContent = profile.faculty;
                moduleclass_area.style.display = "none";
                student_area.style.display = "block";
                return get_semester_std(idStd);
            })
            .then(function (data) {
                const semester_selectbox = document.getElementById("select-semester");
                semester_selectbox.innerHTML = "<option value='-1' selected>--Học kỳ--</option></option><option value='all'>Tất cả học kỳ</option></option>";
                data.semesters.forEach(function (semester) {
                    const option = document.createElement("option");
                    option.value = semester.idSemester;
                    option.textContent = semester.nameSemester;
                    semester_selectbox.appendChild(option);
                });
            })
            .catch(function (error) {
                alert(error);
            });
    });


    //selectbox hoc ky
    const semester_selectbox = document.getElementById("select-semester");
    semester_selectbox.addEventListener("change", function () {
        const semester = semester_selectbox.value;
        if (semester != -1) {
            const idStd = document.getElementById("idStd").getAttribute("idStd");
            const tbody = document.getElementById("tbody-moduleclass");
            get_transcript_semester(idStd, semester)
                .then(function (data) {
                    fill_transcript_std_to_table(tbody, data);
                    const export_table_moduleclass = document.getElementById("btn-print-moduleclass");
                    export_table_moduleclass.disabled = false;
                })
                .catch(function (error) {
                    alert(error);
                });
        };
    });

    auto_close_tag();
});



















//tim kiem lop hoc phan
function get_search_class(value) {
    return new Promise(function (resolve, reject) {
        $.ajax({
            url: 'get-search-class/' + value + '/',
            method: 'GET',
            dataType: 'json',
            success: function (data) {
                if (data.classes) {
                    resolve(data);
                }
                else {
                    reject("Không có kết quả phù hợp");
                };
            },
            error: function () {

            }
        });
    });
}


//tao bang lop hoc phan
function table_class(data) {
    const tbody_class = document.getElementById("tb-class");
    tbody_class.innerHTML = "";
    const table_class = document.getElementById("table-class");
    table_class.style.display = "block";
    data.classes.forEach(function (classe) {

        const tr = document.createElement("tr");

        const cell1 = document.createElement("td");
        cell1.textContent = classe.idClass;
        tr.appendChild(cell1);

        const cell2 = document.createElement("td");
        cell2.textContent = classe.faculty;
        tr.appendChild(cell2);

        const cell3 = document.createElement("td");
        cell3.textContent = classe.department;
        tr.appendChild(cell3);

        const cell4 = document.createElement("td");
        cell4.textContent = classe.idCourse;
        tr.appendChild(cell4);

        tr.setAttribute("idClass", classe.idClass);

        tbody_class.appendChild(tr);

        tr.addEventListener("click", function (event) {
            const idClass = tr.getAttribute("idClass");
            const show_idClass = document.getElementById("choosen-class");
            show_idClass.textContent = idClass;
            show_idClass.setAttribute("idClass", idClass);
            choosen_row(event, tbody_class);
            get_list_module(idClass)
                .then(function (data) {
                    selectbox_module(data);
                });
        });
    });
}


//lay thong tin ve mon hoc thuoc lop
function get_list_module(idClass) {
    return new Promise(function (resolve, reject) {
        $.ajax({
            url: 'get-list-module/' + idClass + '/',
            method: 'GET',
            dataType: 'json',
            success: function (data) {
                resolve(data);
            },
            error: function () {
                reject();
            }
        });
    });
}


//tao list search mon hoc
function selectbox_module(data) {
    const moduleclass_area = document.getElementById("moduleclass-area");
    const student_area = document.getElementById("student-area");
    const div_options = document.getElementById("list-module");
    div_options.innerHTML = "";
    data.modules.forEach(function (module) {
        const option = document.createElement("option");
        option.value = module.idModule;
        option.textContent = module.idModule + " - " + module.nameModule;
        option.classList.add("option-moduleclass");
        div_options.appendChild(option);

        option.addEventListener("click", function () {
            moduleclass_area.style.display = "block";
            student_area.style.display = "none";
            
            const show_module = document.getElementById("choosen-module");
            show_module.textContent = option.textContent;
            show_module.setAttribute("idModule", option.value);
            div_options.style.display = "none";
            const inputbox = document.getElementById("search-module-input");
            inputbox.value = option.textContent;
            if (inputbox.classList.contains("inputbox-module-clicked")) {
                inputbox.classList.remove("inputbox-module-clicked");
                inputbox.classList.add("inputbox-module");
            }
        });
    });
}


//dong the khi khong tuong tac
function auto_close_tag() {
    const div_list_module = document.getElementById("list-module");
    const inputbox = document.getElementById("search-module-input");
    document.addEventListener('click', function (event) {
        if (!inputbox.contains(event.target) && !div_list_module.contains(event.target)) {
            div_list_module.style.display = 'none';
            if (inputbox.classList.contains("inputbox-module-clicked")) {
                inputbox.classList.remove("inputbox-module-clicked");
                inputbox.classList.add("inputbox-module");
            }
        }
    });
}



//ham highlight dong trong bang
function choosen_row(event, tbody) {
    const rows = tbody.getElementsByTagName("tr");
    for (let i = 0; i < rows.length; i++) {
        rows[i].classList.remove("clicked-row");
    }
    const selectRow = event.currentTarget;
    selectRow.classList.add("clicked-row");
}


//tao bang trong
function blank_table(tbody, number_row, number_cell) {
    for (let i = 0; i < number_row; i++) {
        const row = document.createElement("tr");
        for (let i = 0; i < number_cell; i++) {
            const cell = document.createElement("td");
            row.appendChild(cell);
        };
        tbody.appendChild(row);
    }
}


//lay du lieu ve danh sach sinh vien thuoc lop
function get_list_std(idClass, idModule) {
    return new Promise(function (resolve, reject) {
        $.ajax({
            url: 'get-list-std/' + idClass + '/' + idModule + '/',
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

//ham dien thong tin sinh vien vao bang lay tu sever
function fill_transcript_to_table(tbody, data) {
    tbody.innerHTML = "";
    data.transcripts.forEach(function (transcript) {
        const row = document.createElement("tr");

        const cell1 = document.createElement("td");
        row.appendChild(cell1);

        const cell2 = document.createElement("td");
        cell2.textContent = transcript.idStd;
        row.appendChild(cell2);

        const cell3 = document.createElement("td");
        cell3.textContent = transcript.nameStd;
        row.appendChild(cell3);

        const cell4 = document.createElement("td");
        cell4.textContent = transcript.date_birth;
        row.appendChild(cell4);

        const cell5 = document.createElement("td");
        cell5.textContent = transcript.process_grade;
        row.appendChild(cell5);

        const cell6 = document.createElement("td");
        cell6.textContent = transcript.final_grade;
        row.appendChild(cell6);

        const cell7 = document.createElement("td");
        cell7.textContent = transcript.overall_grade;
        row.appendChild(cell7);

        const cell8 = document.createElement("td");
        cell8.textContent = transcript.overall_grade_4;
        row.appendChild(cell8);

        const cell9 = document.createElement("td");
        cell9.textContent = transcript.overall_grade_text;
        row.appendChild(cell9);

        const cell10 = document.createElement("td");
        cell10.textContent = transcript.is_pass;
        row.appendChild(cell10);

        tbody.appendChild(row);
    });
    auto_number(tbody);
}



//ham dien bang diem cua sinh vien theo ky vao bang
function fill_transcript_std_to_table(tbody, data) {
    tbody.innerHTML = "";
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
        row.appendChild(cell11)
        tbody.appendChild(row);
    });
    auto_number(tbody);
}


//ham auto danh so thu tu
function auto_number(tbody) {
    const rows = tbody.querySelectorAll("tr");
    index = 0;
    rows.forEach(function (row) {
        const numberCell = row.querySelector("td:first-child");
        numberCell.textContent = index + 1;
        index += 1;
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
    XLSX.utils.book_append_sheet(wb, ws, "sheet 1");
    var wbout = XLSX.write(wb, { bookType: "xlsx", type: "array" });
    var blob = new Blob([wbout], { type: "application/octet-stream" });
    var url = URL.createObjectURL(blob);
    var a = document.createElement('a');
    a.href = url;
    a.download = name_file + ".xlsx";
    a.click();

    URL.revokeObjectURL(url);

}


//gui excel toi views
function upload_excel_to_view(formData, idClass, idModule, action) {
    return new Promise(function (resolve, reject) {
        const csrfToken = getCSRFToken();
        $.ajax({
            url: 'upload-file-excel/' + idClass + '/' + idModule + '/' + action + '/',
            method: 'POST',
            dataType: 'json',
            data: formData,
            processData: false,
            contentType: false,
            headers: {
                'X-CSRFToken': csrfToken
            },
            success: function (data) {
                if (data.transcripts) {
                    resolve(data)
                }
                else {
                    reject(data.error);
                }
            },
            error: function (data) {
                alert("Có lỗi trong quá trình xử lý");
            },
        });
    });
}



//upload excel + action
function upload_excel(file_input, action) {
    const idClass = document.getElementById("choosen-class").getAttribute("idClass");
    const idModule = document.getElementById("choosen-module").getAttribute("idModule");
    const tbody_std = document.getElementById("tbody-std");
    file = file_input.files[0];
    if (file) {
        const formData = new FormData();
        formData.append("excel_file", file);
        upload_excel_to_view(formData, idClass, idModule, action)
            .then(function (data) {
                fill_transcript_to_table(tbody_std, data);
                const save_btn = document.getElementById("commit-save-data");
                save_btn.disabled = false;
            })
            .catch(function (error) {
                alert(error);
                location.reload();
            });
    }
    else {
        alert("Hãy chọn file cần tải lên trước");
    };
}



//lay danh thong tin sinh vien
function get_profile_std(idStd) {
    return new Promise(function (resolve, reject) {
        $.ajax({
            url: 'get-profile-std/' + idStd + '/',
            method: 'get',
            dataType: 'json',
            success: function (data) {
                if (data.profile) {
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


//lay bang diem sau theo   ky hoc
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


//token
function getCSRFToken() {
    const cookies = document.cookie.split('; ');
    for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].split('=');
        if (cookie[0] === 'csrftoken') {
            return cookie[1];
        }
    }
    return null;
}