from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

# Replace 'your_api_key' with the actual API key you obtain from your currency exchange API provider
API_KEY = '643044ce3191e2f66688e1b7'
BASE_URL = f'https://v6.exchangerate-api.com/v6/{API_KEY}/latest'

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        amount = request.form["amount"]
        from_currency = request.form["from_currency"].upper()  # Convert to uppercase for uniformity
        to_currency = request.form["to_currency"].upper()  # Convert to uppercase

        # Ensure the amount is a valid number
        try:
            amount = float(amount)
        except ValueError:
            error_message = "Please enter a valid number for the amount."
            return render_template("index.html", error_message=error_message)

        # Fetch exchange rates from the API
        url = f"{BASE_URL}/{from_currency}"
        try:
            response = requests.get(url)

            # Check if the response status code is successful
            if response.status_code != 200:
                error_message = "Failed to retrieve exchange rates. Please try again later."
                return render_template("index.html", error_message=error_message)

            # Try to parse the response as JSON
            data = response.json()

            if data.get("result") == "success":
                # Get the conversion rate for the target currency
                rate = data["conversion_rates"].get(to_currency)

                if rate:
                    converted_amount = round(amount * rate, 2)
                    return render_template("index.html", converted_amount=converted_amount,
                                           from_currency=from_currency, to_currency=to_currency)
                else:
                    error_message = f"Currency code '{to_currency}' not found. Please check and try again."
                    return render_template("index.html", error_message=error_message)
            else:
                error_message = "Failed to retrieve exchange rates. Please try again later."
                return render_template("index.html", error_message=error_message)

        except requests.exceptions.RequestException as e:
            # Handle any request-related exceptions (e.g., network issues)
            error_message = f"Error: {str(e)}. Please try again later."
            return render_template("index.html", error_message=error_message)

    return render_template("index.html")


if __name__ == "__main__":
    # Make sure to bind to the correct port when running on Heroku
    port = int(os.environ.get("PORT", 5000))  # Heroku provides this environment variable
    app.run(host="0.0.0.0", port=port, debug=False)
