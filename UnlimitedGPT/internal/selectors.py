from dataclasses import dataclass

from selenium.webdriver.common.by import By

ChatGPTModels = [
    "",
    "?model=text-davinci-002-render-sha",
    "?model=gpt-4",
    "?model=gpt-4-code-interpreter",
    "?model=gpt-4-plugins",
    "?model=gpt-4-dalle"
]

@dataclass
class ChatGPTVariables:
    # Other
    outer_html = (By.XPATH, "/html")
    cf_challenge_form = (By.ID, "challenge-form")
    chats_list_first_node = (
        By.XPATH,
        '//div[substring(@class, string-length(@class) - string-length("text-sm") + 1)  = "text-sm"]//a',
    )

    # Popups and such
    alert = (By.XPATH, '//div[@role="alert"]')
    intro = (By.ID, "headlessui-portal-root")

    # Responses and such
    streaming = (
        By.XPATH,
        '//div[starts-with(@class, "result-streaming markdown prose")]',
    )
    potential_error_response = (By.XPATH, '//div[@class="flex-1 overflow-hidden"]//div[p]')
    normal_response = (
        By.XPATH,
        '//*[@id="__next"]/div[1]/div[2]/div/main/div[1]/div/div/div/div[2]/div/div[2]/div[1]/div/div/p'
    )
    textbox = (By.XPATH, '//*[@id="prompt-textarea"]')
    regenerate_response = (
        By.XPATH,
        "/html/body/div[1]/div[1]/div[2]/div/main/div[2]/form/div/div[1]/div/div[2]/div/button",
    )
    new_chat = (By.LINK_TEXT, "New chat")
    clear_chat = (By.LINK_TEXT, "Clear chat")

    # Menu buttons
    menu_button = (
        By.XPATH,
        "/html/body/div[1]/div[1]/div[1]/div/div/div/nav/div[4]/div/button",
    )
    menu_clear_conversations = (
        By.XPATH,
        "//div[contains(text(), 'Clear all chats')]/following-sibling::button"
    )
    menu_confirm_clear_conversations = (
        By.XPATH,
        '//button[@class="btn relative btn-primary"]/div[text()="Confirm deletion"]'
    )
    menu_settings = (
        By.LINK_TEXT,
        "Settings",
    )
    theme_button = (By.CSS_SELECTOR, "button[role='combobox']")
    data_controls = (
        By.CSS_SELECTOR,
        'button[data-state="inactive"][id^="radix-"][id$="-trigger-DataControls"]',
    )
    shared_links_manage = (
        By.XPATH,
        "//button[.//div[text()='Manage']]"
    )
    send_message_button = (
        By.CSS_SELECTOR, 
        'button[data-testid="send-button"]'
    )

    # URLs
    chat_url = "https://chat.openai.com/chat"
