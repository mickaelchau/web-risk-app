from flask import Flask, render_template, request, jsonify
import google.cloud.webrisk_v1 as webrisk_v1
import os
import hashlib
import requests

from web_risk_requests.lookup import lookup_uri
from web_risk_requests.evaluate import evaluate_uri


app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/lookup', methods=['POST'])
def lookup():
    url = request.form.get('url')
    if not url:
        return jsonify(error="No URL provided"), 400

    result = lookup_uri(url)
    if "error" in result:
        return jsonify(result), 500
    print("Lookup request for url: " + url + " result: " + str(result))
    return jsonify(result)

@app.route('/evaluate', methods=['POST'])
def evaluate():
    url = request.form.get('url')
    if not url:
        return jsonify(error="No URL provided"), 400

    result = evaluate_uri(url)
    if "error" in result:
        return jsonify(result), 500
    print("Evaluate request for url: " + url + " result: " + str(result))
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, port=8080)