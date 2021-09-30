import requests
import json

def Logining (param_login):
    requests.post(
    url_token,
    headers=headers,
    json=param_login
)


username = input('Insert username: ');
password = input('Insert password: ');
url_token = 'https://kitsu.io/api/oauth/token'
url_base = 'https://kitsu.io/api/edge'
headers = {'Content - Type': 'application/json'}
param_login = {'grant_type': 'password',
         'username': username,
         'password': password}
Logining(param_login)
# print(json.loads(login.text)) #Проверка токена
find_anime = requests.get(url_base + '/anime?filter[categories]=adventure')
print(find_anime)

with open('data.json', 'w') as f:
    json.dump(json.loads(find_anime.text), f)
