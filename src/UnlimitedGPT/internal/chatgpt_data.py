from dataclasses import dataclass
from selenium.webdriver.common.by import By

@dataclass
class ChatGPTVariables:
    cf_challenge_form = (By.ID, 'challenge-form')

    chatgpt_textbox = (By.XPATH, '/html/body/div[1]/div[2]/div[2]/div/main/div[3]/form/div/div[2]/textarea')
    chatgpt_info_buttons = [
        (By.XPATH, '/html/body/div[3]/div/div/div/div[2]/div/div[2]/button'),
        (By.XPATH, '/html/body/div[3]/div/div/div/div[2]/div/div[2]/button[2]'),
        (By.XPATH, '/html/body/div[3]/div/div/div/div[2]/div/div[2]/button[2]'),
    ]
    chatgpt_textbox_send_button = '/html/body/div[1]/div[2]/div/div/main/div[3]/form/div/div[1]/button'
    chatgpt_streaming = (
        By.XPATH,
        '//div[starts-with(@class, "result-streaming markdown prose")]'
    )
    chatgpt_big_response = (By.XPATH, '//div[@class="flex-1 overflow-hidden"]//div[p]')
    chatgpt_small_response = (
        By.XPATH,
        '//div[starts-with(@class, "markdown prose w-full break-words")]',
    )
    chatgpt_alert = (By.XPATH, '//div[@role="alert"]')
    chatgpt_intro = (By.ID, 'headlessui-portal-root')
    chatgpt_login_btn = (By.XPATH, '//button[text()="Log in"]')
    chatgpt_login_h1 = (By.XPATH, '//h1[text()="Welcome back"]')
    chatgpt_logged_h1 = (By.XPATH, '//h1[text()="ChatGPT"]')

    chatgpt_new_chat = (By.LINK_TEXT, 'New chat')
    chatgpt_clear_convo = (By.LINK_TEXT, 'Clear conversations')
    chatgpt_confirm_clear_convo = (By.LINK_TEXT, 'Confirm clear conversations')
    chatgpt_chats_list_first_node = (
        By.XPATH,
        '//div[substring(@class, string-length(@class) - string-length("text-sm") + 1)  = "text-sm"]//a',
    )

    chatgpt_chat_url = 'https://chat.openai.com/chat'
