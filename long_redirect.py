import requests

response = requests.get("https://playground.learnqa.ru/api/long_redirect", allow_redirects=True)

redirects_number = len(response.history)

if redirects_number > 0:
    print(f"Number of redirects = {redirects_number}")
else:
    print(f"No redirects registered")

print(f"Last URL is {response.url}")