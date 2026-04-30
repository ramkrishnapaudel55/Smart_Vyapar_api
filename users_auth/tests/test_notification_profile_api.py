from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from transactions.models import Product, Customer
from users_auth.models.models_notification import Notification

User = get_user_model()

class NotificationProfileTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='password123',
            first_name='Test',
            last_name='User'
        )
        self.client.force_authenticate(user=self.user)
        
        # Setup product and customer for sale
        self.product = Product.objects.create(
            user=self.user,
            name='Test Product',
            selling_price=100.00,
            quantity=10
        )
        self.customer = Customer.objects.create(
            user=self.user,
            name='Test Customer',
            phone='1234567890'
        )


    def test_profile_retrieve(self):
        url = reverse('users_auth:profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.user.email)
        self.assertEqual(response.data['username'], self.user.username)

    def test_profile_update(self):
        url = reverse('users_auth:profile-update')
        data = {
            'first_name': 'Updated',
            'last_name': 'Name',
            'bio': 'Updated bio'
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Updated')
        self.assertEqual(self.user.bio, 'Updated bio')

    def test_profile_picture_upload(self):
        import tempfile
        from PIL import Image
        
        # Create a temporary image
        image = Image.new('RGB', (100, 100))
        tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
        image.save(tmp_file)
        tmp_file.seek(0)
        
        url = reverse('users_auth:profile-update')
        data = {
            'profile_picture': tmp_file
        }
        response = self.client.patch(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.user.refresh_from_db()
        self.assertTrue(bool(self.user.profile_picture))


    def test_notification_on_sale_creation(self):
        url = reverse('create-sale')
        data = {
            'customer': self.customer.reference_id,
            'product': self.product.reference_id,
            'quantity': 1,
            'total': 100.00,
            'payment_mode': 'CASH',
            'status': 'COMPLETED',
            'date': '2023-01-01'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Check if notification was created
        self.assertTrue(Notification.objects.filter(user=self.user, notification_type='SALE_ADDED').exists())
        notification = Notification.objects.get(user=self.user, notification_type='SALE_ADDED')
        self.assertIn("New Sale Added", notification.title)
        self.assertIn(self.product.name, notification.message)

    def test_notification_flow(self):
        # 1. Create a notification manually (since sale creation test depends on URL)
        notification = Notification.objects.create(
            user=self.user,
            title="Test Notification",
            message="This is a test",
            notification_type='SYSTEM'
        )
        
        # 2. List notifications
        url_list = reverse('users_auth:notifications')
        response = self.client.get(url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check response structure
        results = response.data
        if isinstance(results, dict) and 'results' in results:
            results = results['results']
            
        self.assertTrue(len(results) > 0)
        self.assertEqual(results[0]['title'], "Test Notification")

        # 3. Mark as read
        url_read = reverse('users_auth:mark-notification-read', args=[notification.reference_id])
        response = self.client.post(url_read)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        notification.refresh_from_db()
        self.assertTrue(notification.is_read)
