# from flask import Flask, render_template, request, redirect, url_for
# import stripe
# app = Flask(__name__)
# public_key = "pk_test_51NadRLFqVq6HkR6T1QVIl6S35zDZ0F91YxHGxybrzGMAezcaRHUtPIPYBixjguzql5Xdn08CdNB0KAAmRqFNYrpE00LjD70O6S"
# stripe.api_key = "sk_test_51NadRLFqVq6HkR6Txnzx9c98JRjpoIp4AoJjXgKFNNr9Zqz6jA2Ampx1veT5vdYde5wteD8e8WZaQyf9jexgeShV00FfUY3mAq"
# @app.route('/')
# def index():
#     return render_template('index.html', public_key=public_key)
# @app.route('/thankyou')
# def thankyou():
#     return render_template('thankyou.html')
# @app.route('/payment', methods=['POST'])
# def payment():
#     # customer
#     customer = stripe.Customer.create(
#         email=request.form['stripeEmail'],
#         source=request.form['stripeToken']
#     )
#     charge = stripe.Charge.create(
#         customer=customer.id,
#         amount=1999,
#         currency='usd',
#         description='donations'
#     )
#     return redirect(url_for('thankyou'))
# if __name__ == '__main__':
#     app.run()


from flask import Flask, request
# from pesapal import Pesapal
from pesapal_py.payments import PesaPal   #its either this one or the one above it


app = Flask(__name__)

consumer_key = "H/zloupuEvfe/1dMcE1mTnlMSzIVNa1q"
consumer_secret = "iv4Ee3iE+uFs5kOnB8qp+hRCNhM="
callback_url = "http://localhost:5000/pesapal_callback"
pesapal = PesaPal(consumer_key, consumer_secret)

@app.route("/create_order", methods=["POST"])
def create_order():
    try:
        # Extract form data
        amount = request.form.get("amount")
        description = request.form.get("description")
        reference = request.form.get("reference")
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        email = request.form.get("email")
        phone_number = request.form.get("phone_number")

        # Construct order data
        order_data = {
            "Amount": amount,
            "Description": description,
            "Type": "MERCHANT",
            "Reference": reference,
            "FirstName": first_name,
            "LastName": last_name,
            "Email": email,
            "PhoneNumber": phone_number
        }

        # Generate payment URL
        url = pesapal.post_direct_order(order_data)

        return url

    except Exception as e:
        return f"Error: {str(e)}", 500

@app.route("/pesapal_callback", methods=["GET"])
def pesapal_callback():
    try:
        pesapal_response = request.args
        pesapal_transaction_tracking_id = pesapal_response.get("pesapal_transaction_tracking_id")
        reference = pesapal_response.get("reference")

        # Check payment status using the Pesapal library
        payment_status = pesapal.query_payment_status(pesapal_transaction_tracking_id)

        # Handle the payment status (e.g., update order status in your database)
        # ...

        return f"Payment for reference {reference} is {payment_status}"

    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == "__main__":
    app.run()