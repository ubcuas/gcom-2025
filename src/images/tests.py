from django.test import TestCase
from .models import Image
from django.db.utils import IntegrityError

# Create your tests here.
class ImageTestCase(TestCase):
    def setUp(self):
        Image.objects.create(image='images/test.jpg',
                              title='Test Image', 
                              image_type='visible',
                              taken_at='2021-01-01 12:00:00')

    def test_image(self):
        image = Image.objects.get(title='Test Image')
        self.assertEqual(image.title, 'Test Image')
        self.assertEqual(image.image_type, 'visible')
        self.assertEqual(image.taken_at.strftime('%Y-%m-%d %H:%M:%S'), '2021-01-01 12:00:00')
    
    def test_representation(self):
        image = Image.objects.get(title='Test Image')
        self.assertEqual(str(image), '2021-01-01 12:00:00')

    def test_cannot_create_without_date(self):
        with self.assertRaises(IntegrityError):
            Image.objects.create(image='images/test.jpg',
                                 title='Test Image', 
                                 image_type='visible')
    
    def test_cannot_create_without_title(self):
        with self.assertRaises(IntegrityError):
            Image.objects.create(image='images/test.jpg',
                                 title=None,
                                 image_type='visible',
                                 taken_at='2021-01-01 12:00:00')
    
    def test_cannot_create_without_image_type(self):
        with self.assertRaises(IntegrityError):
            Image.objects.create(image='images/test.jpg',
                                 title='Test Image',
                                 taken_at='2021-01-01 12:00:00',
                                 image_type=None)
    
    

    