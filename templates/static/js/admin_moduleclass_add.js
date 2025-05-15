document.addEventListener("DOMContentLoaded", function(){
    var globalRow = null;
    const display_table = document.getElementById("added-moduleclass");
    //lấy danh sách các môn trong cơ sở dữ liệu
    const idClass = document.getElementById("choosen-class").getAttribute("data-value");
    const get_list_modulBtn = document.getElementById("get-list-module");
    get_list_modulBtn.addEventListener("click", function(){
        const idClass = document.getElementById("choosen-class").getAttribute("data-value");
        document.getElementById("idClass-choose-module").textContent = "LỚP: "+idClass;
        if(idClass !== null && idClass !== ""){
            $.ajax({
                url : 'get-list-module/' + idClass +'/',
                method : 'get',
                dataType : 'json',
                success : function(data){
                    const tbody_module = document.getElementById("tbody-module");
                    document.getElementById("popup").style.display = "block";
                    tbody_module.innerHTML = "";
                    data.module_departments.forEach(function(module){
                        const newRow = document.createElement("tr");
                        newRow.classList.add("result-row");
                        newRow.setAttribute("idModule-value", module.idModule);

                        const cell1 = document.createElement("td");
                        const checkbox = document.createElement("input");
                        checkbox.type = "checkbox";
                        cell1.appendChild(checkbox);
                        newRow.appendChild(cell1);
                        
                        const cell2 = document.createElement("td");
                        cell2.textContent = module.idModule;
                        newRow.appendChild(cell2);

                        const cell3 = document.createElement("td");
                        cell3.textContent = module.nameModule;
                        newRow.appendChild(cell3);

                        const cell4 = document.createElement("td");
                        cell4.textContent = module.credits;
                        newRow.appendChild(cell4);

                        const cell5 = document.createElement("td");
                        cell5.textContent = module.department;
                        newRow.appendChild(cell5);

                        const cell6 = document.createElement("td");
                        newRow.appendChild(cell6);

                        tbody_module.appendChild(newRow);

                        check_moduleclass_exist(idClass, module.idModule, function (exist) {
                            if (exist === true) {
                                cell6.textContent = "Đã học";
                                checkbox.disabled = true;
                                cell6.setAttribute("exist", "1");
                            }
                            else{
                                cell6.textContent = "Chưa học";
                                cell6.setAttribute("exist", "0");
                            };
                        });
                    });


                    const getallmodule = tbody_module.querySelectorAll("tr");
                    const checkedbox_all = document.getElementById("flexRadioDefault1");
                    checkedbox_all.addEventListener("click", function () {
                        
                        checkbox_all(getallmodule);                      
                    });

                    const checkedbox_exist = document.getElementById("flexRadioDefault2");
                    checkedbox_exist.addEventListener("click", function () {
                        
                        checkbox_exist(getallmodule);                      
                    });

                    const checkedbox_non_exist = document.getElementById("flexRadioDefault3");
                    checkedbox_non_exist.addEventListener("click", function () {
                        
                        checkbox_non_exist(getallmodule);                      
                    })

                },
            });
        }
        else{
            alert("Hãy xác định lớp cần thêm học phần");
        };
    });

    //bang danh sach hoc phan trong
    const table_blank = document.getElementById("choosen-module");
    blank_table(table_blank,7,7);



    //danh sach kỳ
    const semesterSelect = document.getElementById("list-semester");
    get_semester(semesterSelect);
    semesterSelect.addEventListener("change",function(){
    const idClass = document.getElementById("choosen-class").getAttribute("data-value");
    const idSemester = semesterSelect.value;
    get_moduleclass(idClass, idSemester);
    });




    //thêm các học phần vào danh sách mở lớp
    //xử lý bất đồng bộ

const addBtn = document.getElementById("button-add");
addBtn.addEventListener("click", async function() {
    document.getElementById("popup").style.display = "none";
    const checkboxes = document.querySelectorAll("#tbody-module input[type='checkbox']:checked");
    const choosen_module = document.getElementById("choosen-module");
    const length_tbody = choosen_module.childElementCount;
    var index = length_tbody;

    for (const checkbox of checkboxes) {
        const row = checkbox.closest("tr");
        const idModule = row.getAttribute("idModule-value");

        try {
            const response = await fetch('get-module-byidModule/' + idModule + '/');
            if (response.ok) {
                const data = await response.json();
                var index = index + 1;
                const exist_in_db = false;
                add_row_choosen_module(data, index, exist_in_db);
            } else {
                throw new Error('Không có phản hồi từ server');
            }
        } catch (error) {
            alert('Lỗi xử lý dữ liệu');
        }
    }  
});   
  

    //nut them hang cho lich hoc
    const btnAddRowSchedule = document.getElementById("btn-addrowschedule");
    btnAddRowSchedule.addEventListener("click",function(){
        const default_schedule = {
            days_of_week : "T1",
            period_start : "0",
            start_date : "",
            end_date : "",
            periods_count : "3",
            class_rooom : "0",
            idSMC : "-1",
        };
        add_rows_schedule(default_schedule);
    });


    //nut luu thong tin lich hoc lich thi
    btnSaveSchedule();


    //popup close button
      
      document.getElementById("closePopup").addEventListener("click", function() {
        document.getElementById("popup").style.display = "none";
      });

      document.getElementById("closePopup-schedule").addEventListener("click", function() {
        document.getElementById("popup-schedule").style.display = "none";
        document.getElementById("tbody-schedule").innerHTML = "";
      });


});


