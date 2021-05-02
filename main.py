from sanic import Sanic
from sanic.response import json
from sanic_jinja2 import SanicJinja2
from index import bot
from flask import request

app = Sanic(name='Discord Bread Shop', register=False)
jinja = SanicJinja2(app, pkg_name="main")

@app.route("/")
async def index(request):
    return jinja.render("index.html", request)  

@app.route('/test')
async def test(request):
    return jinja.render("order.html", request)  


@app.route('/post', methods=['POST'])
async def post(request):
    value = request.form['test']
    print(str(value))

    u = await bot.fetch_user(443734180816486441)
    print(u)
    return await u.send(str(value))


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)