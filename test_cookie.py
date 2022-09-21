import requests

class TestCookie:
    def test_cookie(self):
        url = "https://playground.learnqa.ru/api/homework_cookie"
        expected_cookie_name = "HomeWork"
        expected_cookie_value = "hw_value"

        response = requests.get(url)

        assert response.status_code == 200, "Wrong response code"
        assert expected_cookie_name in response.cookies.get_dict(), f"There is no cookie with name {expected_cookie_name} in the response cookies"

        actual_cookie_value = response.cookies.get_dict()[expected_cookie_name]

        assert actual_cookie_value == expected_cookie_value, "Actual cookie value is not correct"


        cookie = response.cookies
        print(cookie.values())
        print(cookie.get_dict())