//them mon hoc vao bang hoc phan
function add_row_choosen_module(module, index, exist_in_db) {
    const choosen_module = document.getElementById("choosen-module");
    const newRow = document.createElement("tr");
    newRow.classList.add("row-choosen-module");

    const cell1 = document.createElement("td");
    cell1.textContent = index;
    newRow.appendChild(cell1);

    const cell2 = document.createElement("td");
    cell2.textContent = module.idModule;
    newRow.appendChild(cell2);

    const cell3 = document.createElement("td");
    cell3.textContent = module.nameModule;
    newRow.appendChild(cell3);

    const cell4 = document.createElement("td");
    cell4.textContent = module.credits;
    newRow.appendChild(cell4);

    const cell5 = document.createElement("td");
    const btnschedule = document.createElement("button");
    btnschedule.textContent= "Cập nhật";
    btnschedule.classList.add("btn-schedule");
    cell5.appendChild(btnschedule);
    newRow.appendChild(cell5);


    const cell6 = document.createElement("td");
    if(exist_in_db){
        cell6.textContent = "đã lưu";
    }
    else{
        cell6.textContent = "chưa lưu";
    };
    newRow.appendChild(cell6);



    const cell7 = document.createElement("td");
    cell7.classList.add("action");
    const btndelete = document.createElement("button");
    btndelete.classList.add("btn-custom");
    const icontrash = document.createElement("i");
    icontrash.classList.add("fa","fa-trash", "trash-icon");
    btndelete.appendChild(icontrash);
    cell7.appendChild(btndelete);
    newRow.appendChild(cell7);

    choosen_module.appendChild(newRow);

    newRow.setAttribute("idModule", module.idModule);
    newRow.setAttribute("nameModule", module.nameModule);


    const idClass = document.getElementById("choosen-class").getAttribute("data-value");
    const idModule = module.idModule;

    //them su kien cho nut xoa module
    btndelete.addEventListener("click", function () {
    delete_moduleclass(idClass, idModule, newRow, updateRowNumbers);
        });


    //them su kien cho nut cap nhat lich hoc
    btnschedule.addEventListener("click", function(){
        btnAddSchedule(newRow);
        });  
}



