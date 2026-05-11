# -*- coding: utf-8 -*-
from langchain_community.chat_models.tongyi import ChatTongyi

def create_tongyi_llm():

    llm = ChatTongyi(
        model="qwen3-max",
        temperature=0
    )

    return llm