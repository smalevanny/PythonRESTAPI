from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests

class TestuserDelete(BaseCase):

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

    def test_delete_user_by_id_2(self):
        data = {'email': 'vinkotov@example.com', 'password': '1234'}

        response1 = MyRequests.post("/user/login", data=data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id_login_method = self.get_json_value(response1, "user_id")

        response2 = MyRequests.delete(f"/user/{user_id_login_method}",
                                            headers={"x-csrf-token": token},
                                            cookies={"auth_sid": auth_sid})

        Assertions.assert_status_code(response2, 400)
        Assertions.assert_response_content(response2, 'Please, do not delete test users with ID 1, 2, 3, 4 or 5.')

    def test_delete_user(self):
        response = MyRequests.delete(f"/user/{self.user_id}",
                                  headers={"x-csrf-token": self.token},
                                  cookies={"auth_sid": self.auth_sid})

        Assertions.assert_status_code(response, 200)
        Assertions.assert_response_content(response, '')

        response2 = MyRequests.get(f"/user/{self.user_id}",
                                     headers={"x-csrf-token": self.token},
                                     cookies={"auth_sid": self.auth_sid})

        Assertions.assert_status_code(response2, 404)
        Assertions.assert_response_content(response2, 'User not found')

    def test_delete_wrong_user(self):
        data = {'email': 'vinkotov@example.com', 'password': '1234'}

        response1 = MyRequests.post("/user/login", data=data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")

        #DELETE user created in the setup while being authorized under another user
        print(f"\nThe id of user being deleted is: {self.user_id}")
        response2 = MyRequests.delete(f"/user/{self.user_id}",
                                      headers={"x-csrf-token": token},
                                      cookies={"auth_sid": auth_sid})

        Assertions.assert_status_code(response2, 400)
        #The next assertion passes.
        #Possible bug in API here, since we are not trying to delete user with ID 1, 2, 3, 4 or 5.
        #But we're using user with id=2 credentials
        Assertions.assert_response_content(response2, 'Please, do not delete test users with ID 1, 2, 3, 4 or 5.')





