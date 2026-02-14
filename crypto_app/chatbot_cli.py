# -*- coding: utf-8 -*-
from chatbot import chatbot_response

def main():
    print("Crypto Chatbot (type 'exit' to quit)")
    while True:
        try:
            q = input("> ").strip()
        except EOFError:
            break
        if q.lower() in {"exit", "quit"}:
            break
        print(chatbot_response(q))

if __name__ == "__main__":
    main()
