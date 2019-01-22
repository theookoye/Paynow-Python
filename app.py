"""Paynow implementation in python/flask, using the Paynow-SDK"""

from flask import Flask, render_template, url_for, jsonify, redirect, request
from pymongo import MongoClient
import paynow
import os

"""Create flask app object"""
app = Flask(__name__)

"""Create mongoDB database instance"""
client = MongoClient('localhost', 27017)
db = client['Kudziya']

"""Create a payment route, this receives details about payment from site"""


@app.route('/', methods=('GET', 'POST'))
@app.route('/pay', methods=('GET', 'POST'))
def pay():
    """Create a paynow object"""
    transaction = paynow.Paynow(
        "YOUR-ID", "YOUR-KEY", url_for('done'), url_for('pay'))

    if request.method == 'POST':
        ref = request.form['ref']
        print(ref)
        items = []

        # get corresponding details from database
        query = db.Products.find(
            {'Ref#': ref}, {'Name': '1', 'Price': '1'})

        for i in query:
            items.append(i['Name'])
            items.append(i['Price'])

        print(items)

        # setup payment variables before sending transaction
        payment = transaction.create_payment(ref, '')

        payment.add(items[0], items[1])  # add product to cart

        sendTransaction = transaction.send(
            payment)  # send transaction to paynow

        return redirect(sendTransaction.redirect_url)


@app.route('/done')
def done():
    return "<h2> Thank you for using paynow. </h2>"


if __name__ == '__main__':
    os.system(
        'start mongod --directoryperdb --dbpath C:/mongodb/data --bind_ip 127.0.0.1')
    app.run(port=5000, debug=True)
