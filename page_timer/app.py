from flask import Flask, jsonify, request
import requests

from datetime import datetime

app = Flask(__name__)


def calculate_time_for_site(site_name):
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
            "--data '{\"sites\": [\"http://google.com\", \"http://facebook.com\"]}' "
            "http://<url>/time-load")


@app.route("/time-load", methods=["POST"])
def time_load():
    sites = request.json.get('sites', [])
    results = []

    for site_name in sites:
        load_time = calculate_time_for_site(site_name=site_name)
        results.append({site_name: load_time})

    return jsonify({'sites': results})
