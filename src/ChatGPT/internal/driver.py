import undetected_chromedriver as uc

class ChatGPTDriver(uc.Chrome):
    """
    Custom selenium driver for ChatGPT.
    ##### Still in development.
    """
    def __init__(self, options: uc.ChromeOptions, headless: bool = False):
        super().__init__(options=options, headless=headless)
