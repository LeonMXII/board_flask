import json
import requests


response = requests.post(
    "http://127.0.0.1:5050/api/v1/board",
    json={"title": "Объявление", "description": "Ищу работу!", "owner": "user"},
 )

print(response.status_code)
print(response.text)


# response = requests.get(
#     "http://127.0.0.1:5050/api/v1/board/3"
#  )
#
# print(response.status_code)
# print(json.dumps(response.json(), ensure_ascii=False, indent=2))

# response = requests.delete(
#     "http://127.0.0.1:5050/api/v1/board/1"
#  )
#
# print(response.status_code)
# print(json.dumps(response.json(), ensure_ascii=False, indent=2))



