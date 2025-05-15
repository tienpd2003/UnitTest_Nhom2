document.addEventListener("DOMContentLoaded", function () {


    const idStd = document.getElementById("idStd").getAttribute("idStd");

    //du lieu mac dinh khi mo trang
    get_moduleclass(idStd)
        .then(function (data) {
            data.moduleclasses.forEach(function (moduleclass) {
                const this_idModuleClass = moduleclass.idModuleClass;
                get_detail_schedule(this_idModuleClass)
                    .then(function (data) {
                        const schedule = data.schedule;
                        table_info_moduleclass(moduleclass, schedule);
                    })
                    .catch(function () {
                        alert("Lỗi khi lấy dữ liệu thời khóa biểu");
                    });
            });
        })
        .catch(function () {
            alert("Lỗi khi lấy dữ liệu lớp học phần");
        });


    //nut hoc phan theo tien do
    const btnProcess = document.getElementById('btn-process');
    let isButtonLocked = false;
    btnProcess.addEventListener('click', function () {
        if (!isButtonLocked) {
            isButtonLocked = true;
            document.getElementById("moduleclass").innerHTML = "";

            get_moduleclass(idStd)
                .then(function (data) {
                    data.moduleclasses.forEach(function (moduleclass) {
                        const this_idModuleClass = moduleclass.idModuleClass;
                        get_detail_schedule(this_idModuleClass)
                            .then(function (data) {
                                const schedule = data.schedule;
                                table_info_moduleclass(moduleclass, schedule);
                                setTimeout(function () {
                                    isButtonLocked = false;
                                }, 3000);
                            })
                            .catch(function () {
                                alert("Lỗi khi lấy dữ liệu thời khóa biểu");
                                isButtonLocked = false;
                            });
                    });
                })
                .catch(function () {
                    alert("Lỗi khi lấy dữ liệu lớp học phần");
                    isButtonLocked = false;
                });
        };
    });


    //tim kiem hoc phan
    const searchBtn = document.getElementById("search-btn");
    searchBtn.addEventListener("click", function () {
        document.getElementById("moduleclass").innerHTML = "";
        const searchValue = document.getElementById("search-value").value;
        search_moduleclass(searchValue)
            .then(function (data) {
                data.moduleclasses.forEach(function (moduleclass) {
                    const this_idModuleClass = moduleclass.idModuleClass;
                    get_detail_schedule(this_idModuleClass)
                        .then(function (data) {
                            const schedule = data.schedule;
                            table_info_moduleclass(moduleclass, schedule);
                        })
                        .catch(function () {
                            alert("Lỗi khi lấy dữ liệu thời khóa biểu");
                        });
                });
            })
            .catch(function () {
                alert("Lỗi khi lấy dữ liệu lớp học phần");
            });
    })



    //nut luu hoc phan vao csdl
    const saveBtn = document.getElementById("save-btn");
    saveBtn.addEventListener("click", function () {
        const moduleclass = document.getElementById("moduleclass");
        const checkedboxs = moduleclass.querySelectorAll("input[type='checkbox']:checked");

        var listModuleClass = [];
        for (const checkedbox of checkedboxs) {
            const row = checkedbox.closest("tr");
            const idModuleClass = row.getAttribute("idModuleClass");
            listModuleClass.push(idModuleClass);
        }
        save_moduleclass(idStd, listModuleClass)
            .then(function(data) {
                if (data.success) {
                    alert("Lưu học phần vào CSDL thành công");
                    location.reload();
                }
                else if(data.full_slot){
                    alert("Hết số lượng được phép đăng ký");
                    location.reload();
                }
                else if(data.duplicate){
                    var mess_dup = "Không được đăng ký môn có trùng lịch học: \n ";
                    for (var messs in data.duplicate) {
                        mess_dup += data.duplicate[messs] + "\n";
                    }
                    alert(mess_dup);
                    location.reload();
                }
                else {
                    var message = "Không được đăng ký nhiều hơn một lớp cùng môn trong một học kỳ: \n ";
                    for (var mess in data.exist) {
                        message += data.exist[mess] + "\n";
                    }
                    alert(message);
                    location.reload();
                };
            });
    });



    //load bang hoc phan da   luu
    get_saved_moduleclass(idStd)
        .then(function (data) {
            data.moduleclasses.forEach(function (moduleclass) {
                const this_idModuleClass = moduleclass.idModuleClass;
                get_detail_schedule(this_idModuleClass)
                    .then(function (data) {
                        const schedule = data.schedule;
                        table_saved_moduleclass(moduleclass, schedule);
                    })
                    .catch(function () {
                        alert("Lỗi khi lấy dữ liệu thời khóa biểu");
                    });
            });
        })
        .catch(function () {
            alert("Lỗi khi lấy dữ liệu lớp học phần");
        });



    //nut xoa hoc phan khoi CSDL
    const deleteBtn = document.getElementById("delete-btn");
    deleteBtn.addEventListener("click",function () {
        const saved = document.getElementById("saved-moduleclass");
        const checkedboxs = saved.querySelectorAll("input[type='checkbox']:checked");
        
        var listModuleClass = [];
        for (const checkedbox of checkedboxs) {
            const row = checkedbox.closest("tr");
            const idModuleClass = row.getAttribute("idModuleClass");
            listModuleClass.push(idModuleClass);
        }
        delete_moduleclass(idStd, listModuleClass);
    });




});











