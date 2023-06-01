# UnlimitedGPT Changelog
All notable changes to this project will be documented in this file.

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