from dotenv import load_dotenv
import os
load_dotenv()  
from flask import Flask, render_template, request, jsonify, flash
import requests
import json
import logging
from decimal import Decimal, InvalidOperation
from datetime import datetime, timedelta
import random  
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'pasaishiash'  # Required for flash messages

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Fallback exchange rates in case API fails (with INR as base)
FALLBACK_RATES = {
    'INR': 1.0,
    'USD': 0.012,  # 1 INR = 0.012 USD
    'EUR': 0.011,  # 1 INR = 0.011 EUR
    'GBP': 0.0097, # 1 INR = 0.0097 GBP
    'JPY': 1.78,   # 1 INR = 1.78 JPY
    'AUD': 0.018,  # 1 INR = 0.018 AUD
    'CAD': 0.016,  # 1 INR = 0.016 CAD
    'CHF': 0.011,  # 1 INR = 0.011 CHF
}

# Add comprehensive currency names dictionary
CURRENCY_NAMES = {
    'AED': 'UAE Dirham',
    'AFN': 'Afghan Afghani',
    'ALL': 'Albanian Lek',
    'AMD': 'Armenian Dram',
    'ANG': 'Netherlands Antillean Guilder',
    'AOA': 'Angolan Kwanza',
    'ARS': 'Argentine Peso',
    'AUD': 'Australian Dollar',
    'AWG': 'Aruban Florin',
    'AZN': 'Azerbaijani Manat',
    'BAM': 'Bosnia-Herzegovina Mark',
    'BBD': 'Barbadian Dollar',
    'BDT': 'Bangladeshi Taka',
    'BGN': 'Bulgarian Lev',
    'BHD': 'Bahraini Dinar',
    'BIF': 'Burundian Franc',
    'BMD': 'Bermudan Dollar',
    'BND': 'Brunei Dollar',
    'BOB': 'Bolivian Boliviano',
    'BRL': 'Brazilian Real',
    'BSD': 'Bahamian Dollar',
    'BTN': 'Bhutanese Ngultrum',
    'BWP': 'Botswanan Pula',
    'BYN': 'Belarusian Ruble',
    'BZD': 'Belize Dollar',
    'CAD': 'Canadian Dollar',
    'CDF': 'Congolese Franc',
    'CHF': 'Swiss Franc',
    'CLP': 'Chilean Peso',
    'CNY': 'Chinese Yuan',
    'COP': 'Colombian Peso',
    'CRC': 'Costa Rican Colón',
    'CUP': 'Cuban Peso',
    'CVE': 'Cape Verdean Escudo',
    'CZK': 'Czech Koruna',
    'DJF': 'Djiboutian Franc',
    'DKK': 'Danish Krone',
    'DOP': 'Dominican Peso',
    'DZD': 'Algerian Dinar',
    'EGP': 'Egyptian Pound',
    'ERN': 'Eritrean Nakfa',
    'ETB': 'Ethiopian Birr',
    'EUR': 'Euro',
    'FJD': 'Fijian Dollar',
    'FKP': 'Falkland Islands Pound',
    'FOK': 'Faroese Króna',
    'GBP': 'British Pound Sterling',
    'GEL': 'Georgian Lari',
    'GGP': 'Guernsey Pound',
    'GHS': 'Ghanaian Cedi',
    'GIP': 'Gibraltar Pound',
    'GMD': 'Gambian Dalasi',
    'GNF': 'Guinean Franc',
    'GTQ': 'Guatemalan Quetzal',
    'GYD': 'Guyanaese Dollar',
    'HKD': 'Hong Kong Dollar',
    'HNL': 'Honduran Lempira',
    'HRK': 'Croatian Kuna',
    'HTG': 'Haitian Gourde',
    'HUF': 'Hungarian Forint',
    'IDR': 'Indonesian Rupiah',
    'ILS': 'Israeli New Shekel',
    'IMP': 'Manx Pound',
    'INR': 'Indian Rupee',
    'IQD': 'Iraqi Dinar',
    'IRR': 'Iranian Rial',
    'ISK': 'Icelandic Króna',
    'JEP': 'Jersey Pound',
    'JMD': 'Jamaican Dollar',
    'JOD': 'Jordanian Dinar',
    'JPY': 'Japanese Yen',
    'KES': 'Kenyan Shilling',
    'KGS': 'Kyrgystani Som',
    'KHR': 'Cambodian Riel',
    'KID': 'Kiribati Dollar',
    'KMF': 'Comorian Franc',
    'KRW': 'South Korean Won',
    'KWD': 'Kuwaiti Dinar',
    'KYD': 'Cayman Islands Dollar',
    'KZT': 'Kazakhstani Tenge',
    'LAK': 'Laotian Kip',
    'LBP': 'Lebanese Pound',
    'LKR': 'Sri Lankan Rupee',
    'LRD': 'Liberian Dollar',
    'LSL': 'Lesotho Loti',
    'LYD': 'Libyan Dinar',
    'MAD': 'Moroccan Dirham',
    'MDL': 'Moldovan Leu',
    'MGA': 'Malagasy Ariary',
    'MKD': 'Macedonian Denar',
    'MMK': 'Myanmar Kyat',
    'MNT': 'Mongolian Tugrik',
    'MOP': 'Macanese Pataca',
    'MRU': 'Mauritanian Ouguiya',
    'MUR': 'Mauritian Rupee',
    'MVR': 'Maldivian Rufiyaa',
    'MWK': 'Malawian Kwacha',
    'MXN': 'Mexican Peso',
    'MYR': 'Malaysian Ringgit',
    'MZN': 'Mozambican Metical',
    'NAD': 'Namibian Dollar',
    'NGN': 'Nigerian Naira',
    'NIO': 'Nicaraguan Córdoba',
    'NOK': 'Norwegian Krone',
    'NPR': 'Nepalese Rupee',
    'NZD': 'New Zealand Dollar',
    'OMR': 'Omani Rial',
    'PAB': 'Panamanian Balboa',
    'PEN': 'Peruvian Sol',
    'PGK': 'Papua New Guinean Kina',
    'PHP': 'Philippine Peso',
    'PKR': 'Pakistani Rupee',
    'PLN': 'Polish Złoty',
    'PYG': 'Paraguayan Guarani',
    'QAR': 'Qatari Rial',
    'RON': 'Romanian Leu',
    'RSD': 'Serbian Dinar',
    'RUB': 'Russian Ruble',
    'RWF': 'Rwandan Franc',
    'SAR': 'Saudi Riyal',
    'SBD': 'Solomon Islands Dollar',
    'SCR': 'Seychellois Rupee',
    'SDG': 'Sudanese Pound',
    'SEK': 'Swedish Krona',
    'SGD': 'Singapore Dollar',
    'SHP': 'Saint Helena Pound',
    'SLL': 'Sierra Leonean Leone',
    'SOS': 'Somali Shilling',
    'SRD': 'Surinamese Dollar',
    'SSP': 'South Sudanese Pound',
    'STN': 'São Tomé and Príncipe Dobra',
    'SYP': 'Syrian Pound',
    'SZL': 'Swazi Lilangeni',
    'THB': 'Thai Baht',
    'TJS': 'Tajikistani Somoni',
    'TMT': 'Turkmenistani Manat',
    'TND': 'Tunisian Dinar',
    'TOP': 'Tongan Paʻanga',
    'TRY': 'Turkish Lira',
    'TTD': 'Trinidad and Tobago Dollar',
    'TVD': 'Tuvaluan Dollar',
    'TWD': 'New Taiwan Dollar',
    'TZS': 'Tanzanian Shilling',
    'UAH': 'Ukrainian Hryvnia',
    'UGX': 'Ugandan Shilling',
    'USD': 'United States Dollar',
    'UYU': 'Uruguayan Peso',
    'UZS': 'Uzbekistani Som',
    'VES': 'Venezuelan Bolívar',
    'VND': 'Vietnamese Đồng',
    'VUV': 'Vanuatu Vatu',
    'WST': 'Samoan Tālā',
    'XAF': 'Central African CFA Franc',
    'XCD': 'East Caribbean Dollar',
    'XDR': 'Special Drawing Rights',
    'XOF': 'West African CFA Franc',
    'XPF': 'CFP Franc',
    'YER': 'Yemeni Rial',
    'ZAR': 'South African Rand',
    'ZMW': 'Zambian Kwacha',
    'ZWL': 'Zimbabwean Dollar'
}

