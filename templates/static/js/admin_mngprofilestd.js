    function rowClick(row) {
        const showProfile = document.getElementById("showprofile");
        const profileedit = document.getElementById("edit-profile");
        const form_editprofile = document.getElementById("form-editprofile");
        form_editprofile.style.display = "block";
        profileedit.style.display = "none";
        showProfile.style.display = "flex";
            var idStd = row.getAttribute("data-idStd");
            $.ajax({
                url: 'detail-profile-std/' + idStd + '/',
                method: 'get',
                dataType: 'json',
                success: function (data) {
                    var select = data;
                    document.getElementById("select-idStd").textContent = select.idStd;
                    document.getElementById("select-password-edit").value = select.password;
                    document.getElementById("select-phoneStd").textContent = select.phoneStd;
                    document.getElementById("select-nameStd").textContent = select.nameStd;
                    document.getElementById("select-emailStd").textContent = select.emailStd;
                    document.getElementById("select-datebirthStd").textContent = select.datebirth;
                    document.getElementById("select-datebirthStd").setAttribute("data-value", select.datebirthStd);
                    document.getElementById("select-idClass-faculty").textContent = select.faculty; 
                    document.getElementById("select-idClass-faculty").setAttribute("data-value", select.idFaculty);  //mã khoa
                    document.getElementById("select-genderStd").textContent = select.genderStd;
                    document.getElementById("select-addressStd").textContent = select.addressStd;
                    document.getElementById("select-identityStd").textContent = select.identityStd;
                    document.getElementById("select-ethnicityStd").textContent = select.ethnicityStd;
                    document.getElementById("select-idClass-department").textContent = select.department;
                    document.getElementById("select-idClass-idCourse").setAttribute("data-value", select.idCourse);  //Mã khóa
                    document.getElementById("select-idClass-idCourse").textContent = select.nameCourse;
                    document.getElementById("select-idClass").textContent = select.idClass;
                    var graduate = document.getElementById("select-graduate");

                    
                    if (select.graduate) {
                        graduate.textContent = "Chưa tốt nghiệp";
                        document.querySelector("#select-graduate").setAttribute("data-value", "True");
                    } else {
                        graduate.textContent = "Đã tốt nghiệp";
                        document.querySelector("#select-graduate").setAttribute("data-value", "False");
                    }

                    //tạo select box department từ idFaculty (dung de hien thi gia tri mac dinh)
                    const idFaculty = select.idFaculty;
                    const optionDepartment = document.getElementById("select-idClass-department-edit");
                    $.ajax({
                        url: 'get-department/' + idFaculty +'/',
                        method: 'GET',
                        dataType: 'json',
                        success: function (data) {
                            optionDepartment.innerHTML = '';
                            data.departments.forEach(function(department) {
                            const option = document.createElement("option");
                            option.value = department.idDepartment;
                            option.textContent = department.nameDepartment;
                            optionDepartment.appendChild(option);
                            });

                            //tao select class từ idDepartment(dung de hien thi gia tri mac dinh)
                            const idDepartment = select.idDepartment;
                            const optionClass = document.getElementById("select-idClass-edit");
                            $.ajax({
                                url : 'get-class/' + idDepartment + '/' ,
                                method : 'get',
                                typeData : 'json',
                                success : function (data){
                                    optionClass.innerHTML = '';
                                    data.classes.forEach(function (classe) {
                                        const option = document.createElement('option');
                                        option.value = classe.idClass;
                                        option.textContent = classe.idClass;
                                        optionClass.appendChild(option);
                                    });
                                    document.getElementById("select-idClass").setAttribute("data-value", select.idClass);
                                },
                                error: function(){
                                    alert('Có lỗi trong quá trình lấy dữ liệu');
                                },
                            });
                        },
                        error: function () {
                            alert("Không thể lấy thông tin sinh viên.");
                        },
                    });
                    document.getElementById("select-idClass-department").setAttribute("data-value", select.idDepartment);  //mã ngành
                },
                error: function () {
                    alert("Không thể lấy thông tin sinh viên.");
                }
            });

           


            //lấy thông tin về khoa và tạo select box
            const optionFaculty = document.getElementById("select-idClass-faculty-edit");
            $.ajax({
                url: 'get-faculty/',
                method: 'get',
                dataType: 'json',
                success: function(data){
                    optionFaculty.innerHTML = '';
                    data.faculties.forEach(function(faculty) {
                        const option = document.createElement("option");
                        option.value = faculty.idFaculty;
                        option.textContent = faculty.nameFaculty;
                        optionFaculty.appendChild(option);
                    });
                },
                error: function(){
                    alert('Có lỗi trong quá trình lấy dữ liệu');
                }
            });
            
    }



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

    //load
