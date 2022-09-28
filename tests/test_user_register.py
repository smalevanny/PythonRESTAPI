import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import random
import string
import pytest

class TestUserRegister(BaseCase):
    exclude_params = [("no_password"), ("no_username"), ("no_firstName"), ("no_lastName"), ("no_email")]

    def test_create_user(self):
        data = self.prepare_registration_data()

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_status_code(response, 200)
        Assertions.assert_json_has_key(response, "id")

    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email)

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_status_code(response, 400)
        Assertions.assert_response_content(response, f"Users with email '{email}' already exists")

    def test_create_user_with_wrong_email(self):
        data = self.prepare_registration_data()
        data['email'] = data['email'].replace("@", "")

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_status_code(response, 400)
        Assertions.assert_response_content(response, "Invalid email format")

    def test_create_user_with_short_name(self):
        data = self.prepare_registration_data()
        data['username'] = random.choice(string.ascii_letters)

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_status_code(response, 400)
        Assertions.assert_response_content(response, "The value of 'username' field is too short")

    def test_create_user_with_too_long_name(self):
        data = self.prepare_registration_data()
        data['username'] = ''.join(random.choices(string.ascii_letters, k=251))

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_status_code(response, 400)
        Assertions.assert_response_content(response, "The value of 'username' field is too long")

    @pytest.mark.parametrize('condition', exclude_params)
    def test_create_user_without_some_parameter(self, condition):
        data = self.prepare_registration_data()

        match condition:
            case "no_password":
                data['password'] = None
                missed_param = 'password'
            case "no_username":
                data['username'] = None
                missed_param = 'username'
            case "no_firstName":
                data['firstName'] = None
                missed_param = 'firstName'
            case "no_lastName":
                data['lastName'] = None
                missed_param = 'lastName'
            case "no_email":
                data['email'] = None
                missed_param = 'email'


        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_status_code(response, 400)
        Assertions.assert_response_content(response, f"The following required params are missed: {missed_param}")