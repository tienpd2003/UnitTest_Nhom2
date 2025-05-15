from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from login_admin.models import profile_admin
from newsfeed.models import newsfeed
from django.core.files.uploadedfile import SimpleUploadedFile
import json
from datetime import datetime, date

class AdminMngNewsfeedTests(TestCase):
    def setUp(self):
        """
        Thiết lập dữ liệu ban đầu cho các test case
        - Tạo tài khoản admin test
        - Tạo client để giả lập request
        - Tạo một số bản tin mẫu
        """
        # Tạo profile cho admin
        self.admin_profile = profile_admin.objects.create(
            idAdmin='123',
            password='123',
            nameAdmin='Admin Test',
            datebirthAdmin=date(1990, 1, 1),
            genderAdmin='Nam',
            addressAdmin='Hà Nội',
            emailAdmin='admin@test.com'
        )
        
        # Tạo client để test
        self.client = Client()
        
        # Login với tài khoản admin
        self.client.login(username='123', password='123')
        
        # Tạo một số bản tin mẫu
        self.test_newsfeed = newsfeed.objects.create(
            title="Test News 1",
            pdf_file=b"Test PDF content",
            is_hidden=True
        )
        
        self.test_newsfeed2 = newsfeed.objects.create(
            title="Another Test News",
            pdf_file=b"Another Test PDF content",
            is_hidden=False
        )

    def test_admin_mngnewsfeed_view_not_logged_in(self):
        """
        Test case TC-QLTT-01: Kiểm tra chuyển hướng khi chưa đăng nhập
        Input: Request GET từ user chưa đăng nhập
        Output: 
        - Chuyển hướng đến trang đăng nhập admin
        """
        # Logout để test trường hợp chưa đăng nhập
        self.client.logout()
        response = self.client.get('/admin-mngnewsfeed/')
        self.assertRedirects(response, '/admin/?next=/admin-mngnewsfeed/')

    def test_admin_mngnewsfeed_view_logged_in(self):
        """
        Test case TC-QLTT-02: Kiểm tra hiển thị trang quản lý tin tức khi đã đăng nhập
        Input: Request GET từ admin đã đăng nhập
        Output: 
        - Status code 200
        - Template được sử dụng là admin_mngnewsfeed.html
        - Context chứa thông tin admin
        """
        response = self.client.get('/admin-mngnewsfeed/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin_mngnewsfeed.html')
        self.assertIn('admininfo', response.context)
        self.assertEqual(response.context['admininfo'], self.admin_profile)

    def test_save_newsfeed_success(self):
        """
        Test case TC-QLTT-03: Kiểm tra thêm mới tin tức thành công
        Input:
        - Title hợp lệ
        - File PDF
        - Trạng thái hiển thị
        Output: 
        - Status code 200
        - Message thành công
        - Tin tức được lưu vào database
        """
        pdf_file = SimpleUploadedFile(
            "test.pdf",
            b"PDF content",
            content_type="application/pdf"
        )
        
        response = self.client.post('/admin-mngnewsfeed/save-newsfeed/', {
            'title': 'New Test News',
            'pdf_file': pdf_file,
            'stt_hidden': True
        })
        
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertEqual(response_data['message'], 'Thêm mới tin tức thành công')
        self.assertTrue(newsfeed.objects.filter(title='New Test News').exists())

    def test_save_newsfeed_missing_data(self):
        """
        Test case TC-QLTT-04: Kiểm tra thêm mới tin tức thất bại do thiếu dữ liệu
        Input: Thiếu title hoặc file PDF
        Output:
        - Status code 200
        - Message yêu cầu nhập đủ các trường
        """
        # Test thiếu file PDF
        response = self.client.post('/admin-mngnewsfeed/save-newsfeed/', {
            'title': 'Test News',
            'stt_hidden': True
        })
        
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertEqual(response_data['message'], 'Hãy nhập đủ các trường')

        # Test thiếu title
        pdf_file = SimpleUploadedFile(
            "test.pdf",
            b"PDF content",
            content_type="application/pdf"
        )
        response = self.client.post('/admin-mngnewsfeed/save-newsfeed/', {
            'title': '',
            'pdf_file': pdf_file,
            'stt_hidden': True
        })
        
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertEqual(response_data['message'], 'Hãy nhập đủ các trường')

    def test_get_all_newsfeed(self):
        """
        Test case TC-QLTT-05: Kiểm tra lấy tất cả tin tức
        Input: search_value = 'all'
        Output:
        - Status code 200
        - Danh sách tất cả tin tức
        - Format dữ liệu trả về đúng định dạng
        """
        response = self.client.get('/admin-mngnewsfeed/get-newsfeed/all/')
        
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertIn('newsfeeds', response_data)
        self.assertEqual(len(response_data['newsfeeds']), 2)  # 2 tin tức đã tạo trong setUp
        
        # Kiểm tra format dữ liệu trả về
        first_news = response_data['newsfeeds'][0]
        self.assertIn('id', first_news)
        self.assertIn('post_date', first_news)
        self.assertIn('title', first_news)
        self.assertIn('is_hidden', first_news)

    def test_search_newsfeed(self):
        """
        Test case TC-QLTT-06: Kiểm tra tìm kiếm tin tức
        Input: Từ khóa tìm kiếm
        Output:
        - Status code 200
        - Danh sách tin tức phù hợp với từ khóa
        - Format dữ liệu trả về đúng định dạng
        """
        response = self.client.get('/admin-mngnewsfeed/get-newsfeed/Test/')
        
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertIn('newsfeeds', response_data)
        
        # Kiểm tra kết quả tìm kiếm có chứa từ khóa
        for news in response_data['newsfeeds']:
            self.assertTrue('Test' in news['title'])
            self.assertIn('post_date', news)
            self.assertIn('title', news)
            self.assertIn('is_hidden', news)

    def test_search_newsfeed_no_results(self):
        """
        Test case TC-QLTT-07: Kiểm tra tìm kiếm không có kết quả
        Input: Từ khóa không tồn tại
        Output:
        - Status code 200
        - Danh sách tin tức rỗng
        """
        response = self.client.get('/admin-mngnewsfeed/get-newsfeed/NonExistentKeyword/')
        
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertIn('newsfeeds', response_data)
        self.assertEqual(len(response_data['newsfeeds']), 0)

    def test_delete_newsfeed_success(self):
        """
        Test case TC-QLTT-08: Kiểm tra xóa tin tức thành công
        Input: ID tin tức tồn tại
        Output:
        - Status code 200
        - Message xóa thành công
        - Tin tức đã bị xóa khỏi database
        """
        response = self.client.delete(f'/admin-mngnewsfeed/delete-newsfeed/{self.test_newsfeed.id}/')
        
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertEqual(response_data['message'], 'Xóa tin thành công')
        self.assertFalse(newsfeed.objects.filter(id=self.test_newsfeed.id).exists())

    def test_delete_newsfeed_not_exist(self):
        """
        Test case TC-QLTT-09: Kiểm tra xóa tin tức không tồn tại
        Input: ID tin tức không tồn tại
        Output:
        - Status code 200
        - Message tin không tồn tại
        """
        non_existent_id = 99999
        response = self.client.delete(f'/admin-mngnewsfeed/delete-newsfeed/{non_existent_id}/')
        
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertEqual(response_data['message'], 'Tin không tồn tại')

    def tearDown(self):
        """
        Dọn dẹp sau khi test
        - Xóa các đối tượng đã tạo trong quá trình test
        """
        self.admin_profile.delete()
        newsfeed.objects.all().delete()
