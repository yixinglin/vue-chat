import json
from flask import Flask, request
from flask_cors import CORS
from chatbot import ChatBot_GPT3_5T
import os
app = Flask(__name__)

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
    return {"data": history}

@app.route('/chat3_5', methods=['GET'])
def chatgpt_all_chatbots():
    resp = {"data": ChatBot_GPT3_5T.query_all_chatbots()}
    return resp

@app.route('/chat3_5/all_conversations', methods=['GET'])
def chatgpt_query_all_conversations():
    bots = chatgpt_all_chatbots()
    conversations = []
    for bot in bots['data']:
        botObj = ChatBot_GPT3_5T(bot)
        history = botObj.query_history()
        conversations.append({"bot_name": botObj.bot_name, "history": history})
    return {"data": conversations}

# Add a chatbot

# Delete a chatbot
@app.route('/chat3_5/delete/<bot_name>', methods=['GET'])
def chatgpt_delete_chatbot(bot_name):
    filename = f'./conversation/{bot_name}'
    if os.path.exists(filename):
        os.remove(filename)
        return {"data": "ChatBot deleted"}
    else:
        return {"data": "FileNotFound error!"}

if __name__ == '__main__':
    CORS(app)
    app.run(host='0.0.0.0', port='5000')