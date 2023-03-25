#!/usr/bin/env python3

import os
import openai
import tiktoken
from spinner import Spinner

encoding = tiktoken.get_encoding("cl100k_base")
spinner = Spinner()


openai.api_key = os.getenv("OPENAI_API_KEY")


def print_info(messages):
    token_length = 0
    for message in messages:
        token_length += len(encoding.encode(message["content"]))

    # light grey color
    print("\033[90m" + str(token_length) + " tokens" + "\033[00m")
    print("\033[90m--------------------\033[00m")
    print()


def get_model():
    # Ask the user to choose between the models
    print("Choose a model:")
    print("0. ChatGPT (default)")
    print("1. CodeGPT")
    print("2. TaxGPT")
    print("3. Custom")
    print()
    model = input()

    # delete the user's input and the previous print statements
    print("\033[A                             \033[A")
    print("\033[A                             \033[A")
    print("\033[A                             \033[A")
    print("\033[A                             \033[A")
    print("\033[A                             \033[A")
    print("\033[A                             \033[A")
    print("\033[A                             \033[A")

    return model

def get_system_message(model):
    system_message = ""

    print()
    print("\033[92mSystem:\033[00m")
    if model == "1":
        system_message = "Hi, I'm CodeGPT. I'm a code completion model. I can help you write code. Let's get started."
    elif model == "2":
        system_message = "Hi, I'm TaxGPT. I'm a tax form completion model. I can help you fill out your tax forms. Let's get started."
    elif model == "3":
        system_message = input("  ")
    else:
        system_message = "Hi, I'm ChatGPT. I'm a chat completion model. I can help you write messages. Let's get started."

    print("\033[92m  " + system_message + "\033[00m")
    print()

    return system_message


def get_user_input():
    print("User:")
    user_message = input("  ")
    print()

    if user_message == "exit" or user_message == "quit":
        raise KeyboardInterrupt

    return user_message


def get_assistant_message(completion):
    collectedMessages = []

    print("\033[96mAssistant:\033[00m")
    print("  ", end="")
    for chunk in completion:
        delta = chunk['choices'][0]['delta']
        if "content" in delta:
            content = delta['content']
            collectedMessages.append(content)
            print("\033[96m" + content + "\033[00m", end="")
    print()
    print()

    return "".join(collectedMessages)



def main():
    try:
        model = get_model()
        messages = []

        system_message = get_system_message(model)
        messages.append({"role": "system", "content": system_message})

        print_info(messages)

        while True:
            user_message = get_user_input()
            messages.append({"role": "user", "content": user_message})

            print_info(messages)

            try:
                spinner.start()

                completion = openai.ChatCompletion.create(
                  model="gpt-3.5-turbo",
                  messages=messages,
                  stream=True,
                )
            except Exception as e:
                print(e)
                print("Error: Something went wrong. Please try again.")
                exit()
            finally:
                spinner.stop()

            assistant_message = get_assistant_message(completion)
            messages.append({"role": "assistant", "content": assistant_message})

            print_info(messages)

    except KeyboardInterrupt:
        print()
        print("👋bye")
        exit()


if __name__ == "__main__":
    main()
