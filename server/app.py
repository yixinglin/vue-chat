import json
import os
import openai
from flask import Flask, request
from chatbot import ChatBot_GPT3_5T

app = Flask(__name__)

@app.route('/')
def index():
    return {
        "msg": "success",
        "data": "Welcome to use flask!"
    }

@app.route('/user/<u_id>')
def user_info(u_id):
    return {
        "msg": "success",
        "data": {
            "id": u_id,
            "username": 'yuz',
            "age": 18
        }
    }

@app.route('/chat3_5', methods=['POST'])
def chatgpt_request():
    data = json.loads(request.data)
    bot = ChatBot_GPT3_5T(**data)
    resp = bot.send(data["prompt"])
    return resp

@app.route('/chat3_5/history/<bot_name>', methods=['GET'])
def chatgpt_history_request(bot_name):
    bot = ChatBot_GPT3_5T(bot_name)
    history = bot.query_history()
    return history

@app.route('/chat3_5', methods=['GET'])
def chatgpt_all_chatbots():
    resp = {"chatbots": ChatBot_GPT3_5T.query_all_chatbots()}
    return resp



if __name__ == '__main__':
    app.run()