//lay danh sach hoc phan theo tien trinh hoc tap
function get_moduleclass(idStd) {
    return new Promise(function (resolve, reject) {
        $.ajax({
            url: 'get-moduleclass/' + idStd + '/',
            method: 'get',
            dataType: 'json',
            success: function (data) {
                resolve(data);
            },
            error: function () {
                reject();
            },
        });
    });
}


//tim mon hoc, hoc phan
function search_moduleclass(value) {
    return new Promise(function (resolve, reject) {
        $.ajax({
            url: 'search-moduleclass/' + value + '/',
            method: 'get',
            dataType: 'json',
            success: function (data) {
                resolve(data);
            },
            error: function () {
                reject(data);
            }
        });
    });
}



// lay thong tin ve lich hoc, lich thi
function get_detail_schedule(idModuleClass) {
    return new Promise(function (resolve, reject) {
        $.ajax({
            url: 'get-detail-schedule/' + idModuleClass + '/',
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

// tao bang thong tin lop hoc phan
function table_info_moduleclass(data, schedule) {
    const tbody = document.getElementById("moduleclass");

    const tr = document.createElement("tr");

    const cell1 = document.createElement("td");
    cell1.innerHTML = '<input type="checkbox">';
    tr.appendChild(cell1);


    const cell2 = document.createElement("td");
    cell2.textContent = data.idModule;
    tr.appendChild(cell2);

    const cell3 = document.createElement("td");
    cell3.textContent = data.nameModule;
    tr.appendChild(cell3);

    const cell4 = document.createElement("td");
    cell4.textContent = data.credit;
    tr.appendChild(cell4);

    const cell5 = document.createElement("td");
    cell5.textContent = data.idClass;
    tr.appendChild(cell5);

    const cell6 = document.createElement("td");
    cell6.textContent = data.slot + "/" + data.max_slot;
    tr.appendChild(cell6);

    const cell7 = document.createElement("td");
    table_schedule(schedule, cell7);
    cell7.classList.add("td-schedule");
    tr.appendChild(cell7);

    tbody.appendChild(tr);
    tr.setAttribute("idModuleClass", data.idModuleClass);
}



// ham tao thoi khoa bieu trong  bang lop hoc phan
function table_schedule(datas, td_parent) {
    const table = document.createElement("table");
    table.classList.add("tb-schedule");

    datas.forEach(function (data) {
        const tr = document.createElement("tr");

        const cell1 = document.createElement("td");
        cell1.textContent = data.class_room;
        cell1.classList.add("cell1");
        tr.appendChild(cell1);


        const cell2 = document.createElement("td");
        cell2.textContent = data.days_of_week;
        cell2.classList.add("cell2");
        tr.appendChild(cell2);

        const cell3 = document.createElement("td");
        cell3.textContent = data.period_start;
        cell3.classList.add("cell3");
        tr.appendChild(cell3);

        table.appendChild(tr);
    });

    td_parent.appendChild(table);
}


//ham gui du lieu danh sach lop hoc phan can luu
function save_moduleclass(idStd, listModuleClass) {
    return new Promise(function(resolve, reject) {
    const csrfToken = getCSRFToken();
    $.ajax({
        url: 'save-moduleclass/' + idStd + '/',
        method: 'POST',
        data: JSON.stringify(listModuleClass),
        contentType: 'application/json',
        dataType: 'json',
        headers: {
            'X-CSRFToken': csrfToken
        },
        success: function (data) {
            resolve(data);
        },
        error: function (data) {

        }
    });
});
}



//lay du lieu ve nhung mon hoc da luu trong csdl
function get_saved_moduleclass(idStd) {
    return new Promise(function (resolve, reject) {
        $.ajax({
            url: 'get-saved-moduleclass/' + idStd + '/',
            method: 'get',
            dataType: 'json',
            success: function (data) {
                resolve(data);
            },
            error: function () {
                reject();
            },
        });
    });
}



// tao bang thong tin lop hoc phan da luu
function table_saved_moduleclass(data, schedule) {
    const tbody = document.getElementById("saved-moduleclass");

    const tr = document.createElement("tr");

    const cell1 = document.createElement("td");
    cell1.innerHTML = '<input type="checkbox">';
    tr.appendChild(cell1);

    const cell2 = document.createElement("td");
    cell2.textContent = data.idModule;
    tr.appendChild(cell2);

    const cell3 = document.createElement("td");
    cell3.textContent = data.nameModule;
    tr.appendChild(cell3);

    const cell4 = document.createElement("td");
    cell4.textContent = data.credit;
    tr.appendChild(cell4);

    const cell5 = document.createElement("td");
    cell5.textContent = data.idClass;
    tr.appendChild(cell5);

    const cell6 = document.createElement("td");
    table_schedule(schedule, cell6);
    cell6.classList.add("td-schedule");
    tr.appendChild(cell6);

    tbody.appendChild(tr);
    tr.setAttribute("idModuleClass", data.idModuleClass);
}




//gui hoc phan can xoa
function delete_moduleclass(idStd, listModuleClass) {
    const csrfToken = getCSRFToken();
    $.ajax({
        url: 'delete-moduleclass/' + idStd + '/',
        method: 'POST',
        data: JSON.stringify(listModuleClass),
        contentType: 'application/json',
        dataType: 'json',
        headers: {
            'X-CSRFToken': csrfToken
        },
        success: function (data) {
            alert("Xóa học phần thành công");
            location.reload();
        },
        error: function () {
            alert("Xóa học phần thất bại");
        }
    });
}

//tao xac nhan csrftoken
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