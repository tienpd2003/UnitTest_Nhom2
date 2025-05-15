import io
import pandas as pd
from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
from login_admin.models import profile_admin
from course.models import FacultyClasses, Faculty, Department, Module, ModuleClass, Student_ModuleClass,idCourse
from login_std.models import profile_std
from datetime import date


class TranscriptViewTests(TestCase):
    def setUp(self):
        # Tạo dữ liệu liên quan
        faculty = Faculty.objects.create(idFaculty="CNTT", nameFaculty="Công nghệ thông tin")
        department = Department.objects.create(faculty=faculty, idDepartment="CNPM", nameDepartment="Phần mềm")
        course = idCourse.objects.create(idCourse="K22", nameCourse="Khóa 2022")
        class_obj = FacultyClasses.objects.create(idClass="CLC123", department=department, idCourse=course)

        # Tạo sinh viên
        self.student = profile_std.objects.create(
            idStd="1234567890",
            password="123",  # sẽ được mã hóa nhờ signal
            nameStd="Nguyễn Văn A",
            datebirthStd=date(2000, 1, 1),
            genderStd="Nam",
            addressStd="Hà Nội",
            idClass=class_obj
        )

    def test_get_search_class(self):
        response = self.client.get(reverse('get_search_class', args=['C01']))
        self.assertEqual(response.status_code, 200)
        self.assertIn('classes', response.json())

    def test_get_list_module(self):
        response = self.client.get(reverse('get_list_module', args=['C01']))
        self.assertEqual(response.status_code, 200)
        self.assertIn('modules', response.json())

    def test_get_list_std(self):
        response = self.client.get(reverse('get_list_std', args=['C01', 'M01']))
        self.assertEqual(response.status_code, 200)
        self.assertIn('transcripts', response.json())
        self.assertEqual(response.json()['transcripts'][0]['idStd'], 'SV01')

    def test_upload_excel_upload_mode(self):
        # Tạo file Excel test
        df = pd.DataFrame({
            'STT': [1],
            'MSSV': ['SV01'],
            'Tên SV': ['Nguyễn Văn A'],
            'Lớp': ['C01'],
            'Điểm quá trình': [7.5],
            'Điểm cuối kỳ': [8.0],
        })

        excel_file = io.BytesIO()
        df.to_excel(excel_file, index=False, startrow=4)  # skiprows=4 để trùng với view
        excel_file.seek(0)
        uploaded = SimpleUploadedFile("test.xlsx", excel_file.read(), content_type="application/vnd.ms-excel")

        url = reverse('upload_file_excel', args=['C01', 'M01', 'upload'])
        response = self.client.post(url, {'excel_file': uploaded})
        self.assertEqual(response.status_code, 200)
        self.assertIn('transcripts', response.json())

    def test_get_transcript_all_semester(self):
        response = self.client.get(reverse('get_transcript_semester', args=['SV01', 'all']))
        self.assertEqual(response.status_code, 200)
        self.assertIn('transcripts', response.json())
