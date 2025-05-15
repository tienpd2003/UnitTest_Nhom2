document.addEventListener("DOMContentLoaded", function(){
    
    // lay va tao danh sach khoa
    optionFaculty = document.getElementById("list-faculty");
    $.ajax({
        url : 'get-faculty/',
        method: 'get',
        dataType: 'json',
        success: function(data){
            optionFaculty.innerHTML = '';
            const option = document.createElement("option");
            option.value = "0";
            option.textContent = "----- Khoa -----";
            optionFaculty.appendChild(option);
            data.faculties.forEach(function(faculty) {
                const option = document.createElement("option");
                option.value = faculty.idFaculty;
                option.textContent = faculty.nameFaculty;
                optionFaculty.appendChild(option);
            });
        },
        error: function(){
            alert('Có lỗi trong quá trình lấy dữ liệu Khoa');
        }
    }); 
    


    optionDepartment = document.getElementById("list-department");
    const option_department = document.createElement('option');
    option_department.value = "0";
    option_department.textContent = "----- Ngành -----";
    optionDepartment.appendChild(option_department);




            //lay danh sach nganh
        optionFaculty.addEventListener("change", function () {
        const faculty_value = document.getElementById("list-faculty").value;
        optionDepartment = document.getElementById("list-department");
        $.ajax({
            url : 'get-department/' + faculty_value + '/',
            method : 'get',
            dataType : 'json',
            success : function (data) {
                optionDepartment.innerHTML = '';
                const option = document.createElement('option');
                option.value = "0";
                option.textContent = "----- Ngành -----";
                optionDepartment.appendChild(option);
                data.departments.forEach(function (department) {
                    const option = document.createElement('option');
                    option.value = department.idDepartment;
                    option.textContent = department.nameDepartment;
                    optionDepartment.appendChild(option);
                });  
            },
            error: function(){
                alert('Có lỗi trong quá trình lấy dữ liệu Ngành');
            }
        });
    });


            //lay danh sach khóa
        optionidCourse = document.getElementById('list-idCourse');
        $.ajax({
            url : 'get-idCourse/',
            method : 'get',
            dataType : 'json',
            success : function(data){
                optionidCourse.innerHTML = '';
                const option = document.createElement('option');
                option.value = "0";
                option.textContent = "----- Khóa -----";
                optionidCourse.appendChild(option);
                data.idCourses.forEach(function(idCourse) {
                    const option = document.createElement('option');
                    option.value = idCourse.idCourse;
                    option.textContent = idCourse.nameCourse;
                    optionidCourse.appendChild(option);
                });
            },
            error: function(){
                alert('Có lỗi trong quá trình lấy dữ liệu Khóa');
            }  
        });


        optionClass = document.getElementById("list-class");
        const option_class = document.createElement('option');
        option_class.value = "";
        option_class.textContent = "----- Lớp -----";
        optionClass.appendChild(option_class);

            //lay danh sach lop
        optionDepartment.addEventListener("change", get_class);
        optionidCourse.addEventListener("change", get_class);

        optionClass.addEventListener("change", function() {
            const idClass = optionClass.value;
            choosen_class(idClass);
        });
        


        //tim lop
        const search_btn =  document.getElementById("search-btn");
        search_btn.addEventListener("click", function() {
            get_search_class();
        });
});










    //function lay danh sach lop
    function get_class() {
        const idCourse_value = document.getElementById("list-idCourse").value;
        const department_value = document.getElementById("list-department").value;
        optionClass = document.getElementById("list-class");
        $.ajax({
            url : 'get-class/' + department_value + '/' + idCourse_value + '/',
            method : 'get',
            dataType : 'json',
            success : function (data) {
                optionClass.innerHTML = '';
                const option = document.createElement('option');
                option.value = "";
                option.textContent = "----- Lớp -----";
                optionClass.appendChild(option);
                data.classes.forEach(function(classe){
                    const option = document.createElement('option');
                    option.value = classe.idClass;
                    option.textContent = classe.idClass;
                    optionClass.appendChild(option);
                });
            },
            error: function(){
                alert('Có lỗi trong quá trình lấy dữ liệu Lớp');
            }  
        });
    };



    //bang ket qua tim kiem lop
    function get_search_class() {
        const search_value = document.getElementById("search-value").value;
        const result_rows = document.getElementById("table-body");
        if (search_value.trim() !== ""){
        $.ajax({
            url : 'search-class/' + search_value + '/',
            method : 'get',
            dataType : 'json',
            success : function(data){
                document.getElementById("list-idClass").style.display = "block";
                result_rows.innerHTML = "";
                data.classes.forEach(function(classe) {
                    const newRow = document.createElement("tr");
                    newRow.setAttribute("idClass", classe.idClass);
                    newRow.classList.add("result-row");

                    const cell1 = document.createElement("td");
                    cell1.textContent = classe.idClass;
                    newRow.appendChild(cell1);

                    const cell2 = document.createElement("td");
                    cell2.textContent = classe.faculty;
                    newRow.appendChild(cell2);

                    const cell3 = document.createElement("td");
                    cell3.textContent = classe.department;
                    newRow.appendChild(cell3);

                    const cell4 = document.createElement("td");
                    cell4.textContent = classe.idCourse;
                    newRow.appendChild(cell4);

                    result_rows.appendChild(newRow);

                    newRow.addEventListener("click",function (event) {
                        choosen_row(event, result_rows );
                        idClass = newRow.getAttribute("idClass");
                        choosen_class(idClass);
                        const semesterSelect = document.getElementById("list-semester");
                        const idSemester = semesterSelect.value;
                        get_moduleclass(idClass, idSemester);
                    });

                });
            },
            error: function () {
                alert('Có lỗi trong quá trình tìm Lớp')
            }
        });
    }       
    }


    function choosen_class(idClass){
        const choosen_class_value = document.getElementById("choosen-class");
        choosen_class_value.textContent = "LỚP: " + idClass;
        choosen_class_value.setAttribute("data-value", idClass);
    };


    //highlight dong dang duoc chon
    function choosen_row(event, tbody) {
        const rows = tbody.getElementsByTagName("tr");
        for (let i = 0; i < rows.length; i++) {
            rows[i].classList.remove("clicked-row");
        }
        const selectRow = event.currentTarget;
        selectRow.classList.add("clicked-row");
    }


