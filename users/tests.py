import json
import jwt
import unittest
from unittest.mock    import patch, MagicMock

from django.test      import TestCase, Client

from users.models     import User


class KakaoSigninTest(TestCase):
    def setUp(self):
        User.objects.create(
            kakao     = 123456789,
            name      = "홍길동",
            birthday  = "2000-11-30",
            thumbnail = "http://yyy.kakao.com/.../img_110x110.jpg"
        )

    def tearDown(self):
        User.objects.all().delete()

    @patch("users.views.requests")
    def test_kakao_signin_user_success(self, mocked_requests):
        class MockedResponse :
            def json(self) :
                return {
                    "id"            : 123456789,
                    "kakao_account" : {
                        "profile_needs_agreement"   : True,
                        "profile"                   : {
                            "nickname"            : "홍길동",
                            "thumbnail_image_url" : "http://yyy.kakao.com/.../img_110x110.jpg",
                            "profile_image_url"   : "http://yyy.kakao.com/dn/.../img_640x640.jpg",
                            "is_default_image"    : False
                        },
                        "email_needs_agreement"     : False,
                        "is_email_valid"            : True,
                        "is_email_verified"         : True,
                        "email"                     : "sample@sample.com",
                        "age_range_needs_agreement" : False,
                        "age_range"                 : "20~29",
                        "birthday_needs_agreement"  : False,
                        "birthday"                  : "1130",
                        "gender_needs_agreement"    : False,
                        "gender"                    : "female"
                    }
                }
            status_code = 200

        mocked_requests.get = MagicMock(return_value = MockedResponse())

        client   = Client()
        headers  = {"HTTP_Authorization" : "1234"}
        response = client.get("/users/signin", content_type='applications/json', **headers)
        self.assertEqual(response.status_code, 200)

        user       = User.objects.get(kakao=123456789)
        fake_token = jwt.encode({"id" : user.id}, 'none', algorithm = "HS256")
        self.assertEqual(response.json()["token"], fake_token)

    @patch("users.views.requests")
    def test_kakao_signin_user_fail_needtoken(self, mocked_requests) :
        class MockedResponse:

            def json(self) :
                return {
                    "id"            : 123456789,
                    "kakao_account" : {
                        "profile_needs_agreement"   : True,
                        "profile"                   : {
                            "nickname"            : "홍길동",
                            "thumbnail_image_url" : "http://yyy.kakao.com/.../img_110x110.jpg",
                            "profile_image_url"   : "http://yyy.kakao.com/dn/.../img_640x640.jpg",
                            "is_default_image"    : False
                        },
                        "email_needs_agreement"     : False,
                        "is_email_valid"            : True,
                        "is_email_verified"         : True,
                        "email"                     : "sample@sample.com",
                        "age_range_needs_agreement" : False,
                        "age_range"                 : "20~29",
                        "birthday_needs_agreement"  : False,
                        "birthday"                  : "1130",
                        "gender_needs_agreement"    : False,
                        "gender"                    : "female"
                    }
                }
            
            status_code = 200
        mocked_requests.get = MagicMock(return_value = MockedResponse())

        client   = Client()
        headers  = {}
        response = client.get("/users/signin", content_type = 'applications/json', **headers)
        self.assertEqual(response.status_code, 400)

    @patch("users.views.requests")
    def test_kakao_signin_user_keyerror(self, mocked_requests):
        class MockedResponse:
            def json(self):
                return {
                }

            status_code = 400
        mocked_requests.get = MagicMock(return_value = MockedResponse())

        client   = Client()
        headers  = {"HTTP_Authorization" : "1234"}
        response = client.get("/users/signin", content_type='applications/json', **headers)
        self.assertEqual(response.status_code, 408)