//nut cap nhat  lịch học
function btnAddSchedule(row){
    globalRow = row.querySelectorAll('td')[5];

    document.getElementById("popup-schedule").style.display = "block";
    document.getElementById("tbody-schedule").innerHTML = "";

    const idClass = document.getElementById("choosen-class").getAttribute("data-value");
    const idModuleClass = document.getElementById("info-moduleclass");
    idModuleClass.textContent = "Lớp " + idClass;
    idModuleClass.setAttribute("data-value",idClass);

    const idModuel = document.getElementById("info-module");
    idModuel.setAttribute("data-value", row.getAttribute("idModule"));
    idModuel.textContent = row.getAttribute("idModule") + " - " + row.getAttribute("nameModule");

    const idModule = row.getAttribute("idModule");

    get_schedule_detail(idClass, idModule, function (data) {
        if (data.schedule_data && data.schedule_exam_data) {
            data.schedule_data.forEach(function (schedule) {
                add_rows_schedule(schedule);
            });
            document.getElementById("max-slots").value = data.max_slot;
            document.getElementById("date-exam").value = data.schedule_exam_data.date_exam;
            const period_start = document.getElementById("period-start").querySelector("select");
            period_start.value = data.schedule_exam_data.period_start;
            const room_exam = document.getElementById("room-exam");
            const currentvalue_room = data.schedule_exam_data.class_room;
            get_room(room_exam, currentvalue_room);
        }

        else {
            document.getElementById("max-slots").value = "";
            document.getElementById("date-exam").value = "";
            const period_start = document.getElementById("period-start").querySelector("select");
            period_start.value = "";
            const class_room = "";
            const room_exam = document.getElementById("room-exam");
            get_room(room_exam, class_room);
        };
    });
};



//lay danh sach ky tu database
function get_semester(semesterSelect) {
    $.ajax({
        url : 'get-semester/',
        method : 'get',
        dataType : 'json',
        success : function(data){
            data.semesters.forEach(function (semester) {
                const option = document.createElement("option");
                option.value = semester.idSemester;
                option.textContent = semester.nameSemester;
                semesterSelect.appendChild(option);
            });
        },
        error: function(){
            alert("Lỗi khi lấy danh sách kỳ học");
        },
    });
}


//lay danh sách phong tu database
function get_room(td_room, currentvalue) {
    $.ajax({
        url: 'get-room/',
        method: 'get',
        dataType: 'json',
        success: function(data){
            td_room.innerHTML = "";
            const roomSelect = document.createElement("select");
            data.rooms.forEach(function (room) {
                const option = document.createElement("option");
                option.value = room.idRoom;
                option.textContent = room.nameRoom;
                roomSelect.appendChild(option);
            });
            td_room.appendChild(roomSelect);
            roomSelect.value = currentvalue;
        },
        error : function(){

        },
    });
}



//lay thong tin ve lich hoc tu database
function get_schedule_detail(idClass, idModule, callback){
    $.ajax({
        url: 'get-schedule-detail/'+ idClass+'/'+ idModule + '/',
        method: 'GET',
        dataType: 'json',
        success: function(data){
            callback(data);
        },
        error: function(){
        },
    });
}



