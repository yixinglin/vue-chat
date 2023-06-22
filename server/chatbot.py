import base64
from typing import List
import openai
import os
import json
from urllib.parse import unquote

with open("api_key.txt", 'r') as f:
    openai.api_key = f.read()

class BaseChatBot:

    def __init__(self, bot_name: str,
                 model: str, temperature: float,
                 sys_prompt: str):
        os.makedirs("./conversation", exist_ok=True)
        self.bot_name = bot_name
        self.model = model
        self.temperature = temperature

        self.filename = f"./conversation/{bot_name}.json"
        if not os.path.exists(self.filename):
            with open(self.filename, 'w', encoding="utf-8") as f:
                s = json.dumps([{"role": "system", "content": sys_prompt}])
                f.write(s)

        with open(self.filename, 'r', encoding="utf-8") as f:
            self.message_history = json.load(f)

    def send(self):
        raise NotImplementedError

    def update_message_history_to_file(self):
        with open(self.filename, 'w', encoding='utf-8') as f:
            s = json.dumps(self.message_history)
            f.write(s)

    # def delete_message_history_file(self):
    #     if os.path.exists(self.filename):
    #         os.remove(self.filename)
    #     else:
    #         raise FileNotFoundError

    def limit_num_messages(self, messages: List):
        textlen = 0
        for i, m in enumerate(messages[::-1]):
            textlen += len(m['content'])
            if textlen >= 3500:
                break
        print("Text length: ", textlen)
        start = len(messages)-i-1
        return messages[start+1:]

    def create_completion(self, index=0):
        msgs = self.limit_num_messages(self.message_history)
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=msgs,
            temperature=self.temperature
        )
        return {"role": response.choices[index].message["role"],
                "content": response.choices[index].message["content"]}

    def query_history(self):
        return self.message_history

    @staticmethod
    def query_all_chatbots():
        res = os.listdir("./conversation")
        bots = [b.split('.')[0] for b in res]
        return bots

    @staticmethod
    def decodeContent(content):
        text = base64.b64decode(content)
        return text.decode('utf-8')

    @staticmethod
    def encodeContent(content):
        return base64.b64encode(bytes(content, 'utf-8')).decode()

class ChatBot_GPT3_5T(BaseChatBot):
    def __init__(self, bot_name, temperature=0.7, sys_prompt="You are a helpful assistant", *args, **kwargs):
        super(ChatBot_GPT3_5T, self).__init__(bot_name=bot_name, model="gpt-3.5-turbo",
                                              temperature=temperature, sys_prompt=sys_prompt)

    def send(self, prompt):
        usr_msg = {"role": "user", "content": self.decodeContent(prompt)}
        self.message_history.append(usr_msg)
        resp = self.create_completion(0)
        self.message_history.append(resp)
        self.update_message_history_to_file()
        resp["content"] = self.encodeContent(resp["content"])
        return resp


if __name__ == '__main__':

    cb = ChatBot_GPT3_5T("中国律师", sys_prompt="You are a teacher teaching German.")
    print(cb.message_history)
    print(cb.query_all_chatbots())
    for i in range(100):
        resp = cb.send(input("User: "))
        print(resp)
