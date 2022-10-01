from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
import random
import string
import pytest
import allure

@allure.epic("Registration cases")
class TestUserRegister(BaseCase):
    exclude_params = [("no_password"), ("no_username"), ("no_firstName"), ("no_lastName"), ("no_email")]

    @allure.description("This test checks successful registration of a new user")
    @allure.tag("Positive")
    def test_create_user(self):
        data = self.prepare_registration_data()

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_status_code(response, 200)
        Assertions.assert_json_has_key(response, "id")

    @allure.description("This test checks that it's not possible to register user with existing email")
    @allure.tag("Negative")
    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_status_code(response, 400)
        Assertions.assert_response_content(response, f"Users with email '{email}' already exists")

    @allure.description("This test checks that it's not possible to register user with incorrectly formatted email")
    @allure.tag("Negative")
    def test_create_user_with_wrong_email(self):
        data = self.prepare_registration_data()
        data['email'] = data['email'].replace("@", "")

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_status_code(response, 400)
        Assertions.assert_response_content(response, "Invalid email format")

    @allure.description("This test checks that it's not possible to register user with too short username")
    @allure.tag("Negative")
    def test_create_user_with_short_name(self):
        data = self.prepare_registration_data()
        data['username'] = random.choice(string.ascii_letters)

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_status_code(response, 400)
        Assertions.assert_response_content(response, "The value of 'username' field is too short")

    @allure.description("This test checks that it's not possible to register user with too long username")
    @allure.tag("Negative")
    def test_create_user_with_too_long_name(self):
        data = self.prepare_registration_data()
        data['username'] = ''.join(random.choices(string.ascii_letters, k=251))

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_status_code(response, 400)
        Assertions.assert_response_content(response, "The value of 'username' field is too long")

    @allure.description("This test checks that it's not possible to register user without one of required parameter")
    @allure.tag("Negative")
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


        response = MyRequests.post("/user/", data=data)

        Assertions.assert_status_code(response, 400)
        Assertions.assert_response_content(response, f"The following required params are missed: {missed_param}")