#RestFul API test script

import requests

BASE = "http://127.0.0.1:5000/"

# data = [{"name": "RayR","views": 1000,"likes": 1000},
#         {"name": "RayJ","views": 2000,"likes": 1550},
#         {"name": "RayF","views": 3000,"likes": 1770},
#         {"name": "RayG","views": 4000,"likes": 1990},
#         {"name": "RayT","views": 5000,"likes": 1209},
#         {"name": "RayK","views": 6000,"likes": 1110}]
# for i in range(len(data)):
#     response = requests.put(BASE + "video/" + str(i), data[i])
#     print(response.json())

# input()
#
# response = requests.delete(BASE + "video/0")
# print(response)

#
# input()
response = requests.patch(BASE + "video/2", {"views": 1990})
print(response.json())