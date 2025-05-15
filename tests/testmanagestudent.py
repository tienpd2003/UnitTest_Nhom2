from django.test import TestCase, Client
from django.urls import reverse
from login_std.models import profile_std
from login_admin.models import profile_admin
from faculty.models import Faculty, Department, FacultyClasses, idCourse
from django.contrib.messages import get_messages
from datetime import datetime, date
import json
from django.contrib.auth.hashers import check_password

class TestAdminMngProfileStd(TestCase):
    """
    Test cases cho chức năng quản lý hồ sơ sinh viên
    """
    
    def setUp(self):
        """
        Khởi tạo dữ liệu test cho các test case
        """
        # Tạo dữ liệu khoa
        self.faculty = Faculty.objects.create(
            idFaculty='CNTT',
            nameFaculty='Công nghệ thông tin'
        )
        
        # Tạo dữ liệu ngành thuộc khoa CNTT
        self.department = Department.objects.create(
            idDepartment='KHMT',
            nameDepartment='Khoa học máy tính',
            faculty=self.faculty
        )
        
        # Tạo dữ liệu khóa học
        self.course = idCourse.objects.create(
            idCourse='K21',
            nameCourse='Khóa 2021'
        )
        
        # Tạo lớp học thuộc ngành KHMT, khóa K21
        self.class_instance = FacultyClasses.objects.create(
            idClass='CNPM6',
            department=self.department,
            idCourse=self.course
        )
        
        # Tạo một sinh viên mẫu
        self.student = profile_std.objects.create(
            idStd='12345',
            password='123455',
            nameStd='Nguyễn Văn A',
            datebirthStd=date(2003, 5, 22),
            genderStd='Nam',
            identityStd='00123456789',
            ethnicityStd='Kinh',
            phoneStd='0912345678',
            emailStd='a@example.com',
            addressStd='Hà Nội',
            idClass=self.class_instance,
            graduate=True
        )

        # Tạo admin để test
        self.admin = profile_admin.objects.create(
            idAdmin='123',
            password='123',
            nameAdmin='Admin Test',
            datebirthAdmin=date(1990, 1, 1),
            genderAdmin='Nam',
            addressAdmin='Hà Nội',
            emailAdmin='admin@test.com'
        )

        # Khởi tạo client để test
        self.client = Client()
        
        # Login với tài khoản admin
        login_success = self.client.post(reverse('login_admin'), {
            'username': '123',  # Sử dụng username thay vì idAdmin theo views.py
            'password': '123'
        })
        
        # Kiểm tra đăng nhập thành công
        self.assertEqual(login_success.status_code, 302)  # Redirect sau khi đăng nhập
        self.assertRedirects(login_success, reverse('admin_mngprofilestd'))

    def test_search_by_student_id(self):
        """
        Test Case ID: TC001
        Mục đích: Kiểm tra chức năng tìm kiếm theo mã sinh viên
        Input: search_field='id', search_query='12345'
        Output mong đợi: 
        - Status code 200
        - Kết quả chứa sinh viên có mã 12345
        """
        response = self.client.get(
            reverse('admin_mngprofilestd'),
            {'search_field': 'id', 'search_query': '12345'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Nguyễn Văn A')
        self.assertContains(response, '12345')

    def test_search_by_name(self):
        """
        Test Case ID: TC002
        Mục đích: Kiểm tra chức năng tìm kiếm theo tên sinh viên
        Input: search_field='name', search_query='Nguyễn Văn A'
        Output mong đợi:
        - Status code 200
        - Kết quả chứa sinh viên có tên Nguyễn Văn A
        """
        response = self.client.get(
            reverse('admin_mngprofilestd'),
            {'search_field': 'name', 'search_query': 'Nguyễn Văn A'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Nguyễn Văn A')
        self.assertContains(response, '12345')

    def test_search_by_birthdate(self):
        """
        Test Case ID: TC003
        Mục đích: Kiểm tra chức năng tìm kiếm theo ngày sinh
        Input: search_field='birthdate', search_query='2003-05-22'
        Output mong đợi:
        - Status code 200
        - Kết quả chứa sinh viên có ngày sinh 22/05/2003
        """
        response = self.client.get(
            reverse('admin_mngprofilestd'),
            {'search_field': 'birthdate', 'search_query': '2003-05-22'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Nguyễn Văn A')
        self.assertContains(response, '22/05/2003')

    def test_search_by_address(self):
        """
        Test Case ID: TC004
        Mục đích: Kiểm tra chức năng tìm kiếm theo địa chỉ
        Input: search_field='address', search_query='Hà Nội'
        Output mong đợi:
        - Status code 200
        - Kết quả chứa sinh viên có địa chỉ Hà Nội
        """
        response = self.client.get(
            reverse('admin_mngprofilestd'),
            {'search_field': 'address', 'search_query': 'Hà Nội'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Nguyễn Văn A')
        self.assertContains(response, 'Hà Nội')

    def test_search_by_class(self):
        """
        Test Case ID: TC005
        Mục đích: Kiểm tra chức năng tìm kiếm theo lớp
        Input: search_field='class', search_query='CNPM6'
        Output mong đợi:
        - Status code 200
        - Kết quả chứa sinh viên thuộc lớp CNPM6
        """
        response = self.client.get(
            reverse('admin_mngprofilestd'),
            {'search_field': 'class', 'search_query': 'CNPM6'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Nguyễn Văn A')
        self.assertContains(response, 'CNPM6')

    def test_search_by_gender(self):
        """
        Test Case ID: TC006
        Mục đích: Kiểm tra chức năng tìm kiếm theo giới tính
        Input: search_field='gender', search_query='Nam'
        Output mong đợi:
        - Status code 200
        - Kết quả chứa sinh viên có giới tính Nam
        """
        response = self.client.get(
            reverse('admin_mngprofilestd'),
            {'search_field': 'gender', 'search_query': 'Nam'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Nguyễn Văn A')
        self.assertContains(response, 'Nam')

    def test_search_by_ethnicity(self):
        """
        Test Case ID: TC007
        Mục đích: Kiểm tra chức năng tìm kiếm theo dân tộc
        Input: search_field='ethnicity', search_query='Kinh'
        Output mong đợi:
        - Status code 200
        - Kết quả chứa sinh viên dân tộc Kinh
        """
        response = self.client.get(
            reverse('admin_mngprofilestd'),
            {'search_field': 'ethnicity', 'search_query': 'Kinh'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Nguyễn Văn A')
        self.assertContains(response, 'Kinh')

    def test_search_by_phone(self):
        """
        Test Case ID: TC008
        Mục đích: Kiểm tra chức năng tìm kiếm theo số điện thoại
        Input: search_field='phone', search_query='0912345678'
        Output mong đợi:
        - Status code 200
        - Kết quả chứa sinh viên có SĐT 0912345678
        """
        response = self.client.get(
            reverse('admin_mngprofilestd'),
            {'search_field': 'phone', 'search_query': '0912345678'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Nguyễn Văn A')
        self.assertContains(response, '0912345678')

    def test_search_by_email(self):
        """
        Test Case ID: TC009
        Mục đích: Kiểm tra chức năng tìm kiếm theo email
        Input: search_field='email', search_query='a@example.com'
        Output mong đợi:
        - Status code 200
        - Kết quả chứa sinh viên có email a@example.com
        """
        response = self.client.get(
            reverse('admin_mngprofilestd'),
            {'search_field': 'email', 'search_query': 'a@example.com'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Nguyễn Văn A')
        self.assertContains(response, 'a@example.com')

    def test_search_by_identity(self):
        """
        Test Case ID: TC010
        Mục đích: Kiểm tra chức năng tìm kiếm theo CCCD/CMND
        Input: search_field='identity', search_query='00123456789'
        Output mong đợi:
        - Status code 200
        - Kết quả chứa sinh viên có CCCD 00123456789
        """
        response = self.client.get(
            reverse('admin_mngprofilestd'),
            {'search_field': 'identity', 'search_query': '00123456789'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Nguyễn Văn A')
        self.assertContains(response, '00123456789')

    def test_search_no_results(self):
        """
        Test Case ID: TC011
        Mục đích: Kiểm tra thông báo khi không tìm thấy kết quả
        Input: search_field='id', search_query='99999'
        Output mong đợi:
        - Status code 200
        - Message thông báo không có kết quả
        """
        response = self.client.get(
            reverse('admin_mngprofilestd'),
            {'search_field': 'id', 'search_query': '99999'}
        )
        self.assertEqual(response.status_code, 200)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Không có kết quả phù hợp.')

    def test_search_with_partial_match(self):
        """
        Test Case ID: TC012
        Mục đích: Kiểm tra tìm kiếm với kết quả một phần
        Input: search_field='name', search_query='Nguyễn'
        Output mong đợi:
        - Status code 200
        - Kết quả chứa sinh viên có tên chứa 'Nguyễn'
        """
        response = self.client.get(
            reverse('admin_mngprofilestd'),
            {'search_field': 'name', 'search_query': 'Nguyễn'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Nguyễn Văn A')

        def test_admin_login_required(self):
            """
            Test Case ID: TC001
            Mục đích: Kiểm tra yêu cầu đăng nhập admin trước khi truy cập chức năng
            Input: Truy cập trang quản lý hồ sơ khi chưa đăng nhập
            Output mong đợi:
            - Redirect về trang đăng nhập admin
            """
            # Tạo client mới chưa đăng nhập
            new_client = Client()
            response = new_client.get(reverse('admin_mngprofilestd'))
            self.assertEqual(response.status_code, 302)
            self.assertRedirects(response, '/admin/?next=/admin-mngprofilestd')

    def test_get_profile_detail_success(self):
        """
        Test Case ID: TC013
        Mục đích: Kiểm tra lấy thông tin chi tiết của sinh viên thành công
        Input: idStd='12345' (mã sinh viên tồn tại)
        Output mong đợi:
        - Status code 200
        - Dữ liệu JSON chứa đầy đủ thông tin sinh viên
        - Thông tin khoa, ngành, lớp chính xác
        """
        response = self.client.get(reverse('detail_profile_std', args=['12345']))
        self.assertEqual(response.status_code, 200)
        
        # Parse JSON response
        data = json.loads(response.content)
        
        # Kiểm tra thông tin cơ bản sinh viên
        self.assertEqual(data['idStd'], '12345')
        self.assertEqual(data['nameStd'], 'Nguyễn Văn A')
        self.assertEqual(data['genderStd'], 'Nam')
        self.assertEqual(data['ethnicityStd'], 'Kinh')
        self.assertEqual(data['phoneStd'], '0912345678')
        self.assertEqual(data['emailStd'], 'a@example.com')
        self.assertEqual(data['addressStd'], 'Hà Nội')
        self.assertEqual(data['identityStd'], '00123456789')
        
        # Kiểm tra thông tin khoa, ngành, lớp
        self.assertEqual(data['faculty'], 'Công nghệ thông tin')
        self.assertEqual(data['idFaculty'], 'CNTT')
        self.assertEqual(data['department'], 'Khoa học máy tính')
        self.assertEqual(data['idDepartment'], 'KHMT')
        self.assertEqual(data['idCourse'], 'K21')
        self.assertEqual(data['nameCourse'], 'Khóa 2021')
        
        # Kiểm tra format ngày sinh
        self.assertEqual(data['datebirth'], '22/05/2003')

    def test_get_profile_detail_not_found(self):
        """
        Test Case ID: TC014
        Mục đích: Kiểm tra xử lý khi không tìm thấy sinh viên
        Input: idStd='99999' (mã sinh viên không tồn tại)
        Output mong đợi:
        - Status code 404
        - Message thông báo không tìm thấy hồ sơ
        """
        response = self.client.get(reverse('detail_profile_std', args=['99999']))
        self.assertEqual(response.status_code, 404)
        
        data = json.loads(response.content)
        self.assertEqual(data['error'], 'Không tìm thấy hồ sơ')

    def test_get_profile_detail_unauthorized(self):
        """
        Test Case ID: TC015
        Mục đích: Kiểm tra yêu cầu đăng nhập khi xem chi tiết hồ sơ
        Input: Truy cập chi tiết hồ sơ khi chưa đăng nhập
        Output mong đợi:
        - Redirect về trang đăng nhập
        """
        # Tạo client mới (chưa đăng nhập)
        new_client = Client()
        response = new_client.get(reverse('detail_profile_std', args=['12345']))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/admin/?next=/detail-profile-std/12345/')

    def test_get_faculty_list(self):
        """
        Test Case ID: TC016
        Mục đích: Kiểm tra lấy danh sách khoa
        Input: Không có
        Output mong đợi:
        - Status code 200
        - Danh sách khoa không chứa khoa 'unknown'
        - Thông tin khoa chính xác
        """
        response = self.client.get(reverse('get_faculty'))
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.content)
        self.assertTrue('faculties' in data)
        
        # Kiểm tra có đúng 1 khoa (đã tạo trong setUp)
        self.assertEqual(len(data['faculties']), 1)
        
        # Kiểm tra thông tin khoa
        faculty = data['faculties'][0]
        self.assertEqual(faculty['idFaculty'], 'CNTT')
        self.assertEqual(faculty['nameFaculty'], 'Công nghệ thông tin')
        
        # Kiểm tra không có khoa 'unknown'
        faculty_ids = [f['idFaculty'] for f in data['faculties']]
        self.assertNotIn('unknown', faculty_ids)

    def test_get_department_list(self):
        """
        Test Case ID: TC017
        Mục đích: Kiểm tra lấy danh sách ngành theo khoa
        Input: idFaculty='CNTT'
        Output mong đợi:
        - Status code 200
        - Danh sách ngành thuộc khoa CNTT
        - Thông tin ngành chính xác
        """
        response = self.client.get(reverse('get_department', args=['CNTT']))
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.content)
        self.assertTrue('departments' in data)
        
        # Kiểm tra có đúng 1 ngành (đã tạo trong setUp)
        self.assertEqual(len(data['departments']), 1)
        
        # Kiểm tra thông tin ngành
        department = data['departments'][0]
        self.assertEqual(department['idDepartment'], 'KHMT')
        self.assertEqual(department['nameDepartment'], 'Khoa học máy tính')

    def test_get_department_list_invalid_faculty(self):
        """
        Test Case ID: TC018
        Mục đích: Kiểm tra lấy danh sách ngành với mã khoa không tồn tại
        Input: idFaculty='INVALID'
        Output mong đợi:
        - Status code 200
        - Danh sách ngành rỗng
        """
        response = self.client.get(reverse('get_department', args=['INVALID']))
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.content)
        self.assertTrue('departments' in data)
        self.assertEqual(len(data['departments']), 0)

    def test_get_class_list(self):
        """
        Test Case ID: TC019
        Mục đích: Kiểm tra lấy danh sách lớp theo ngành
        Input: idDepartment='KHMT'
        Output mong đợi:
        - Status code 200
        - Danh sách lớp thuộc ngành KHMT
        - Thông tin lớp chính xác
        """
        response = self.client.get(reverse('get_class', args=['KHMT']))
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.content)
        self.assertTrue('classes' in data)
        
        # Kiểm tra có đúng 1 lớp (đã tạo trong setUp)
        self.assertEqual(len(data['classes']), 1)
        
        # Kiểm tra thông tin lớp
        class_info = data['classes'][0]
        self.assertEqual(class_info['idClass'], 'CNPM6')

    def test_get_class_add_course(self):
        """
         Test Case ID: TC020
        Mục đích: Kiểm tra lấy   danh sách lớp theo ngành và khóa
        Input:
        - idDepartment='KHMT'
        - idCourse='K21'
        Output mong đợi:
        - Status code 200
        - Danh sách lớp thuộcngành KHMT và khóa K21
        - Thông tin lớp chính xác
        """
        response = self.client.get(
            reverse('get_class', args=['KHMT', 'K21'])
        )
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.content)
        self.assertTrue('classes' in data)
        
        # Kiểm tra có đúng 1 lớp (đã tạo trong setUp)
        self.assertEqual(len(data['classes']), 1)
        
        # Kiểm tra thông tin lớp
        class_info = data['classes'][0]
        self.assertEqual(class_info['idClass'], 'CNPM6')

    def test_get_course_list(self):
        """
        Test Case ID: TC021
        Mục đích: Kiểm tra lấy danh sách khóa học
        Input: Không có
        Output mong đợi:
        - Status code 200
        - Danh sách khóa học
        - Thông tin khóa học chính xác
        """
        response = self.client.get(reverse('get_idCourse'))
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.content)
        self.assertTrue('idCourses' in data)
        
        # Kiểm tra có đúng 1 khóa học (đã tạo trong setUp)
        self.assertEqual(len(data['idCourses']), 1)
        
        # Kiểm tra thông tin khóa học
        course = data['idCourses'][0]
        self.assertEqual(course['idCourse'], 'K21')
        self.assertEqual(course['nameCourse'], 'Khóa 2021')

    def test_unauthorized_access(self):
        """
        Test Case ID: TC022
        Mục đích: Kiểm tra yêu cầu đăng nhập cho tất cả các API
        Input: Truy cập các API khi chưa đăng nhập
        Output mong đợi: Redirect về trang đăng nhập
        """
        # Tạo client mới (chưa đăng nhập)
        new_client = Client()
        
        # Test get_faculty
        response = new_client.get(reverse('get_faculty'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/admin/?next=/get-faculty/')
        
        # Test get_department
        response = new_client.get(reverse('get_department', args=['CNTT']))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/admin/?next=/get-department/CNTT/')
        
        # Test get_class
        response = new_client.get(reverse('get_class', args=['KHMT']))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/admin/?next=/get-class/KHMT/')
        
        # Test get_idCourse
        response = new_client.get(reverse('get_idCourse'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/admin/?next=/admin-moduleclass/get-idCourse/')

    def test_create_new_profile(self):
        """
        Test Case ID: TC023
        Mục đích: Kiểm tra tạo mới hồ sơ sinh viên
        Input: 
        - Dữ liệu sinh viên mới hợp lệ
        Output mong đợi:
        - Status code 200
        - Response success = '2' (tạo mới thành công)
        - Dữ liệu được lưu chính xác trong database
        """
        new_student_data = {
            'idStd': '67890',
            'password': 'test123',
            'phoneStd': '0987654321',
            'nameStd': 'Nguyễn Văn B',
            'emailStd': 'b@example.com',
            'datebirthStd': '2003-06-15',
            'genderStd': 'Nam',
            'identityStd': '00987654321',
            'ethnicityStd': 'Kinh',
            'addressStd': 'Hà Nội',
            'idClass': 'CNPM6',
            'graduate': False
        }
        
        response = self.client.post(reverse('update_or_create_profile'), new_student_data)
        self.assertEqual(response.status_code, 200)
        
        # Kiểm tra response
        data = json.loads(response.content)
        self.assertEqual(data['success'], '2')
        
        # Kiểm tra dữ liệu trong database
        created_student = profile_std.objects.get(idStd='67890')
        self.assertEqual(created_student.nameStd, 'Nguyễn Văn B')
        self.assertEqual(created_student.phoneStd, '0987654321')
        self.assertEqual(created_student.emailStd, 'b@example.com')
        self.assertEqual(created_student.genderStd, 'Nam')
        self.assertEqual(created_student.identityStd, '00987654321')
        self.assertEqual(created_student.ethnicityStd, 'Kinh')
        self.assertEqual(created_student.addressStd, 'Hà Nội')
        self.assertEqual(created_student.idClass.idClass, 'CNPM6')

    def test_update_existing_profile(self):
        """
        Test Case ID: TC024
        Mục đích: Kiểm tra cập nhật hồ sơ sinh viên đã tồn tại
        Input:
        - Dữ liệu cập nhật cho sinh viên có mã '12345'
        Output mong đợi:
        - Status code 200
        - Response success = '1' (cập nhật thành công)
        - Dữ liệu được cập nhật chính xác trong database
        """
        update_data = {
            'idStd': '12345',
            'password': '123455',  # Giữ nguyên password
            'phoneStd': '0999888777',
            'nameStd': 'Nguyễn Văn A Updated',
            'emailStd': 'a_updated@example.com',
            'datebirthStd': '2003-05-22',
            'genderStd': 'Nam',
            'identityStd': '00123456789',
            'ethnicityStd': 'Kinh',
            'addressStd': 'Hà Nội Updated',
            'idClass': 'CNPM6',
            'graduate': True
        }
        
        response = self.client.post(reverse('update_or_create_profile'), update_data)
        self.assertEqual(response.status_code, 200)
        
        # Kiểm tra response
        data = json.loads(response.content)
        self.assertEqual(data['success'], '1')
        
        # Kiểm tra dữ liệu trong database
        updated_student = profile_std.objects.get(idStd='12345')
        self.assertEqual(updated_student.nameStd, 'Nguyễn Văn A Updated')
        self.assertEqual(updated_student.phoneStd, '0999888777')
        self.assertEqual(updated_student.emailStd, 'a_updated@example.com')
        self.assertEqual(updated_student.addressStd, 'Hà Nội Updated')
        self.assertTrue(updated_student.graduate)

    def test_update_profile_with_new_password(self):
        """
        Test Case ID: TC025
        Mục đích: Kiểm tra cập nhật mật khẩu của sinh viên
        Input:
        - Dữ liệu cập nhật với mật khẩu mới
        Output mong đợi:
        - Status code 200
        - Response success = '1'
        - Mật khẩu mới được mã hóa và lưu chính xác
        """
        update_data = {
            'idStd': '12345',
            'password': 'newpassword123',
            'phoneStd': '0912345678',
            'nameStd': 'Nguyễn Văn A',
            'emailStd': 'a@example.com',
            'datebirthStd': '2003-05-22',
            'genderStd': 'Nam',
            'identityStd': '00123456789',
            'ethnicityStd': 'Kinh',
            'addressStd': 'Hà Nội',
            'idClass': 'CNPM6',
            'graduate': True
        }
        
        response = self.client.post(reverse('update_or_create_profile'), update_data)
        self.assertEqual(response.status_code, 200)
        
        # Kiểm tra response
        data = json.loads(response.content)
        self.assertEqual(data['success'], '1')
        
        # Kiểm tra mật khẩu mới đã được mã hóa
        updated_student = profile_std.objects.get(idStd='12345')
        self.assertTrue(check_password('newpassword123', updated_student.password))

    def test_create_profile_missing_id(self):
        """
        Test Case ID: TC026
        Mục đích: Kiểm tra xử lý khi thiếu mã sinh viên
        Input:
        - Dữ liệu không có trường idStd
        Output mong đợi:
        - Status code 200
        - Response success = '3' (lỗi)
        """
        invalid_data = {
            'password': 'test123',
            'phoneStd': '0987654321',
            'nameStd': 'Test Student',
            'emailStd': 'test@example.com',
            'datebirthStd': '2003-01-01',
            'genderStd': 'Nam',
            'identityStd': '001234567890',
            'ethnicityStd': 'Kinh',
            'addressStd': 'Test Address',
            'idClass': 'CNPM6'
        }
        
        response = self.client.post(reverse('update_or_create_profile'), invalid_data)
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.content)
        self.assertEqual(data['success'], '3')



    def test_unauthorized_profile_update(self):
        """
        Test Case ID: TC028
        Mục đích: Kiểm tra yêu cầu đăng nhập khi cập nhật hồ sơ
        Input:
        - Gửi request cập nhật khi chưa đăng nhập
        Output mong đợi:
        - Redirect về trang đăng nhập
        """
        new_client = Client()
        update_data = {
            'idStd': '12345',
            'password': '123455',
            'phoneStd': '0912345678',
            'nameStd': 'Test Update',
            'emailStd': 'test@example.com',
            'datebirthStd': '2003-05-22',
            'genderStd': 'Nam',
            'identityStd': '00123456789',
            'ethnicityStd': 'Kinh',
            'addressStd': 'Test Address',
            'idClass': 'CNPM6',
            'graduate': True
        }
        
        response = new_client.post(reverse('update_or_create_profile'), update_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/admin/?next=/update-or-create-profile/')




    def tearDown(self):
        """
        Xóa toàn bộ dữ liệu test sau khi test xong
        Thứ tự xóa: từ bảng con đến bảng cha để tránh lỗi khóa ngoại
        """
        # Xóa dữ liệu sinh viên trước
        profile_std.objects.all().delete()
        
        # Xóa dữ liệu admin
        profile_admin.objects.all().delete()
        
        # Xóa dữ liệu lớp học
        FacultyClasses.objects.all().delete()
        
        # Xóa dữ liệu khóa học
        idCourse.objects.all().delete()
        
        # Xóa dữ liệu ngành
        Department.objects.all().delete()
        
        # Sau khi xóa hết các bảng con, xóa dữ liệu khoa
        Faculty.objects.all().delete()
   
