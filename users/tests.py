from unittest.mock import patch

#Django
from django.test         import Client
from django.contrib.auth import get_user_model

#DRF
from rest_framework.test import APITestCase, APIRequestFactory
from .models             import GoogleSocialAccount
from .views              import GoogleSignInAPI

User = get_user_model()

client = Client()

test_user_data = {
    'sub'           : 'test_sub1234',
    'name'          : 'test_name',
    'given_name'    : 'test_given_name',
    'family_name'   : 'test_family_name',
    'picture'       : 'test_picture',
    'email'         : 'test123@email.com',
    'email_verified': True,
    'locale'        : 'ko'
    }

class GoogleLoginTest(APITestCase):
    def setUp(self):
        self.factory  = APIRequestFactory()
        self.test_url =  'http://localhost:8080/users/google/login'
    
        self.google_account = GoogleSocialAccount.objects.create(
            sub       = test_user_data.get('sub'),
            image_url = test_user_data.get('picture'),
            email     = test_user_data.get('email'),
        )
        
        self.user = User.objects.create(
            name           = 'test_name',
            ordinal_number =  31,
            google_account = self.google_account
        )
    
    def tearDown(self):
        self.user.delete()
        self.google_account.delete()
    
    @patch.object(GoogleSignInAPI, 'google_get_user_info')
    def test_google_social_signin(self, mocked_google_user_info):
        
        mocked_google_user_info.return_value = test_user_data
        
        response = self.client.get(self.test_url)
        print(response.content)
        
        self.assertEqual(response.status_code, 200)

    
class GoogleLoginTestNotUser(APITestCase):
    def setUp(self):
        self.factory  = APIRequestFactory()
        self.test_url =  'http://localhost:8080/users/google/login'
            
        self.google_account = GoogleSocialAccount.objects.create(
            sub       = test_user_data.get('sub'),
            image_url = test_user_data.get('picture'),
            email     = test_user_data.get('email'),
        )

    def tearDown(self):
        self.google_account.delete()
    
    @patch.object(GoogleSignInAPI, 'google_get_user_info')
    def test_google_social_signin(self, mocked_google_user_info):
        
        mocked_google_user_info.return_value = test_user_data
        
        response = self.client.get(self.test_url)
        print(response.content)
        
        self.assertEqual(response.status_code, 200)


class GoogleLoginTestNotGoogleSocialAccount(APITestCase):
    def setUp(self):
        self.factory  = APIRequestFactory()
        self.test_url =  'http://localhost:8080/users/google/login'
    
    @patch.object(GoogleSignInAPI, 'google_get_user_info')
    def test_google_social_signin(self, mocked_google_user_info):
        
        mocked_google_user_info.return_value = test_user_data
        
        response = self.client.get(self.test_url)
        print(response.content)
        
        self.assertEqual(response.status_code, 200)