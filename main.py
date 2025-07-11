from flask import Flask, render_template, request, jsonify
import google.cloud.webrisk_v1 as webrisk_v1
import os
import hashlib
import requests

from web_risk_requests.lookup import lookup_uri
from web_risk_requests.evaluate import evaluate_uri

import logging                      # ① std-lib logging
from google.cloud import logging as cloud_logging   # ② give it a different name

logging.basicConfig(level=logging.WARNING)

# optional: route std-lib logs to Cloud Logging
cloud_client = cloud_logging.Client()
cloud_client.setup_logging()        # after this, logging.info() goes to Cloud Run Logs

log = logging.getLogger(__name__)

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
    log.warning("Lookup request for url: " + url + " result: " + str(result))
    return jsonify(result)

@app.route('/evaluate', methods=['POST'])
def evaluate():
    url = request.form.get('url')
    if not url:
        return jsonify(error="No URL provided"), 400

    result = evaluate_uri(url)
    if "error" in result:
        return jsonify(result), 500
    log.warning("Evaluate request for url: " + url + " result: " + str(result))
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, port=8080)