def get_exchange_rates():
    try:
        api_key = os.getenv("API_KEY")
        url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/INR"  # Using INR as base
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        
        rates = response.json().get('conversion_rates', {})
        if not rates:
            return FALLBACK_RATES
            
        return rates
        
    except Exception as e:
        logger.error(f"API Error: {str(e)}")
        return FALLBACK_RATES

@app.route('/')
def home():
    return render_template('index.html', rates=get_exchange_rates(), currency_names=CURRENCY_NAMES, active_page='home')

@app.route('/convert', methods=['POST'])
def convert():
    try:
        # Validate amount
        amount = request.form.get('amount', '')
        try:
            amount = Decimal(amount)
            if amount <= 0:
                raise ValueError("Amount must be positive")
        except (InvalidOperation, ValueError) as e:
            flash("Please enter a valid positive number")
            return render_template('index.html', rates=get_exchange_rates(), active_page='home')

        # Validate currencies
        from_currency = request.form.get('from_currency', '').upper()
        to_currency = request.form.get('to_currency', '').upper()
        rates = get_exchange_rates()
        
        if not all([from_currency in rates, to_currency in rates]):
            flash("Invalid currency selection")
            return render_template('index.html', rates=rates, active_page='home')

        # Perform conversion
        result = float(amount) * (rates[to_currency] / rates[from_currency])
        
        return render_template('result.html', 
                             converted_amount=round(result, 2),
                             from_currency=from_currency,
                             to_currency=to_currency,
                             amount=amount,
                             active_page='home')
                             
    except Exception as e:
        logger.error(f"Conversion error: {str(e)}")
        flash("An error occurred during conversion")
        return render_template('index.html', rates=get_exchange_rates(), active_page='home')

