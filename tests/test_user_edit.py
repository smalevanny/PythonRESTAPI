from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
import random
import string
import allure

@allure.epic("Updating cases")
class TestUserEdit(BaseCase):

    def setup(self):
        # REGISTER
        self.register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=self.register_data)

        Assertions.assert_status_code(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = self.register_data['email']
        first_name = self.register_data['firstName']
        password = self.register_data['password']
        self.user_id = self.get_json_value(response1, "id")

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post("/user/login", data=login_data)

        self.auth_sid = self.get_cookie(response2, "auth_sid")
        self.token = self.get_header(response2, "x-csrf-token")

    @allure.description("This test checks successful name update of just created user")
    @allure.tag("Positive")
    def test_edit_just_created_user(self):
        #EDIT
        new_name = "Changed_name"

        response = MyRequests.put(f"/user/{self.user_id}",
                                            data={"firstName": new_name},
                                            headers={"x-csrf-token": self.token},
                                            cookies={"auth_sid": self.auth_sid})

        Assertions.assert_status_code(response, 200)

        #GET
        response2 = MyRequests.get(f"/user/{self.user_id}",
                                            headers={"x-csrf-token": self.token},
                                            cookies={"auth_sid": self.auth_sid})

        Assertions.assert_status_code(response, 200)
        Assertions.assert_json_value_by_name(response2, "firstName", new_name, "Wrong user name after edit")

    @allure.description("This test checks that it's not possible to update user without being authorized")
    @allure.tag("Negative")
    def test_edit_just_created_user_without_authorization(self):
        # EDIT
        new_name = "Changed_name"

        response = MyRequests.put(f"/user/{self.user_id}",
                                cookies={"auth_sid": self.auth_sid},
                                data={"firstName": new_name})

        Assertions.assert_status_code(response, 400)
        Assertions.assert_response_content(response, "Auth token not supplied")

    @allure.description("This test checks that it's not possible to update user with incorrectly formatted email")
    @allure.tag("Negative")
    def test_edit_just_created_user_wrong_email(self):
        #EDIT
        new_email = self.register_data['email'].replace("@", "")

        response = MyRequests.put(f"/user/{self.user_id}",
                                            headers={"x-csrf-token": self.token},
                                            cookies={"auth_sid": self.auth_sid},
                                            data={"email": new_email})

        Assertions.assert_status_code(response, 400)
        Assertions.assert_response_content(response, "Invalid email format")

    @allure.description("This test checks that it's not possible to update user with very short firstName")
    @allure.tag("Negative")
    def test_edit_just_created_user_too_short_first_name(self):
        #EDIT
        new_name = random.choice(string.ascii_letters)

        response = MyRequests.put(f"/user/{self.user_id}",
                                            headers={"x-csrf-token": self.token},
                                            cookies={"auth_sid": self.auth_sid},
                                            data={"firstName": new_name})

        Assertions.assert_status_code(response, 400)
        Assertions.assert_response_content(response, '{"error":"Too short value for field firstName"}')

    @allure.description("This test checks that it's not possible to update user while being authorized by another user")
    @allure.tag("Negative")
    def test_edit_just_created_user_authorized_by_another_user(self):
        # REGISTER another user
        register_data2 = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data2)

        Assertions.assert_status_code(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email2 = register_data2['email']
        password2 = register_data2['password']

        # LOGIN another user
        login_data = {
            'email': email2,
            'password': password2
        }
        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid2 = self.get_cookie(response2, "auth_sid")
        token2 = self.get_header(response2, "x-csrf-token")

        # EDIT original user authorized as another user
        new_username = "Changed_username"

        response3 = MyRequests.put(f"/user/{self.user_id}",
                                headers={"x-csrf-token": token2},
                                cookies={"auth_sid": auth_sid2},
                                data={"username": new_username})

        # Possible bug in API here. Status code shouldn't be 200 and content should contain error message, but it's empty
        Assertions.assert_status_code(response3, 200)
        Assertions.assert_response_content(response3, '')

        # GET original user
        response4 = MyRequests.get(f"/user/{self.user_id}",
                                 headers={"x-csrf-token": self.token},
                                 cookies={"auth_sid": self.auth_sid})

        # Making sure that original username hasn't been changed
        Assertions.assert_json_value_by_name(response4, "username", self.register_data['username'],
                                             "Wrong username! Username shouldn't have been changed")