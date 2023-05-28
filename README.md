# UnlimitedGPT

[![Downloads](https://static.pepy.tech/badge/unlimitedgpt)](https://pepy.tech/project/unlimitedgpt)
[![PyPi](https://img.shields.io/pypi/v/UnlimitedGPT.svg)](https://pypi.python.org/pypi/UnlimitedGPT)
[![License](https://img.shields.io/github/license/Sxvxgee/UnlimitedGPT.svg?color=green)](https://github.com/Sxvxgee/UnlimitedGPT/blob/main/LICENSE)

> This is a maintained, modified and improved package of the original [pyChatGPT](https://github.com/terry3041/pyChatGPT) package. The original package is in slow development and has many issues. This package is actively maintained and updated.

An unofficial Python wrapper for OpenAI's ChatGPT API

## Features

-   [x] Cloudflare's anti-bot protection bypass using `undetected_chromedriver`
-   [x] [Headless machines support](#how-do-i-get-it-to-work-on-headless-linux-server)
-   [x] [Google Colab support](#how-do-i-get-it-to-work-on-google-colab)
-   [x] Proxy support (only without basic auth)

## Getting Started

> This library is using only the `undetected_chromedriver` package to bypass Cloudflare's anti-bot protection. `requests` module is not used due to the complexity of the protection. **Please make sure you have [Google Chrome](https://www.google.com/chrome/) / [Chromium](https://www.chromium.org/) before using this wrapper.**

### Installation

```bash
pip install -U UnlimitedGPT
```

### Usage

#### Obtaining session_token

1. Go to https://chat.openai.com/chat and open the developer tools by `F12`.
2. Find the `__Secure-next-auth.session-token` cookie in `Application` > `Storage` > `Cookies` > `https://chat.openai.com`.
3. Copy the value in the `Cookie Value` field.

![image](https://user-images.githubusercontent.com/19218518/206170122-61fbe94f-4b0c-4782-a344-e26ac0d4e2a7.png)

#### Interactive mode

> Currently, interactive mode is not supported in this package. But it will be added in the future.

#### Import as a module

```python
from UnlimitedGPT import ChatGPT

session_token = 'abc123'  # `__Secure-next-auth.session-token` cookie from https://chat.openai.com/chat
api = ChatGPT(
    session_token, # Specify session token
    conversation_id='some-random-uuid', # Specify conversation ID (Defaults to None)
    proxy='https://proxy.example.com:8080', # Specify proxy (Defaults to None)
    chrome_args=['--window-size=1920,768'], # Specify chrome args (optional)
    disable_moderation=True, # Disable moderation (Defaults to False)
    verbose=True, # Verbose mode (Defaults to False)
)

message = api.send_message('Hello, world!')
print(message.response, message.conversation_id)

api.reset_conversation()  # reset the conversation
api.clear_conversations() # clear all conversations
api.switch_theme('DARK') # switch themes (DARK, LIGHT, SYSTEM, OPPOSITE)
data = api.get_session_data() # Returns SessionData object with some data, also User object inside of it
api.logout() # Logout from the session
api.switch_account("some-other-token") # Switch to another account
```

## Frequently Asked Questions

### When is proper documentation coming?
Documentation of every function, class and object will be coming very soon. For now, all information of current exisiting functions can be found [here](#import-as-a-module).

### How do I get it to work on headless linux server?

```bash
# install chromium & X virtual framebuffer
sudo apt install chromium-browser xvfb

# start your script
python3 your_script.py
```

### How do I get it to work on Google Colab?

It is normal for the seession to be crashed when installing dependencies. Just ignore the error and run your script.

```python
# install dependencies
!apt install chromium-browser xvfb
!pip install -U selenium_profiles UnlimitedGPT

# install chromedriver
from selenium_profiles.utils.installer import install_chromedriver
install_chromedriver()
```

## Insipration

This project is inspired by

-   [ChatGPT](https://github.com/acheong08/ChatGPT)
-   [chatgpt-api](https://github.com/transitive-bullshit/chatgpt-api)
-   [pyChatGPT](https://github.com/terry3041/pyChatGPT)

## Disclaimer

- This project is not affiliated with OpenAI in any way. Use at your own risk. I am not responsible for any damage caused by this project. Please read the [OpenAI Terms of Service](https://beta.openai.com/terms) before using this project.
- This project is not built from scratch by me, I just modified, improved and fixed the original code of [pyChatGPT](https://github.com/terry3041/pyChatGPT) since I noticed there were already some PRs and they were not responded to by the terry3041. I also added some new features to the package, and will keep on doing so.

## License

This project is licensed under the GPLv3 License - see the [LICENSE](LICENSE) file for details.

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=Sxvxgee/UnlimitedGPT&type=Date)](https://star-history.com/#Sxvxgee/UnlimitedGPT&Date)