@app.route('/toggle-theme', methods=['POST'])
def toggle_theme():
    return jsonify({"status": "success"})

@app.route('/get-live-rates/<currency>')
def get_live_rates(currency):
    try:
        # Demo data - Replace with real API data in production
        current_time = datetime.now()
        data_points = []
        base_rate = 1/FALLBACK_RATES[currency] if currency != 'INR' else 1  # Inverse the rate for display
        
        # Generate 24 hourly data points
        for i in range(24):
            time_point = current_time - timedelta(hours=i)
            # Simulate small random variations in rate
            rate = base_rate * (1 + random.uniform(-0.02, 0.02))
            data_points.append({
                'time': time_point.strftime('%H:%M'),
                'rate': round(rate, 4)
            })
        
        return jsonify({
            'currency': currency,
            'data': data_points[::-1]  # Reverse to show oldest first
        })
        
    except Exception as e:
        logger.error(f"Error fetching live rates: {str(e)}")
        return jsonify({'error': 'Failed to fetch live rates'}), 500

@app.route('/about')
def about():
    team_members = [
        {
            'name': 'Atharva Murukate',
            'role': 'Developer',
            'batch': 'A2',
            'icon': 'fas fa-user-tie'  # Professional developer icon
        },
        {
            'name': 'Ayush Mishra',
            'role': 'Developer',
            'batch': 'A2',
            'icon': 'fas fa-user-tie'  # Professional developer icon
        },
        {
            'name': 'Shailesh Modak',
            'role': 'Developer',
            'batch': 'A2',
            'icon': 'fas fa-user-tie'  # Professional developer icon
        },
        {
            'name': 'Sanjana Jain',
            'role': 'Developer',
            'batch': 'A2',
            'icon': 'fas fa-user-tie female-dev'  # Professional developer icon with female class
        }
    ]
    return render_template('about.html', team_members=team_members, active_page='about')


@app.route('/rates')
def rates():
    rates = get_exchange_rates()
    return render_template('rates.html', rates=rates, currency_names=CURRENCY_NAMES, active_page='rates')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('index.html', rates=get_exchange_rates(), active_page='home'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('index.html', rates=get_exchange_rates(), active_page='home'), 500

if __name__ == '__main__':
    app.run(debug=True)

