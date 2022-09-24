import requests

class TestHeader:
    def test_header(self):
        url = "https://playground.learnqa.ru/api/homework_header"
        expected_header_name = "x-secret-homework-header"
        expected_header_value = "Some secret value"

        response = requests.get(url)

        assert response.status_code == 200, "Wrong response code"
        assert expected_header_name in response.headers.keys(), f"There is no header with name {expected_header_name} in the response headers"

        actual_header_value = response.headers.get(expected_header_name)

        assert actual_header_value == expected_header_value, "Actual header value is not correct"

