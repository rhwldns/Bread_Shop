from flask import Flask, render_template, request
from waitress import serve
from discord.ext import commands
import discord
import os

load_dotenv()

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=['bs.', 'bs. '], help_command=None)

app = Flask(__name__)

@app.route("/")
def main():
    return render_template('index.html')

@app.route('/desc.html')
def desc():
    return render_template('desc.html')

@app.route('/index.html')
def index_html():
    return render_template('index.html')

@app.route('/test')
def test():
    return render_template('order.html')

@app.route('/post', methods=['POST'])
def post():
    value = request.form['test']
    return value

if __name__ == "__main__":
    bot.run(os.getenv("TOKEN"))
    serve(app, host="127.0.0.1", port=5000)
    print("Server is Ready.")
