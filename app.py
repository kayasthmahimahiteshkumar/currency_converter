from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('converter.html')

@app.route('/convert', methods=["POST"])
def convert():
    try:
        amount = float(request.form["amount"])
        from_currency = request.form["from_currency"]
        to_currency = request.form["to_currency"]

        url = f"https://api.exchangerate-api.com/v4/latest/{from_currency.upper()}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            rate = data['rates'].get(to_currency.upper())
            if rate:
                converted_amount = round(amount * rate, 2)
                result = f"{amount} {from_currency.upper()} = {converted_amount} {to_currency.upper()}"
            else:
                result = "Invalid TO currency code."
        else:
            result = "Invalid FROM currency code."

    except Exception as e:
        result = f"Error: {str(e)}"

    return render_template("converter.html", result=result)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Use 5000 as fallback
    app.run(host="0.0.0.0", port=port)
