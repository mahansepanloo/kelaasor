from django.test import SimpleTestCase, TestCase, Client
from django.urls import resolve,reverse
from .views import *


class TestUrls(SimpleTestCase):
    def test_UserSocer(self):
        url = reverse('accounts:s')
        self.assertEqual(resolve(url).func.view_class, UserSocer)

    def test_EditUser(self):
        urls = reverse('accounts:profile')
        self.assertEqual(resolve(urls).func.view_class, EditUser)
    def test_Change_password2(self):
        urls = reverse("accounts:Change_password2")
        self.assertEqual(resolve(urls).func.view_class,Change_password2)
    def test_Change_password(self):
        urls = reverse("accounts:Change_password")
        self.assertEqual(resolve(urls).func.view_class, Change_password)
    def test_OptCode(self):
        urls = reverse("accounts:OptCode")
        self.assertEqual(resolve(urls).func.view_class, OptCode)
    def test_Register(self):
        urls = reverse("accounts:register")
        self.assertEqual(resolve(urls).func.view_class,Register)

    def test_GetSocerINclass(self):
        url = reverse("accounts:GetSocerINclass", args=(1,))
        self.assertEqual(resolve(url).func.view_class, GetSocerINclass)



from .models import User
from .serializer import UserSerializer,ChangeSerializer
class Test_UserSerializer(TestCase):
    @classmethod
    def setUpTestData(cls):
       User.objects.create_user(username='mahan',password="1234",phone_number="09129738933")

    def test_valid_data(self):
        serilazer = UserSerializer(data={'username': 'ali', 'password': "mahkat78",
                                          "password2": "mahkat78", "phone_number": "09123232106"})
        self.assertTrue(serilazer.is_valid())


    def test_empty_data(self):
        serilazers = UserSerializer(data={})
        self.assertFalse(serilazers.is_valid())
        self.assertEqual(len(serilazers.errors),4)
    #
    def test_validate_username(self):
        serilazers = UserSerializer(data={'username':'mahan','password':"mahkat78","password2":"mahkat78",
                                          "phone_number":"amskksgm"})
        self.assertFalse(serilazers.is_valid())
        self.assertEqual(len(serilazers.errors),2)
        self.assertIn('username', serilazers.errors)

from model_bakery import baker
class Test_UserModel(TestCase):
    def setUp(self):
        self.user = baker.make(User,username='mahan')
    def test_string_representation(self):
        self.assertEqual(str(self.user),'mahan')

from exercise.models import Socer,RezScore
from rest_framework_simplejwt.tokens import AccessToken

class Test_UserSocerView(TestCase):

    @classmethod
    def setUpTestData(cls):
        baker.make(Socer)
        baker.make(RezScore)
        cls.user = baker.make(User, username='mahan', password='1234')

    def setUp(self):
        self.client = Client()
        self.token = AccessToken.for_user(self.user)

    def test_usersocer_GET(self):
        response = self.client.get(reverse("accounts:s"),
                                   HTTP_AUTHORIZATION=f'Bearer {self.token}')
        print(response)
        self.assertEqual(response.status_code, 200)
