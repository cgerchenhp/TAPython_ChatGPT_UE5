# -*- coding: utf-8 -*-
import requests
import asyncio
import json

import unreal
from Utilities.Utils import Singleton
from .config import API_KEY
import os
import ast


import openai

openai.api_key = API_KEY

# chameleon_chat
class ChatGPT35:
    def __init__(self, max_his:int):
        self.history = []
        self.role = {"role": "system", "content": "你是一个帮我写Unreal Python工具的智能助手"}
        self.max_his = max_his
        self.last_response = None

    def ask(self, question):
        messages = [self.role]
        messages.extend(self.history[-self.max_his:])
        messages.append({"role": "user", "content": question})

        print(f"ask: len(messages): {len(messages)}")
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages

        )
        self.history.append({"role": "user", "content": question})

        self.last_response = response
        answer = response.choices[0].message['content']
        self.history.append({"role": "assistant", "content": answer})

        print(f"use token: {response['usage']}")

        return answer


class chat(metaclass=Singleton):
    def __init__(self, jsonPath:str):
        self.jsonPath = jsonPath
        self.data = unreal.PythonBPLib.get_chameleon_data(self.jsonPath)
        self.ui_gpt = "GPT"
        self.ui_input = "Input"
        self.ui_status = "Status"
        self.history = []
        self.status_text = ""
        self.ai = ChatGPT35(15)

    def on_committed(self):
        self.on_send_click()

    def on_send_click(self):
        text = self.data.get_text(self.ui_input)

        print(f"on_send_click: {text}")
        answer = self.ai.ask(text)

        self.set_gpt_out(answer)

        self.set_status(str(self.ai.last_response))

        self.data.set_text('Input', '')

        self.get_json_from_content(answer)

    def on_combo_select(self, content):
        print(content)
        if content == "发送最小范例":
            projectFolder = unreal.SystemLibrary.get_project_directory()
            with open(os.path.join(projectFolder,"TA/TAPython/Python/Example/MinimalExample.json"), 'r',
                      encoding="UTF-8") as f:
                content = f.read()

        self.data.set_text('Input', content)


    def set_gpt_out(self, text):
        self.data.set_text(self.ui_gpt, text)

    def set_status(self, text):
        self.status_text = text + "\n"
        self.data.set_text(self.ui_status, self.status_text)

    def append_status(self, text):
        self.status_text += text + "\n"

        self.data.set_text(self.ui_status, self.status_text)



    def get_json_from_content(self, content:str):
        if "{" in content and "}" in content:
            content = content[content.find("{", 1) : content.rfind("}", 1) + 1]
            try:
                j = ast.literal_eval(content)
                if j:
                    projectFolder = unreal.SystemLibrary.get_project_directory()
                    with open(os.path.join(projectFolder, "TA/TAPython/Python/ChameleonSketch/ChameleonSketch.json"), 'w', encoding="UTF-8") as f:
                        f.write(content)
                print(f"NICE: json: {len(content)}")
            except Exception as e:
                unreal.log_warning(e)



