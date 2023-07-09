from flask import Flask, request, render_template
import json
from typing import Final
import requests

app = Flask(__name__)


BASE_URL: Final[str] = 'http://api.exchangeratesapi.io/v1/latest'
API_KEY: Final[str] = 'b635964842b6139844f1c87f4ef60121'

def get_rates(mock: bool=False) -> dict:
    if mock:
        with open('rates.json', 'r') as file:
            return json.load(file)
    
    payload: dict = {'access_key': API_KEY}
    request = requests.get(url=BASE_URL, params=payload)
    data: dict = request.json()
    
    return data


def get_currency(currency: str, rates: dict) -> float:
    currency: str = currency.upper()
    if currency in rates.keys():
        return rates.get(currency)
    else:
        raise ValueError(f'"{currency}" is not a valid currency.')

def convert_currency(amount: float, base: str, vs: str, rates: dict) -> float:
    base_rate: float = get_currency(base, rates)
    vs_rate: float = get_currency(vs, rates)

    conversion: float = round((vs_rate / base_rate) * amount, 2)
    print(f'{amount:,.2f} ({base}) is: {conversion:,.2f} ({vs})')
    return conversion

@app.route('/')
def home():
    return render_template('index.html')
    
@app.route('/convert', methods=['POST'])
def convert():
    amount = float(request.form['amount'])
    base = request.form['base']
    target = request.form['target']

    data: dict = get_rates(mock=True)
    rates: dict = data.get('rates')

    conversion_result = convert_currency(amount, base, target, rates=rates)

    return render_template('result.html', amount=amount, base=base, target=target, result=conversion_result)

if __name__ == '__main__':
    app.run(debug=True)
