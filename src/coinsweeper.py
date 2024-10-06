from src.__init__ import *
# from __init__ import *
import requests

import json

class Coinsweeper:
    def __init__(self, token, proxy, timeout):
        self.token = token
        # if proxy:
        #     self.session.proxies.update(proxy)

        self.proxy = proxy
        self.timeout = timeout


        self.accessToken = None
        self.refreshToken = None
        self.game_id = None

        self.user_id = None

        self.hash = None
        self.score = None
        self.gameTime = None

    def login(self):
        json_data = {
            'initData': self.token,
        }

        response = requests.post('https://api.bybitcoinsweeper.com/api/auth/login', json=json_data, proxies=self.proxy)

        if response.status_code != 201:
            return 'fail'

        data = response.json()

        self.accessToken = data['accessToken']

        self.refreshToken = data['refreshToken']


        return 'success'


    def refresh_token(self):
        
        headers = {
            'authority': 'api.bybitcoinsweeper.com',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-EG,en;q=0.9,ar-EG;q=0.8,ar;q=0.7,en-GB;q=0.6,en-US;q=0.5',
            'authorization': f'Bearer {self.accessToken}',
            'content-type': 'application/json',
            'origin': 'https://bybitcoinsweeper.com',
            'referer': 'https://bybitcoinsweeper.com/',
            'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'tl-init-data': self.token,
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        }

        json_data = {
            'refreshToken': self.refreshToken
        }

        response = requests.post('https://api.bybitcoinsweeper.com/api/auth/refresh-token', headers=headers, json=json_data, proxies=self.proxy)

        data = response.json()

        self.accessToken = data['accessToken']
        self.refreshToken = data['refreshToken']

    def user_info(self):
        
        headers = {
            'authority': 'api.bybitcoinsweeper.com',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-EG,en;q=0.9,ar-EG;q=0.8,ar;q=0.7,en-GB;q=0.6,en-US;q=0.5',
            'authorization': f'Bearer {self.accessToken}',
            'origin': 'https://bybitcoinsweeper.com',
            'referer': 'https://bybitcoinsweeper.com/',
            'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'tl-init-data': self.token,
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        }

        response = requests.get('https://api.bybitcoinsweeper.com/api/users/me', headers=headers, proxies=self.proxy)
        # response = self.session.get('https://api.bybitcoinsweeper.com/api/users/me')
        
        if response.status_code == 401:
            self.refresh_token()
            return self.user_info()
        
        if response.status_code != 200:
            return 'fail'
        
        res = response.json()
        self.user_id = res['id']
        res['success'] = True
        return res
    
    def start_game(self):
        
        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en,en-EG;q=0.9,ar-EG;q=0.8,ar;q=0.7,en-US;q=0.6',
            'authorization': f'Bearer {self.accessToken}',
            'cache-control': 'no-cache',
            'origin': 'https://bybitcoinsweeper.com',
            'pragma': 'no-cache',
            'priority': 'u=1, i',
            'referer': 'https://bybitcoinsweeper.com/',
            'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Android WebView";v="128"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'tl-init-data': self.token,
            'user-agent': 'Mozilla/5.0 (Linux; Android 13; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.6613.148 Mobile Safari/537.36',
            'x-requested-with': 'org.telegram.messenger',
        }
        # self.session.headers.update(headers)
        response = requests.post('https://api.bybitcoinsweeper.com/api/games/start', headers=headers, proxies=self.proxy)
        
        if response.status_code == 401:
            self.refresh_token()
            return self.start_game()


        self.game_response = response.json()
        if response.status_code == 201:
            return 'success'
        
        return 'fail'
    
    def win_game(self):
        
        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en,en-EG;q=0.9,ar-EG;q=0.8,ar;q=0.7,en-US;q=0.6',
            'authorization': f'Bearer {self.accessToken}',
            'cache-control': 'no-cache',
            'content-type': 'application/json',
            'origin': 'https://bybitcoinsweeper.com',
            'pragma': 'no-cache',
            'priority': 'u=1, i',
            'referer': 'https://bybitcoinsweeper.com/',
            'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Android WebView";v="128"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'tl-init-data': self.token,
            'user-agent': 'Mozilla/5.0 (Linux; Android 13; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.6613.148 Mobile Safari/537.36',
            'x-requested-with': 'org.telegram.messenger',
        }

        json_data = {
            'gameId': self.game_response['id'],
            'bits': self.game_response['rewards']['bits'],
            'bagCoins': self.game_response['rewards']['bagCoins'],
            'gifts': self.game_response['rewards']['gifts'],
            'score': self.game['score'],
            'gameTime': self.gameTime,
            'h': self.game['hash']
        }
        
        response = requests.post('https://api.bybitcoinsweeper.com/api/games/win', headers=headers, json=json_data, proxies=self.proxy)
        
        if response.status_code == 401:
            self.refresh_token()
            return self.win_game()
        

        if response.status_code == 201:
            return 'success'
        return 'fail'

    def lose_game(self):
        headers = {
            'authority': 'api.bybitcoinsweeper.com',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en,en-EG;q=0.9,ar-EG;q=0.8,ar;q=0.7,en-US;q=0.6',
            'authorization': f'Bearer {self.accessToken}',
            'cache-control': 'no-cache',
            'content-type': 'application/json',
            'origin': 'https://bybitcoinsweeper.com',
            'pragma': 'no-cache',
            'priority': 'u=1, i',
            'referer': 'https://bybitcoinsweeper.com/',
            'sec-ch-ua': '"Android WebView";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'tl-init-data': self.token,
            'user-agent': 'Mozilla/5.0 (Linux; Android 13; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.6668.81 Mobile Safari/537.36',
            'x-requested-with': 'org.telegram.messenger',
        }

        json_data = {
            'gameId': self.game_response['id'],
            'bits': self.game_response['rewards']['bits'],
            'bagCoins': self.game_response['rewards']['bagCoins'],
            'gifts': self.game_response['rewards']['gifts'],
        }

        response = requests.post('https://api.bybitcoinsweeper.com/api/games/lose', headers=headers, json=json_data, proxies=self.proxy)
        if response.status_code == 401:
            self.refresh_token()
            return self.lose_game()
        
        if response.status_code == 201:
            return 'success'
        return 'fail'
    
    def game_data(self, key, gameTime):
        self.gameTime = gameTime
        url = config('API', 'NOT SET')+'/Coinsweeper/api/v1/play'
        with open('test.json', 'w') as f:
            json.dump(self.game_response, f)
        
        data = {
            'key': key,
            'game_response': self.game_response,
            'user_id': self.user_id,
            'game_time': gameTime
        }
        
        if url == 'NOT SET':
            log(f'{Colors.RED} Please Set the API !')
            return 'fail', 1

        response = requests.get(url, json=data, timeout=self.timeout, proxies=self.proxy)
        res = response.json()
        if res['message']=='success':
            self.game = res['game']
            return 'success', response.status_code
        
        return 'fail', response.status_code
    

if __name__ == '__main__':
    tokens = load_tokens()
    x = Coinsweeper(tokens[0], random_proxy(), config('TIMEOUT', 6))
    x.login()
    
    print(x.user_info())
    # x.refresh_token()
    # x.start_game()




