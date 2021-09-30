import requests
import json

def request(username: str):
    url = 'https://api.github.com/users/' + username + '/repos'
    req = requests.get(url)
    data = json.loads(req.text)
    for i in range(len(data)):
        print(f"Repository №{i + 1}: {data[i]['name']}")

    with open('data.json', 'w') as f:
        json.dump(data, f)

    print(f'\nOK')

username = input("Insert username: ")
request(username)
