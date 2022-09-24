import requests

url = "https://playground.learnqa.ru/api/compare_query_type"

#1
response_without_param = requests.get(url)
print(response_without_param)

#2
response_wrong_method = requests.head(url, params="HEAD")
print(response_wrong_method)

#3
response_correct_param = requests.get(url, params="GET")
print(response_correct_param)

#4
methods = ["GET", "POST", "PUT", "DELETE"]

for method in methods:
    for param in methods:
        print(f"Method = {method}: Param = {param}")
        match method:
            case "GET":
                response = requests.get(url, params=param)
                print(response)
            case "POST":
                response = requests.post(url, data=param)
                print(response)
            case "PUT":
                response = requests.put(url, data=param)
                print(response)
            case "DELETE":
                response = requests.delete(url, data=param)
                print(response)
            case _:
                print(f"Unsupported HTTP method: {method}")





