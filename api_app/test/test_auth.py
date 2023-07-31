from django.test import tag
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIRequestFactory, APIClient
from api_app.views import LoginView


@tag('auth')
class LoginTestCase(APITestCase):
    """ Test authentication"""

    def setUp(self):
        self.factory = APIRequestFactory()
        self.client = APIClient()
        self.credentials = {"email": "usuario@mail.com", "username": "usuario", "password": "usuario"}
        self.uri = '/api/login/`'
        self.view = LoginView.as_view()
        self.login_request = self.factory.post(self.uri, self.credentials, format='json')
        self.user = User.objects.create(**self.credentials)
        self.user.set_password(self.credentials.get('password'))
        self.user.save()
        # en caso de no  crear un token para el usuario
        # django.contrib.auth.models.User.auth_token.RelatedObjectDoesNotExist: User has no auth_token.
        self.token = Token.objects.create(user=self.user)

    def test_1_login(self):
        """
        Verificar autenticacion correcta
        """
        response = self.view(self.login_request)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data.get('token') is not None)

    def test_2_bad_login(self):
        """
        Verificar autenticacion incorrecta
        """
        self.credentials['username'] = 'usuario_incorrecto'
        self.login_request = self.factory.post(self.uri, self.credentials, format='json')
        response = self.view(self.login_request)

        self.assertEqual(response.status_code, 400)

    def test_protected_endpoint_auth(self):
        response = self.client.get("/api/medios/", self.credentials, headers={'AUTHORIZATION': f'Token {self.token.key}'})

        self.assertEqual(response.status_code, 200)

    def test_protected_endpoint_noauth(self):
        response = self.client.get("/api/medios/", self.credentials,
        content_type='application/json', headers={'AUTHORIZATION': 'Token FakeToken'})
        
        self.assertEqual(response.status_code, 401)
