from flask import Flask, render_template, request, url_for, flash, redirect
import requests
import os
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = "63a43551a8683875884b78tfdgshjkdjfjdkjfgjhkjerthjdfdd"
currencies = sorted(['XCD', 'EUR', 'BBD', 'BTN', 'BND', 'XAF', 'CUP', 'USD', 'FKP', 'GIP', 'HUF', 'IRR', 'JMD', 'AUD', 'LAK', 'LYD', 'MKD', 'XOF', 'NZD', 'OMR', 'PGK', 'RWF', 'WST', 'RSD', 'SEK', 'TZS', 'AMD', 'BSD', 'BAM', 'CVE', 'CNY', 'CRC', 'CZK', 'ERN', 'GEL', 'HTG', 'INR', 'JOD', 'KRW', 'LBP', 'MWK', 'MRO', 'MZN', 'ANG', 'PEN', 'QAR', 'STD', 'SLL', 'SOS', 'SDG', 'SYP', 'AOA', 'AWG', 'BHD', 'BZD', 'BWP', 'BIF', 'KYD', 'COP', 'DKK', 'GTQ', 'HNL', 'IDR', 'ILS', 'KZT', 'KWD', 'LSL', 'MYR', 'MUR', 'MNT', 'MMK', 'NGN', 'PAB', 'PHP', 'RON', 'SAR', 'SGD', 'ZAR', 'SRD', 'TWD', 'TOP', 'VEF', 'DZD', 'ARS', 'AZN', 'BYR', 'BOB', 'BGN', 'CAD', 'CLP', 'CDF', 'DOP', 'FJD', 'GMD', 'GYD', 'ISK', 'IQD', 'JPY', 'KPW', 'LVL', 'CHF', 'MGA', 'MDL', 'MAD', 'NPR', 'NIO', 'PKR', 'PYG', 'SHP', 'SCR', 'SBD', 'LKR', 'THB', 'TRY', 'AED', 'VUV', 'YER', 'AFN', 'BDT', 'BRL', 'KHR', 'KMF', 'HRK', 'DJF', 'EGP', 'ETB', 'XPF', 'GHS', 'GNF', 'HKD', 'XDR', 'KES', 'KGS', 'LRD', 'MOP', 'MVR', 'MXN', 'NAD', 'NOK', 'PLN', 'RUB', 'SZL', 'TJS', 'TTD', 'UGX', 'UYU', 'VND', 'TND', 'UAH', 'UZS', 'TMT', 'GBP', 'ZMW', 'BTC', 'BYN', 'BMD', 'GGP', 'CLF', 'CUC', 'IMP', 'JEP', 'SVC', 'ZMK', 'XAG', 'ZWL'])
today_date = datetime.today().strftime('%Y-%m-%d')
delta = datetime.today() - timedelta(days=7)
previous_date = delta.strftime('%Y-%m-%d')
fromCurr = ""
toCurr = ""
historical_data = ""

@app.route('/', methods=["POST", "GET"])
def index():
    if request.method == "POST":
        os.environ["CURR_API"] = "63a43551a8683875884b"
        API = os.environ.get("CURR_API")
        fromCurr = request.form.get('fromCurr')
        toCurr = request.form.get('toCurr')
        if fromCurr and toCurr:
            try:
                url = f"https://free.currconv.com/api/v7/convert?q={fromCurr}_{toCurr}&compact=ultra&apiKey={API}"
                rates = requests.get(url).json()[f"{fromCurr}_{toCurr}"]
                return render_template('index.html', result=f"{rates} {toCurr}", currency=currencies, minimum=previous_date, maximum=today_date)
            except:
                flash("An error encountered, Please try again later", "danger")
                return redirect(url_for('index'))
        else:
            flash("An error encountered, Please try again later", "danger")
            return redirect(url_for('index'))
    return render_template('index.html', currency=currencies, minimum=previous_date, maximum=today_date)

@app.route('/history', methods=["POST", "GET"])
def history():
    os.environ["CURR_API"] = "63a43551a8683875884b"
    API = os.environ.get("CURR_API")
    fromcurr = request.args.get('from')
    tocurr = request.args.get('to')
    if fromcurr is None:
        fromcurr="USD"
    if tocurr is  None:
        tocurr="INR"
    exchange = fromcurr + '_' + tocurr
    selected_date = request.form.get('date')
    if selected_date:
        try:
            url = f"https://free.currconv.com/api/v7/convert?q={fromcurr}_{tocurr}&compact=ultra&date={selected_date}&endDate={today_date}&apiKey={API}"
            historical_data = requests.get(url).json()[exchange].items()
            print(historical_data)

            return render_template('index.html', currency=currencies, minimum=previous_date, maximum=today_date, historical_data=historical_data)
        except:
            flash("An error encountered, Please try again later", "danger")
            return redirect(url_for('index'))
    return render_template('index.html', currency=currencies, minimum=previous_date, maximum=today_date, exchange=exchange)
if __name__ == '__main__':
    app.run(debug=True)