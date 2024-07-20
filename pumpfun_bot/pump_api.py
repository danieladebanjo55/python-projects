# pumpfun_api.py
import requests
from config import PUMP_FUN_API_KEY

BASE_URL = 'https://api.pump.fun/'

def get_new_tokens():
    response = requests.get(f'{BASE_URL}/new-tokens', headers={'Authorization': f'Bearer {PUMP_FUN_API_KEY}'})
    return response.json()

def buy_token(token_id, amount):
    data = {'token_id': token_id, 'amount': amount}
    response = requests.post(f'{BASE_URL}/buy', json=data, headers={'Authorization': f'Bearer {PUMP_FUN_API_KEY}'})
    return response.json()

def sell_token(token_id, amount):
    data = {'token_id': token_id, 'amount': amount}
    response = requests.post(f'{BASE_URL}/sell', json=data, headers={'Authorization': f'Bearer {PUMP_FUN_API_KEY}'})
    return response.json()
