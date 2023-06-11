# UnlimitedGPT Changelog
All notable changes to this project will be documented in this file.

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