document.addEventListener("DOMContentLoaded", function() {

        

        //click xem thong tin tu bang ket qua
        const rows = document.querySelectorAll(".table-body");
        rows.forEach(function(row) {
            row.addEventListener("click", function(){
                rowClick(this);
            });
        });


        // Nút đóng detail
        const closeBtnDetail = document.getElementById("closedetail");
        const profile_area = document.getElementById("form-editprofile");
        const profiledetail = document.getElementById("showprofile");
        closeBtnDetail.addEventListener("click", function() {
            profile_area.style.display = "none";
        });

        // Nút đóng edit
        const closeBtnEdit = document.getElementById("closeedit");
        closeBtnEdit.addEventListener("click", function() {
            profile_area.style.display = "none";
        });

        // Nút thêm mới
        const addprofileBtn = document.getElementById("addprofile");
        const titlecard = document.getElementById("title-card");
        const hidden_idStd = document.getElementById("value-idStd");
        const text_Std = document.getElementById("select-idStd-edit");
        const graduate = document.getElementById("gradutelb");
        const profileedit = document.getElementById("edit-profile");
        addprofileBtn.addEventListener("click", function() {
            clearFormInputs();
            graduate.style.display = "none";
            hidden_idStd.style.display = "";
            refreshBtn.style.display="";
            text_Std.style.display="none";
            profiledetail.style.display = "none";
            titlecard.textContent = "Thêm mới hồ sơ";
            profileedit.style.display = "flex";
            profile_area.style.display = "flex";

            const optionFaculty = document.getElementById("select-idClass-faculty-edit");
            maxlength_input_number();
            $.ajax({
                url: 'get-faculty/',
                method: 'get',
                dataType: 'json',
                success: function(data){
                    optionFaculty.innerHTML = '';
                    data.faculties.forEach(function(faculty) {
                        const option = document.createElement("option");
                        option.value = faculty.idFaculty;
                        option.textContent = faculty.nameFaculty;
                        optionFaculty.appendChild(option);
                    });
                    document.getElementById("select-idClass-faculty-edit").value = "abc";
                },
                error: function(){
                    alert('Có lỗi trong quá trình lấy dữ liệu');
                }
            });
        });

        // Nút sửa hồ sơ
        const editprofileBtn = document.getElementById("editprofile");
        editprofileBtn.addEventListener("click", function() {
            hidden_idStd.style.display = "none";
            graduate.style.display = "";
            titlecard.textContent = "Chỉnh sửa hồ sơ";
            text_Std.style.display="";
            refreshBtn.style.display="none";
            profileedit.style.display = "flex";
            profile_area.style.display = "flex";
            profiledetail.style.display = "none";
            document.getElementById("select-idStd-edit").textContent =  document.getElementById("select-idStd").textContent;
            document.getElementById("value-idStd").value =  document.getElementById("select-idStd").textContent;
            document.getElementById("select-phoneStd-edit").value =  document.getElementById("select-phoneStd").textContent;
            document.getElementById("select-nameStd-edit").value =  document.getElementById("select-nameStd").textContent;
            document.getElementById("select-emailStd-edit").value =  document.getElementById("select-emailStd").textContent;
            document.getElementById("select-datebirthStd-edit").value =  document.getElementById("select-datebirthStd").getAttribute("data-value");
            document.getElementById("select-idClass-faculty-edit").value = document.querySelector("#select-idClass-faculty").getAttribute("data-value");
            document.getElementById("select-genderStd-edit").value =  document.getElementById("select-genderStd").textContent;
            document.getElementById("select-identityStd-edit").value =  document.getElementById("select-identityStd").textContent;
            document.getElementById("select-ethnicityStd-edit").value =  document.getElementById("select-ethnicityStd").textContent;
            document.getElementById("select-idClass-department-edit").value = document.querySelector("#select-idClass-department").getAttribute("data-value");
            document.getElementById("select-addressStd-edit").value =  document.getElementById("select-addressStd").textContent;
            document.getElementById("select-idClass-idCourse-edit").value =  document.getElementById("select-idClass-idCourse").getAttribute("data-value");
            document.getElementById("select-idClass-edit").value =  document.querySelector("#select-idClass").getAttribute("data-value");
            document.getElementById("select-graduate-edit").value =  document.querySelector("#select-graduate").getAttribute("data-value");
            maxlength_input_number();
        });




        //cập nhật select deparment khi thay đổi faculty
        const onchangeFaculty = document.getElementById("select-idClass-faculty-edit");
        onchangeFaculty.addEventListener("change", function () {
        const selectFacultyValue = onchangeFaculty.value;
        const optionDepartment = document.getElementById("select-idClass-department-edit");
        $.ajax({
                url: 'get-department/'+ selectFacultyValue + '/',
                method: 'get',
                dataType: 'json',
                success: function (data) {
                    optionDepartment.innerHTML = '';
                    data.departments.forEach(function(department) {
                        const option = document.createElement("option");
                        option.value = department.idDepartment;
                        option.textContent = department.nameDepartment;
                        optionDepartment.appendChild(option);
                    });
                },
                error: function(){
                    alert('Có lỗi trong quá trình lấy dữ liệu');
                },
        });
        });



        //hàm cập nhật class
        function updateselectClass() {
            const optionClass = document.getElementById("select-idClass-edit");
            const selectidCourseValue = document.getElementById("select-idClass-idCourse-edit").value;
            const selectDepartmentValue = onchangeDepartment.value;
            $.ajax({
                url : 'get-class-add-course/' + selectDepartmentValue + '/' + selectidCourseValue + '/',
                method : 'get',
                typeData : 'json',
                success : function (data){
                    optionClass.innerHTML = '';
                    data.classes.forEach(function (classe) {
                        const option = document.createElement('option');
                        option.value = classe.idClass;
                        option.textContent = classe.idClass;
                        optionClass.appendChild(option);
                    });
                },
            });     
        }

        // cập nhật select class khi thay đổi department

        const onchangeDepartment = document.getElementById("select-idClass-department-edit");
        onchangeDepartment.addEventListener("change", updateselectClass);

        //cập nhật select khi thay đổi khóa

        const onchangeidCourse = document.getElementById("select-idClass-idCourse-edit");
        onchangeidCourse.addEventListener("change", updateselectClass);



        


      

        
        //danh sách khóa và select box lần đầu

        const optionidCourse = document.getElementById("select-idClass-idCourse-edit");
        $.ajax({
            url: 'get-idCourse',
            method: 'get',
            typeData: 'json',
            success : function (data) {
                    optionidCourse.innerHTML = "";
                    data.idCourses.forEach(function (idCourse) {
                       const option = document.createElement("option");
                       option.value = idCourse.idCourse;
                       option.textContent = idCourse.nameCourse;
                       optionidCourse.appendChild(option); 
                    });
                },
            error: function(){
                    alert('Có lỗi trong quá trình lấy dữ liệu');
            },
        });
        
        //hàm làm mới
        function clearFormInputs() {
            const inputs = document.querySelectorAll(".edit-profile input");
            inputs.forEach(function(input) {
                input.value = "";
            });
            
            const selects = document.querySelectorAll(".edit-profile select");
            selects.forEach(function(select){
                select.value = "0";
            });
        }

        const refreshBtn = document.getElementById("button-refresh");
        refreshBtn.addEventListener("click", function() {
            clearFormInputs();
        });




        // Nút  lưu
        const saveBtn = document.getElementById("saveprofile");
        saveBtn.addEventListener("click", function(event) {
            const csrfToken = getCSRFToken();
            var profile_data = {
                idStd : document.getElementById("value-idStd").value,
                password : document.getElementById("select-password-edit").value,
                phoneStd : document.getElementById("select-phoneStd-edit").value,
                nameStd : document.getElementById("select-nameStd-edit").value,
                emailStd : document.getElementById("select-emailStd-edit").value,
                datebirthStd : document.getElementById("select-datebirthStd-edit").value,
                genderStd : document.getElementById("select-genderStd-edit").value,
                addressStd : document.getElementById("select-addressStd-edit").value,
                idClass : document.getElementById("select-idClass-edit").value,
                identityStd : document.getElementById("select-identityStd-edit").value,
                ethnicityStd : document.getElementById("select-ethnicityStd-edit").value,
                graduate : document.getElementById("select-graduate-edit").value,
            };
            var requiredFields = document.querySelectorAll(".not-empty");
            var passed = true;
            requiredFields.forEach(function(field){
                if (field.value.trim() === ""){
                    passed = false;
                    return;
                };
            });
            if (passed){
            $.ajax({
                url: 'update-or-create-profile/',
                method: 'post',
                data: profile_data,
                dataType: 'json',
                headers: {
                    'X-CSRFToken': csrfToken
                },
                success: function(data) {
                    if (data.success === '1') {
                        alert('Cập nhật hồ sơ thành công');
                    }
                    else if (data.success === '2') {
                        alert('Tạo hồ sơ thành công');
                    }
                    else {
                        alert('Đã có hồ sơ được tạo với MSSV này');
                    }
                },
                error: function() {
                    alert('Có lỗi, vui lòng kiểm tra lại !');
                },
            });
        }
        else {
            alert("Hãy nhập đủ các trường bắt buộc !")
        };
        });



        //bang ket qua sinh vien trong
        const tbody_results = document.getElementById("results-body");
        blank_table(tbody_results, 4, 9);

});





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


//maxlength input number
function maxlength_input_number(){
    document.querySelectorAll('input[type="number"]').forEach(function(input){
        input.addEventListener("input", function(){
            var length = input.value.length;
            const maxLength = input.maxLength;
            if (length > maxLength) {
                input.value = input.value.slice(0, maxLength);

            };
        });
    });
}