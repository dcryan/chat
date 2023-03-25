import os
import openai
from spinner import Spinner

spinner = Spinner()


openai.api_key = os.getenv("OPENAI_API_KEY")

try:
    messages = []

    # Ask the user to choose between the two models
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

    system_message = ""

    print()
    print("\033[92mSystem:\033[00m")
    if model == "1":
        system_message = "Hi, I'm CodeGPT. I'm a code completion model. I can help you write code. Let's get started."
    elif model == "2":
        system_message = "Hi, I'm TaxGPT. I'm a tax form completion model. I can help you fill out your tax forms. Let's get started."
    elif model == "3":
        system_message = input()
    else:
        system_message = "Hi, I'm ChatGPT. I'm a chat completion model. I can help you write messages. Let's get started."

    print("\033[92m  " + system_message + "\033[00m")
    print()

    messages.append({"role": "system", "content": system_message})

    while True:
        print("User:")
        user_message = input("  ")

        if user_message == "exit" or user_message == "quit":
            raise KeyboardInterrupt

        print()
        messages.append({"role": "user", "content": user_message})

        spinner.start()

        completion = openai.ChatCompletion.create(
          model="gpt-3.5-turbo",
          messages=messages,
          stream=True,
        )

        spinner.stop()

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


        assistant_message = "".join(collectedMessages)

        messages.append({"role": "assistant", "content": assistant_message})

except KeyboardInterrupt:
    print()
    print("👋bye")
    exit()
