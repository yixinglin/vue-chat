import json
from flask import Flask, request
from flask_cors import CORS
from chatbot import ChatBot_GPT3_5T, BaseChatBot
import os
from login import login

app = Flask(__name__)

# 登陆
@app.route('/login', methods=['POST'])
def login_validate():
    data = json.loads(request.data)
    return login(**data)

# 聊天
@app.route('/chat3_5', methods=['POST'])
def chatgpt_request():
    data = json.loads(request.data)
    data['sys_prompt'] = BaseChatBot.decodeContent(data['sys_prompt'])
    bot = ChatBot_GPT3_5T(**data)
    resp = bot.send(data["prompt"])
    return resp

# 查询某个机器人的聊天记录
@app.route('/chat3_5/history/<bot_name>', methods=['GET'])
def chatgpt_history_request(bot_name):
    bot = ChatBot_GPT3_5T(bot_name)
    history = bot.query_history()
    encoded = BaseChatBot.encodeContent(json.dumps(history, ensure_ascii=False))
    return {"data": encoded}

# 获得所有聊天角色
@app.route('/chat3_5', methods=['GET'])
def chatgpt_all_chatbots():
    resp = {"data": ChatBot_GPT3_5T.query_all_chatbots()}
    return resp

# 获取所有对话
@app.route('/chat3_5/all_conversations', methods=['GET'])
def chatgpt_query_all_conversations():
    bots = chatgpt_all_chatbots()
    conversations = []
    for bot in bots['data']:
        botObj = ChatBot_GPT3_5T(bot)
        history = botObj.query_history()
        conversations.append({"bot_name": botObj.bot_name, "history": history})

    encoded = BaseChatBot.encodeContent(json.dumps(conversations, ensure_ascii=False))
    return {"data": encoded}

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
    port = 5000
    print("PORT: ", port)
    app.run(host='0.0.0.0', port=port)