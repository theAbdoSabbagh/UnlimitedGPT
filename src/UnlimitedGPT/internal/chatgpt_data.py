from dataclasses import dataclass

from selenium.webdriver.common.by import By


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
    info_buttons = (
        (By.XPATH, "/html/body/div[3]/div/div/div/div[2]/div/div[2]/button"),
        (By.XPATH, "/html/body/div[3]/div/div/div/div[2]/div/div[2]/button[2]"),
        (By.XPATH, "/html/body/div[3]/div/div/div/div[2]/div/div[2]/button[2]"),
    )
    alert = (By.XPATH, '//div[@role="alert"]')
    intro = (By.ID, "headlessui-portal-root")

    # Responses and such
    streaming = (
        By.XPATH,
        '//div[starts-with(@class, "result-streaming markdown prose")]',
    )
    big_response = (By.XPATH, '//div[@class="flex-1 overflow-hidden"]//div[p]')
    small_response = (
        By.XPATH,
        '//div[starts-with(@class, "markdown prose w-full break-words")]',
    )
    textbox = (By.XPATH, '//*[@id="prompt-textarea"]')
    continue_regenerating = (
        By.XPATH,
        "/html/body/div[1]/div[1]/div[2]/div/main/div[3]/form/div/div[1]/div/button[2]",
    )
    regenerate_response = (
        By.XPATH,
        "/html/body/div[1]/div[1]/div[2]/div/main/div[3]/form/div/div[1]/div/button",
    )
    new_chat = (By.LINK_TEXT, "New chat")
    clear_chat = (By.LINK_TEXT, "Clear chat")

    # Menu buttons
    menu_button = (
        By.XPATH,
        "/html/body/div[1]/div[1]/div[1]/div/div/div/nav/div[4]/div/button",
    )
    menu_clear_conversations = (
        By.LINK_TEXT,
        "Clear conversations",
    )
    menu_confirm_clear_conversations = (By.LINK_TEXT, "Confirm clear conversations")
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

    # URLs
    chat_url = "https://chat.openai.com/chat"