//ham tao them row cho lich hoc chi tiet
function add_rows_schedule(schedule) {
    const period_start = document.getElementById("period-start").querySelector("select");
    const dayofweek = document.getElementById("dayofweek").querySelector("select");
    const tbody_schedule = document.getElementById("tbody-schedule");
    
    const tr_schedule = document.createElement("tr");

    const cell1 = document.createElement("td");
    const dayofweekclone = dayofweek.cloneNode(true);
    cell1.appendChild(dayofweekclone);
    dayofweekclone.value = schedule.days_of_week;
    tr_schedule.appendChild(cell1);

    
    const cell2 = document.createElement("td");
    const period_startclone = period_start.cloneNode(true);
    cell2.appendChild(period_startclone);
    period_startclone.value = schedule.period_start;
    tr_schedule.appendChild(cell2);

    const cell3 = document.createElement("td");
    const input_period = document.createElement("input");
    input_period.type = "number";
    input_period.min = "0";
    input_period.value = schedule.periods_count;
    cell3.appendChild(input_period);
    tr_schedule.appendChild(cell3);

    const cell4 = document.createElement("td");
    const input_startdate = document.createElement("input");
    input_startdate.type = "date";
    input_startdate.value = schedule.start_date;
    cell4.appendChild(input_startdate);
    tr_schedule.appendChild(cell4);

    const cell5 = document.createElement("td");
    const input_enddate = document.createElement("input");
    input_enddate.type = "date";
    input_enddate.value = schedule.end_date;
    cell5.appendChild(input_enddate);
    tr_schedule.appendChild(cell5);

    const cell6 = document.createElement("td");
    tr_schedule.appendChild(cell6);
    get_room(cell6, schedule.class_room);

    const cell7 = document.createElement("td");
    cell7.classList.add("action");
    const btndelete = document.createElement("button");
    btndelete.classList.add("btn-custom");
    const icontrash = document.createElement("i");
    icontrash.classList.add("fa","fa-trash", "trash-icon");
    btndelete.appendChild(icontrash);
    cell7.appendChild(btndelete);
    tr_schedule.appendChild(cell7);

    tr_schedule.setAttribute("idSMC", schedule.idSMC);

    tbody_schedule.appendChild(tr_schedule);
    const idSMC = schedule.idSMC;

    
    
    //them su kien cho nut xoa lich hoc
    btndelete.addEventListener("click", function() {
        delete_schedule(tr_schedule , idSMC);
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


//lay danh sach mon hoc theo lop + hoc ky

function get_moduleclass(idClass, idSemester) {
    $.ajax({
    url : 'get-moduleclass/' + idClass + '/' + idSemester + '/',
    method : 'GET',
    dataType : 'json',
    success : function(data){
        const module = document.getElementById("choosen-module");
        module.innerHTML = "";
        var index = 0;
        data.modules.forEach(function (module) {
            var currentindex = index + 1;
            const exist_in_db = true;
            add_row_choosen_module(module, currentindex, exist_in_db);
            index += 1;
        });
    },
    error : function(){
    }
    });
}


//xoa mon hoc tu danh sach mon hoc thuoc lop
function delete_moduleclass(idClass, idModule, row , callback) {
    $.ajax({
        url : 'delete-moduleclass/'+idClass+'/'+idModule+'/',
        method : 'get',
        dataType : 'json',
        success: function(data){
            if (data.result == "deleted"){
                alert("Xóa thành công");
                row.remove();
                callback();

            }
            else {
                row.remove();
                callback();
            };
        },
        error: function () {
            alert("có lỗi trong quá trình xử lý");
        }
    });
}

// kiẻm tra mon hoc da ton tai trong moduleclass hay chua
function check_moduleclass_exist(idClass, idMoudle, callback) {
    $.ajax({
        url: 'check-moduleclass-exist/' + idClass + '/' + idMoudle + '/',
        method: 'get',
        dataType: 'json',
        success: function(data){

            callback(data.exist);

        },
        error: function(){

        }
    });
}


//filter checkbox da ton tai
function checkbox_exist(alltr) {
    alltr.forEach(function(tr){
        const alltd = tr.querySelectorAll("td");
        const value = alltd[5].getAttribute("exist");
        if (value === "0"){
            
            tr.style.display = "none";
        }
        else if (value === "1"){
            
            tr.style.display = "table-row";
        };
    });
}

//filter checbox chua ton tai
function checkbox_non_exist(alltr) {
    alltr.forEach(function(tr){
        const alltd = tr.querySelectorAll("td");
        const value = alltd[5].getAttribute("exist");
        if (value === "0"){
            tr.style.display = "table-row";
        }
        else if (value === "1"){
            tr.style.display = "none";
        };
    });
    
}

//filter checkboxx tat ca
function checkbox_all(alltr) {
    alltr.forEach(function(tr){
        tr.style.display = "table-row";
    });
    
}

//update lai stt
function updateRowNumbers() {
    const tbody = document.getElementById("added-moduleclass");
    const rows = tbody.querySelectorAll("tr");
    index = 0;
    rows.forEach(function (row) {
        const numberCell = row.querySelector("td:first-child");
        numberCell.textContent = index + 1;
        index += 1;
    });
}

//xoa hang trong lich hoc
function delete_schedule(row, idSMC) {
    $.ajax({
        url: 'delete-schedule/'+ idSMC + '/',
        method: 'get',
        dataType: 'json',
        success: function(data){
            if (data.exist){
                row.remove();
            }
            else {
                row.remove();
            };
        },
        error: function(){
        },
    })    
}



//check input select empty value
function check_fields_value() {
    var fields = document.querySelectorAll("#mng-schedule input, #mng-schedule select");
    for (var i = 0; i < fields.length; i++){
        var field = fields[i];
        if (field.value == ""){
            alert("Hay điền vào những trường cần thiết");
            return false;
        };
    };
    return true;
}


//nut luu thong tin lich hoc va lich thi
//lay du lieu tu bang lich hoc de gui ve views
function btnSaveSchedule() {
    const btnSaveSchedule = document.getElementById("button-save-schedule");
    btnSaveSchedule.addEventListener("click",function(){
        if (check_fields_value()){
            var tableSchedule = [];
            var tableScheduleExam = [];

            var rows_schedule = document.getElementById("tbody-schedule").rows;
            
            for (var i=0; i < rows_schedule.length; i++){
                var rowData = [];
                var cells = rows_schedule[i].cells;

                for (var j=0; j < cells.length; j++) {
                    var inputElement = cells[j].querySelector("input");
                    var selectElement = cells[j].querySelector("select");
                    if (inputElement) {
                        rowData.push(inputElement.value);
                    } else if (selectElement) {
                        rowData.push(selectElement.value);
                    }
                };
                const idSMC = rows_schedule[i].getAttribute("idSMC");
                rowData.push(idSMC);
                tableSchedule.push(rowData);
            };
            
            var rows_schedule_exam = document.getElementById("tbody-finalexam").rows;
            var date_exam = rows_schedule_exam[0].cells[0].querySelector("input").value;
            tableScheduleExam.push(date_exam);
            var start_period_exam = rows_schedule_exam[0].cells[2].querySelector("select").value;
            tableScheduleExam.push(start_period_exam);
            var room_exam = rows_schedule_exam[0].cells[3].querySelector("select").value;
            tableScheduleExam.push(room_exam);
        
            const idClass = document.getElementById("info-moduleclass").getAttribute("data-value");
            const idModule = document.getElementById("info-module").getAttribute("data-value");
            const idSemester = document.getElementById("list-semester").value;
            var max_slot = document.getElementById("max-slots").value;

            const csrfToken = getCSRFToken();
            var data_json = JSON.stringify({
                'tableSchedule' : tableSchedule,
                'tableScheduleExam' : tableScheduleExam,
                'max_slot' : max_slot
            });

            $.ajax({
                url : 'save-moduleclass/' + idClass + '/' + idModule + '/' + idSemester + '/',
                method : 'post',
                data : data_json,
                contentType : 'application/json',
                dataType : 'json',
                headers: {
                    'X-CSRFToken': csrfToken
                },
                success: function(data){
                    if (data.result == "updated"){
                        document.getElementById("popup-schedule").style.display = "none";
                        alert("Cập nhật lịch học thành công");
                    }
                    else{
                        document.getElementById("popup-schedule").style.display = "none";
                        alert("Thêm lớp học phần thành công");
                        globalRow.textContent = "đã lưu";
                    }
                },
                error: function(){
                    alert("Có lỗi xảy ra");
                }
            });
        };
    });
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