from flask import Flask
from flask import request
import requests
import json

from projects.restApi.utils.config_util import get_config

app = Flask(__name__)
REDIRECT_URI = 'http://ec2-54-153-19-163.us-west-1.compute.amazonaws.com/redirect'


@app.route("/")
def main():
    return "Welcome!"


@app.route("/authorize")
def authorize():
    configs = get_config()
    slack_authorize_url = 'https://slack.com/oauth/authorize?client_id={}&scope=read&redirect_uri={}'
    client_id = configs['API_TOKENS']['CLIENT_ID']
    url = slack_authorize_url.format(client_id, REDIRECT_URI)
    resp = requests.get(url=url)
    return


@app.route("/redirect")
def redirect():
    code = request.args.get('code')
    configs = get_config()
    client_id = configs['API_TOKENS']['CLIENT_ID']
    client_secret = configs['API_TOKENS']['CLIENT_SECRET']
    url = 'https://slack.com/api/oauth.access?client_id={}&client_secret={}&code={}&redirect_uri={}'.format(
        client_id, client_secret, code, REDIRECT_URI)
    resp = requests.get(url).text
    resp_json = json.loads(resp)
    access_token = resp_json.get('access_token','')
    scope = resp_json.get('scope', '')
    return
