# UnlimitedGPT Changelog

## [0.1.1] 2023/05/23
- Applied custom driver function `safe_click` on all functions over `driver.click` to prevent errors, such as `StaleElementReferenceError`.
    - There is one `driver.click` in the code though that doesn't use `safe_click` as there is some checks before clicking, but it also implements the same error handling.
- Created new exceptions file with the main exception `UnlimitedGPTException` and `InvalidConversationID` which is raised when there is an alert saying the conversation ID is invalid.