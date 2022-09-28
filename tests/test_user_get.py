from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests

class TestuserGet(BaseCase):
    def test_get_user_by_id_not_authorized(self):
        response = MyRequests.get("/user/2")

        not_expected_keys = ["email", "firstName", "lastName"]

        Assertions.assert_json_has_key(response, "username")
        Assertions.assert_json_has_not_keys(response, not_expected_keys)


    def test_get_user_by_id_authorized(self):
        data = {'email': 'vinkotov@example.com', 'password': '1234'}

        response1 = MyRequests.post("/user/login", data=data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id_login_method = self.get_json_value(response1, "user_id")

        response2 = MyRequests.get(f"/user/{user_id_login_method}",
                                            headers={"x-csrf-token": token},
                                            cookies={"auth_sid": auth_sid})

        expected_keys = ["username", "email", "firstName", "lastName"]
        Assertions.assert_json_has_keys(response2, expected_keys)

    def test_get_another_user_by_id_authorized(self):
        data = {'email': 'vinkotov@example.com', 'password': '1234'}

        response1 = MyRequests.post("/user/login", data=data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id_login_method = self.get_json_value(response1, "user_id")
        another_user_id = '1'

        response2 = MyRequests.get(f"/user/{another_user_id}",
                                            headers={"x-csrf-token": token},
                                            cookies={"auth_sid": auth_sid})

        not_expected_keys = ["email", "firstName", "lastName"]

        assert user_id_login_method != another_user_id, "Another user id is equal to id of authorised user "
        Assertions.assert_json_has_key(response2, "username")
        Assertions.assert_json_has_not_keys(response2, not_expected_keys)


