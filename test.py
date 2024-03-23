import requests

BASE ="http://127.0.0.1:5000/"

# data = [{"name": "how to become a billanore", "likes": 1000, "views":10000},
#         {"name": "how to become a millanore", "likes": 100, "views":10000},
#         {"name": "how to become a financially independent", "likes": 45, "views":10000}]

# for i in range(len(data)):
#     response = requests.put(BASE + "video/" + str(i), data[i])
#     print(response.json())

# input()

response = requests.patch(BASE+ "video/1", {"likes": 101})
print(response.json())