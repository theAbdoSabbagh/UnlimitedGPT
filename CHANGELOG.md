# UnlimitedGPT Changelog
All notable changes to this project will be documented in this file.

## [0.1.9.3] 2023/08/15
- Added check for platform to use command when on MacOS instead of left control.
- Added `pyperclip` to requirements.txt as it is a required library now.

## [0.1.9] 2023/08/10
- Updated selectors yet again.
- Added a smart solution to dismissing the onboarding box that pops out when logged into an account:
    - Instead of constantly using XPATHs to click the "Next" buttons and suffering as it sometimes just refuses to click, or when the website updates and the selectors are changed, I came up with the solution of adding an item to the `localStorage` of the ChatGPT website that marks the user as already seen the onboarding popup.
- Instead of the old, hard to maintain way of using XPATHs to get the response from ChatGPT, I've decided to use the copying machanism instead.
    - Clicking CTRL + SHIFT + C copies the last response from ChatGPT, so I've used that to our advantage.
- Removed continue generating mechanism as I just couldn't get a single case where there was a need to continue generating as ChatGPT now seems to write a lot more than before in a single message.
- Updated `ChatGPTResponse` object to have a boolean attribute called `failed` which indicates whether the library failed to get the response from ChatGPT Or not.
- Added an element visibility check to the custom `safe_click` function within the driver of UnlimitedGPT.
- Updated `requirements.txt` and the `README.md`.

## [0.1.8] 2023/08/08
> Been extremely busy so I couldn't maintain the project.
- Fixed `_check_blocking_elements` not working due to change in XPATH of buttons.
- Fixed typos in logging.
- Fixed regenerating the response.
- Fixed clearing chats.
- Updated `Account` object.
- Removed `Accounts` object.

## [0.1.7] 2023/06/26
- Fixed `send_message`, `regenerate_response`, `switch_theme`, `toggle_chat_history`, `regenerate_response` and more functions because of a new site updated.
- Updated some selectors.

## [0.1.6] 2023/06/13
- Fixed `reset_conversation` not working when the chat history and training is disabled.
- Added `_get_conversation_id` which is used in `send_message` to update the conversation ID. 
    - Thanks to [@ezyyeah](https://github.com/ezyyeah) for their awesome contribution!
- Added 8 new objects:
    - `Conversation`
    - `Conversations`
    - `Account`
    - `Accounts`
    - `DefaultAccount`
    - `Entitlement`
    - `LastActiveSubscription`
    - `SharedConversation`
    - `SharedConversations`
- Added `get_user_data` function: Gets the user data of the current session.
- Added `get_conversations` function: Gets the conversations of the current session.
- Added `DesiredCapabilities` to `ChatGPTDriver`. This makes getting the backend API data possible.
- Added `get_shared_conversations` function: Gets the shared conversations of the current session.

## [0.1.5.5] 2023/06/11
- Fixed `send_message` raising an exception when it fails to continue regenerating the response.
- Fixed `regenerate_response` raising an exception when it fails to continue regenerating the response.

## [0.1.5] 2023/06/11
- Added `continue_generating` parameter to `send_message` function to allow the user to continue generating the response of ChatGPT if the button was presented.
- Added `continue_generating` parameter to `regenerate_response` function to allow the user to continue generating the response of ChatGPT if the button was presented.
- Fixed `regenerate_response` docstring having the `Returns` section include the `Args` text.

## [0.1.4] 2023/06/06
- Fixed `send_message` not working due to yet another website update, which changed the XPATH of the textbox used for sending messages.
- Fixed `regenerate_response` not working due to yet another website update, which changed the XPATH of the button used for regenerating the response.
- Fixed `switch_account` raising `InvalidConversationID` exception since it would use the conversation ID set in the old session, which isn't accessible in the new session.
- Added `--disable-popup-blocking` argument to the driver to allow opening new tabs using `window.open();` JS function.
- Modified `regenerate_response` to markdownify the content of the message differently by not adding backslashes before the asterisks or underscores, and also by removing the newlines at the end of the string.
- Modified `switch_account` to return the new session data as a `SessionData` object.

## [0.1.3] 2023/06/04
- Added `preview.txt` file in the `docs` folder, which contains the text from the `preview.png` image.
- Added more `debug` logger messages.
- Added `switch_conversation` function to switch to a different conversation.
- Updated `preview.png` image in the `docs` folder.
- Removed the check for `session_token` when initializing `ChatGPT` as the parameter is required.
- Removed `chatgpt_` prefix from all data variables (XPATHs and other selectors).
- Modified `disable_moderation` default value to False.
- Modified `reset_conversation` to handle the button not being clicked correctly.
- Modified `send_message` to markdownify the content of the message differently by not adding backslashes before the asterisks or underscores, and also by removing the newlines at the end of the string.
- Modified most of selector variable names under `chatgpt_data`.
- Fixed `send_message` not working because of yet another website update, which changed many XPATHs including the textbox used for sending messages.
- Fixed `reset_conversation` not working, ever, because of not using the correct URL to check.
- Fixed `regenerate_response` outdated XPATH.

## [0.1.2.5] 2023/06/01
- Fixed `send_message` having the default value of `input_mode` having a typo. It was "INSANT" instead of "INSTANT".
- Fixed the driver opening up `https://chat.openai.com//` instead of `https://chat.openai.com/` resulting in the conversation ID not working.

## [0.1.2] 2023/05/31
- Removed `chatgpt_theme_selector` from `chatgpt_data` file.
- Removed `input_mode` and `input_delay` parameters from the `ChatGPT` class.
- Added `input_mode` and `input_delay` parameters to the `send_message` function.
- Fixed `send_message` not working when the conversation ID is not set.
- Fixed `switch_theme` not working because of improper parameter being passed to `find_element`.
- Fixed `toggle_data_control` not working because of using nonexisiten element selector.
- Started using `LINK_TEXT` selector instead of XPATH when trying to find menu button since some users may have a different amount of menu buttons.
- Modified `get_session_data` to open a new tab instead of opening the session over the tab that is used for ChatGPT.
- Modified `send_message` and `regenerate_response` to no longer try to get the conversation ID as there is no way of changing the conversation ID besides specifying it in the class, meaning it is better to just get the value that was set in the class previously.
- Updated the `preview.png` image in the `docs` folder.

## [0.1.1] 2023/05/31
- Applied custom driver function `safe_click` on all functions over `driver.click` to prevent errors, such as `StaleElementReferenceError`.
    - There is one `driver.click` in the code though that doesn't use `safe_click` as there is some checks before clicking, but it also implements the same error handling.
- Created new exceptions file with the main exception `UnlimitedGPTException` and `InvalidConversationID` which is raised when there is an alert saying the conversation ID is invalid.