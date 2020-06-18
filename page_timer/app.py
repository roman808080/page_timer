from flask import Flask, jsonify, request
import requests

from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

SIMULTANEOUS_THREADS = 5

app = Flask(__name__)


def calculate_load_time(site_name):
    try:
        start = datetime.now()

        if requests.get(site_name).status_code != 200:
            raise Exception('Failed to load the site.')

        delta = datetime.now() - start
        return delta.total_seconds()
    except Exception as exc:
        return -1


@app.route("/")
def show_right_request_format():
    return ("Example of the request: "
            "curl --header \"Content-Type: application/json\" "
            "--request POST "
            "--data '{\"sites\": [\"http://google.com\", "
                                 "\"http://facebook.com\"]}' "
            "http://<url>/load-time")


@app.route("/load-time", methods=["POST"])
def load_time():
    sites = request.json.get('sites', [])
    results = []

    with ThreadPoolExecutor(max_workers=SIMULTANEOUS_THREADS) as executor:
        submitted_sites = []

        for site_name in sites:
            submitted_site = executor.submit(calculate_load_time, site_name)
            submitted_sites.append(submitted_site)

        for future in as_completed(submitted_sites):
            load_time = future.result()
            results.append({site_name: load_time})

    return jsonify({'sites': results})
