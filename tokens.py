import requests
import time

url = "https://playground.learnqa.ru/ajax/api/longtime_job"

#1
response_init_task_as_json = requests.get(url).json()
print(response_init_task_as_json)
token = response_init_task_as_json['token']
task_processing_seconds = response_init_task_as_json['seconds']

#2
response_task_in_progress_as_json = requests.get(url, params={"token":token}).json()
print(response_task_in_progress_as_json)
status = response_task_in_progress_as_json['status']
expected_status = "Job is NOT ready"
if status != expected_status:
    print(f"Wrong status!\nExpected: \"{expected_status}\", Actual: \"{status}\"")

#3
time.sleep(task_processing_seconds)

#4
response_task_in_progress_as_json = requests.get(url, params={"token":token}).json()
print(response_task_in_progress_as_json)
status = response_task_in_progress_as_json['status']
result = response_task_in_progress_as_json['result']
expected_status = "Job is ready"
if status != expected_status:
    print(f"Wrong status!\nExpected: \"{expected_status}\", Actual: \"{status}\"")
if result == None:
    print("The task result is not set")



