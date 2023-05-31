# UnlimitedGPT Documentation

A Python class for interacting with ChatGPT.

## Getting started
Make sure you install [Chrome](https://www.google.com/chrome/) or [Chromium](https://www.chromium.org/) before using this library, as it uses `undetected_chromedriver` to bypass Cloudflare's anti-bot protection, which requires Chrome/Chromium to be installed. 

## Installation

You can install the library from [PyPi](https://pypi.org/project/UnlimitedGPT/) using the following command:

### Normal Operating Systems
```sh
# Windows
pip install UnlimitedGPT -U

# Linux/macOS
pip3 install UnlimitedGPT -U
```

### Headless Linux Servers
```sh
# install chromium & X virtual framebuffer
sudo apt install chromium-browser xvfb
pip3 install UnlimitedGPT -U
```

### Google Colab
```sh
# install dependencies
!apt install chromium-browser xvfb
!pip install -U selenium_profiles UnlimitedGPT
```
```py
# install chromedriver
from selenium_profiles.utils.installer import install_chromedriver
install_chromedriver()
```

## Initialization

Create an instance of `ChatGPT`:
```py
from UnlimitedGPT import ChatGPT

session_token = "YOUR_SESSION_TOKEN"
conversation_id = "YOUR_CONVERSATION_ID"

chatbot = ChatGPT(
    session_token,
    conversation_id=conversation_id,
    proxy=None,
    chrome_args=None,
    disable_moderation=False,
    verbose=False,
)
```

## Parameters

- `session_token (str)`: The `__Secure-next-auth.session-token` cookie from https://chat.openai.com/chat.
- `conversation_id (Optional[int])`: The conversation ID. Defaults to `None`.
    - To obtain a conversation ID, click on any conversation, then take the part of the URL that comes after `https://chat.openai.com/c/`
        - Example: The conversation ID in the URL `https://chat.openai.com/c/aa4f2349-8090-42a8-b8dc-0d116ce6b712` is `aa4f2349-8090-42a8-b8dc-0d116ce6b712`.
- `proxy (Optional[str])`: The proxy to use. Defaults to `None`.
- `disable_moderation (bool)`: Whether to disable moderation or not. Defaults to `False`.
- `verbose (bool)`: Whether to print debug messages or not. Defaults to `False`.
- `headless (bool)`: Whether to run Chrome in headless mode or not. Defaults to `True`.
- `chrome_args: (list)`: The Chrome arguments to use. Defaults to `[]`.

## Obtaining the session token

1. Go to https://chat.openai.com/chat and open the developer tools by `F12`.
2. Find the `__Secure-next-auth.session-token` cookie in `Application` > `Storage` > `Cookies` > `https://chat.openai.com`.
3. Copy the value in the `Cookie Value` field.

![image](https://user-images.githubusercontent.com/19218518/206170122-61fbe94f-4b0c-4782-a344-e26ac0d4e2a7.png)

## Methods

### Remember to initialize the class first!
```py
from UnlimitedGPT import ChatGPT
api = ChatGPT(...)
```
### Sending a message
```py
message = api.send_message(
    "Hey ChatGPT!",
    input_mode="INSANT", # Can be INSTANT or SLOW
    input_delay=0.1 # Only used when input_mode is set to SLOW
)
print(message.response, message.conversation_id)
```
### Regenrating a response
```py
message = api.regenerate_response() # Regenerates the last response sent by ChatGPT
print(message.response, message.conversation_id)
```
### Resetting the conversation
```py
api.reset_conversation()
```
### Clearing all conversations
```py
api.clear_conversations()
```
### Switching themes
```py
api.switch_theme("DARK") # DARK, LIGHT, SYSTEM, OPPOSITE
```
### Getting session data
```py
data = api.get_session_data() # Returns SessionData object with some data, also User object inside of it
print(repr(data), repr(data.user))
```
### Toggling the chat history on/off
```py
api.toggle_chat_history(state = False) # If set to True, it enables it
```
### Logging out
```py
api.logout()
```
### Switching accounts
```py
api.switch_account("some-other-token")
```

## Frequently Asked Questions
- Why use this project instead of OpenAI's official API?
    - This project is open-source, and you can use it for free. OpenAI's official API is closed-source, and you have to pay to use it. In addition, this project has more features than OpenAI's official API.

- When is proper documentation coming?
    - Documentation of every function, class and object will be coming very soon. For now, all information of current exisiting functions can be found [here](#methods).

- What can I do with this project?
    - You can use this project to create your own chatbot, or to automate your conversations on https://chat.openai.com/chat.

- How do I suggest a feature?
    - You can suggest a feature by creating an issue [here](https://github.com/Sxvxgee/UnlimitedGPT/issues). Please make sure that the feature you are suggesting is not already implemented.

- How do I report a bug?
    - You can report a bug by creating an issue [here](https://github.com/Sxvxgee/UnlimitedGPT/issues). Please make sure that you are using the latest version of the library before reporting a bug. Also, please make sure that the bug you are reporting has not been reported before.

- Does this library support GPT-4?
    - No, GPT-4 is a paid model, and I haven't subscribed to it. So, unless someone sponsors the project by giving me a GPT-4 subscription, I won't be able to add support for GPT-4.

- When is interactive mode coming?
    - Interactive mode is not on my priority list right now. I will add it when I have time.

- Is this project affiliated with OpenAI?
    - No, this project is not affiliated with OpenAI in any way.

- Is this project safe to use?
    - Yes, this project is safe to use. However, if you are using this project to automate your conversations on https://chat.openai.com/chat, you might get banned. So, use this project at your own risk, as it is against the OpenAI's TOS.

## Closing Notes
This project is solely maintained by me, and I maintain this project and its dependencies in my free time. If you like this project, please consider starring it on GitHub.