import requests


#data = requests.post(url='http://localhost:8000/', data={'command': '0', 'dat': 1})
data2 = requests.post(url='http://localhost:8000/search_by_name', data={'name': 'Sean Thompson'})

print(data2.text)


# import requests
#
# data = {'name': 'Sean Thompson'}
# response = requests.post(url='http://localhost:8000/search_by_name', data=data)
#
# print(response.text)
