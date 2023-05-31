from dataclasses import dataclass
from selenium.webdriver.common.by import By

@dataclass
class ChatGPTVariables:
    cf_challenge_form = (By.ID, 'challenge-form')

    chatgpt_outer_html = (
        By.XPATH,
        "/html"
    )
    chatgpt_textbox = (
        By.XPATH,
        '/html/body/div[1]/div[2]/div[2]/div/main/div[3]/form/div/div/textarea'
    )
    chatgpt_info_buttons = [
        (By.XPATH, '/html/body/div[3]/div/div/div/div[2]/div/div[2]/button'),
        (By.XPATH, '/html/body/div[3]/div/div/div/div[2]/div/div[2]/button[2]'),
        (By.XPATH, '/html/body/div[3]/div/div/div/div[2]/div/div[2]/button[2]'),
    ]
    chatgpt_streaming = (
        By.XPATH,
        '//div[starts-with(@class, "result-streaming markdown prose")]'
    )
    chatgpt_big_response = (
        By.XPATH,
        '//div[@class="flex-1 overflow-hidden"]//div[p]'
    )
    chatgpt_small_response = (
        By.XPATH,
        '//div[starts-with(@class, "markdown prose w-full break-words")]',
    )
    chatgpt_alert = (
        By.XPATH,
        '//div[@role="alert"]'
    )
    chatgpt_intro = (
        By.ID,
        'headlessui-portal-root'
    )

    chatgpt_new_chat = (
        By.LINK_TEXT,
        'New chat'
    )
    chatgpt_chats_list_first_node = (
        By.XPATH,
        '//div[substring(@class, string-length(@class) - string-length("text-sm") + 1)  = "text-sm"]//a',
    )
    chatgpt_menu_button = (
        By.XPATH,
        "/html/body/div[1]/div[2]/div[1]/div/div/div/nav/div[3]/div/button"
    )
    chatgpt_menu_clear_conversations = (
        # By.XPATH,
        # "/html/body/div[1]/div[2]/div[1]/div/div/div/nav/div[3]/div/div/nav/a[2]"
        By.LINK_TEXT,
        'Clear conversations'
    ) # Confirm button is the same path
    chatgpt_menu_settings_button = (
        # By.XPATH,
        # "/html/body/div[1]/div[2]/div[1]/div/div/div/nav/div[3]/div/div/nav/a[3]"
        By.LINK_TEXT,
        'Settings'
    )
    chatgpt_regenerate_response_button = (
        By.XPATH,
        "/html/body/div[1]/div[2]/div[2]/div/main/div[3]/form/div/div[1]/div/button"
    )
    chatgpt_theme_select = (
        By.CSS_SELECTOR,
        'select.rounded'
    )
    chatgpt_data_controls_button = (
        By.CSS_SELECTOR,
        'button[data-state="inactive"][id^="radix-"][id$="-trigger-DataControls"]'
    )

    chatgpt_chat_url = 'https://chat.openai.com/'
