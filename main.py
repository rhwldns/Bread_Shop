import os
from flask import Flask, g, session, redirect, request, url_for, jsonify, render_template
from requests_oauthlib import OAuth2Session
from dotenv import load_dotenv
from json import loads
from pymongo import MongoClient

coll = MongoClient('mongodb://localhost:27017/').Bread_Shop.user

load_dotenv()

OAUTH2_CLIENT_ID = 838262770830409748
OAUTH2_CLIENT_SECRET = os.getenv("SECRET")
OAUTH2_REDIRECT_URI = 'http://127.0.0.1:5000/callback'

API_BASE_URL = os.environ.get('API_BASE_URL', 'https://discordapp.com/api')
AUTHORIZATION_BASE_URL = API_BASE_URL + '/oauth2/authorize'
TOKEN_URL = API_BASE_URL + '/oauth2/token'

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = OAUTH2_CLIENT_SECRET

if 'http://' in OAUTH2_REDIRECT_URI:
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = 'true'

token = os.getenv("TOKEN")
def token_updater(token):
    session['oauth2_token'] = token


def make_session(token=None, state=None, scope=None):
    return OAuth2Session(
        client_id=OAUTH2_CLIENT_ID,
        token=token,
        state=state,
        scope=scope,
        redirect_uri=OAUTH2_REDIRECT_URI,
        auto_refresh_kwargs={
            'client_id': OAUTH2_CLIENT_ID,
            'client_secret': OAUTH2_CLIENT_SECRET,
        },
        auto_refresh_url=TOKEN_URL,
        token_updater=token_updater)

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/index.html')
def main2():
    return render_template('index.html')

@app.route('/desc.html')
def des():
    return render_template('desc.html')

@app.route('/oauth2')
def index():
    scope = request.args.get(
        'scope',
        'identify')
    discord = make_session(scope=scope.split(' '))
    authorization_url, state = discord.authorization_url(AUTHORIZATION_BASE_URL)
    session['oauth2_state'] = state
    return redirect(authorization_url)


@app.route('/callback')
def callback():
    if request.values.get('error'):
        return request.values['error']
    discord = make_session(state=session.get('oauth2_state'))
    token = discord.fetch_token(
        TOKEN_URL,
        client_secret=OAUTH2_CLIENT_SECRET,
        authorization_response=request.url)
    session['oauth2_token'] = token
    return redirect(url_for('.me'))


@app.route('/me')
def me():
    discord = make_session(token=session.get('oauth2_token'))
    user = discord.get(API_BASE_URL + '/users/@me').json()
    jj = dict(user)
    global user_id
    user_id = jj['id']

    if coll.find_one({"_id": str(user_id)}):
        pass
    else:
        _LENGTH = 12
        string_pool = string.ascii_letters + string.digits
        result = ""
        for i in range(_LENGTH):
            result += random.choice(string_pool)
        coll.insert_one({
            "_id": str(user_id),
            "uuid": str(result),
            "count": 0
        })
    return redirect(url_for('orderss'))

@app.route('/orders')
def orderss():
    return render_template('order.html')

@app.route('/post', methods=['POST'])
def _post():
    value = request.form['applyorder']
    result = '200'
    if user_id != None:

        if coll.find_one({'_id': str(user_id)}):

            find = {"_id": str(user_id)}
            set_data = {"$inc": {"count": 1}}

            coll.update_one(find, set_data)
        
        else:
            _LENGTH = 12
            string_pool = string.ascii_letters + string.digits
            result = ""
            for i in range(_LENGTH):
                result += random.choice(string_pool)
            coll.insert_one({
                "_id": str(user_id),
                "uuid": str(result),
                "count": 1
            })

        with open(f'Goods/{str(user_id)}.txt', 'w', encoding='UTF-8') as f:
            f.write(value)
        
        return render_template('done.html', STATE='Completed', S='주문이 완료되었습니다.')

    return redirect(url_for('index')) # Oauth2 페이지로 redirect


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
