from flask import Flask
from flask import request
import requests
import json

from requests.models import Response
from projects.restApi.utils.config_util import get_config
from projects.restApi.utils.mongo_util import mongodb

app = Flask(__name__)
REDIRECT_URI = 'http://ec2-54-153-19-163.us-west-1.compute.amazonaws.com/redirect'
scope = 'chat:write:bot,users.profile:read'
access_collection = 'access'


@app.route("/authorize")
def authorize():
    configs = get_config()
    slack_authorize_url = 'https://slack.com/oauth/authorize?client_id={}&scope={}&redirect_uri={}'
    client_id = configs['API_TOKENS']['CLIENT_ID']
    url = slack_authorize_url.format(client_id, scope, REDIRECT_URI)
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
    res = Response()
    try:
        access_token = resp_json.get('access_token')
        scope = resp_json.get('scope')
        team_id = resp_json.get('team_id')
        user_id = resp_json.get('user_id')
        team_name = resp_json.get('team_name')
        relevant_fields = ['access_token', 'team_id', 'user_id', 'team_name']
        ok = resp_json.get('ok')
        if not ok:
            res.status_code = 400
            res._content = b'{"message":"not authorized"}'
            return res
        mongo = mongodb()
        col = mongo.get_collection(access_collection)
        access_doc = {key : resp_json[key] for key in relevant_fields}
        col.insert_one(access_doc)
        res.status_code = 200
        res._content = b'{"message":"ok"}'
        return res
    except:
        res.status_code = 500
        res._content = b'{"message":"server error"}'
        return res
