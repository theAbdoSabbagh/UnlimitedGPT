import re
from typing import Optional
from time import sleep, time
from threading import Thread
from platform import system
from os import environ
from json import loads
from logging import getLogger, DEBUG, Formatter, StreamHandler
from weakref import finalize

from markdownify import markdownify
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
from undetected_chromedriver import ChromeOptions

from .internal.driver import ChatGPTDriver
from .internal.chatgpt_data import ChatGPTVariables as CGPTV
from .internal.objects import ChatGPTResponse

class ChatGPT:
    """
    A class for interacting with ChatGPT.

    Args:
    ----------
        session_token (str): The session token for authentication.
        conversation_id (str, optional): The conversation ID. Defaults to ''.
        proxy (Optional[str], optional): The proxy server URL. Defaults to None.
        disable_moderation (bool, optional): Whether to disable moderation. Defaults to True.
        verbose (bool, optional): Whether to enable verbose logging. Defaults to False.
        headless (bool, optional): Whether to run the browser in headless mode. Defaults to False.
        chrome_args (list, optional): Additional arguments for the Chrome browser. Defaults to [].
    
    Raises:
    ----------
        ValueError: If the session token is not provided.
        ValueError: If the proxy is invalid.
    """

    def __init__(
        self,
        session_token: str,
        conversation_id: str = '',
        proxy: Optional[str] = None,
        disable_moderation: bool = True,
        verbose: bool = False,
        headless: bool = False,
        chrome_args: list = [],
    ) -> None:
        self._session_token = session_token
        self._conversation_id = conversation_id
        self._proxy = proxy
        self._disable_moderation = disable_moderation
        self._headless = headless
        self._chrome_args = chrome_args
        self._clicked_buttons = False
        self._init_logger(verbose)

        if not self._session_token:
            raise ValueError("session_token is required")
        if self._proxy and not re.findall(
            r'(https?|socks(4|5)?):\/\/.+:\d{1,5}', self._proxy # type: ignore
        ):
            raise ValueError('Invalid proxy format')

        self._init_browser()
        finalize(self, self.__del__)

    def __del__(self) -> None:
        """
        Close the browser and display.
        """
        self._is_active = False
        if hasattr(self, 'driver'):
            self.logger.debug('Closing browser...')
            self.driver.quit()
        if hasattr(self, 'display'):
            self.logger.debug('Closing display...')
            self.display.stop()

    def _init_logger(self, verbose: bool) -> None:
        """
        Initialize the logger.

        Args:
        ----------
            verbose (bool): Whether to enable verbose logging.
        """
        self.logger = getLogger('pyChatGPT')
        self.logger.setLevel(DEBUG)
        if verbose:
            formatter = Formatter('[%(funcName)s] %(message)s')
            stream_handler = StreamHandler()
            stream_handler.setFormatter(formatter)
            self.logger.addHandler(stream_handler)
    
    def _init_browser(self) -> None:
        """
        Initialize the browser.

        Raises:
        ----------
            ValueError: If the proxy is invalid.
            ValueError: If the Chrome installation is not found.
            ValueError: If the virtual display is not found.

        Notes:
        ----------
            If the system is Linux and the DISPLAY environment variable is not set, a virtual display will be started.
        """
        if system() == 'Linux' and 'DISPLAY' not in environ:
            self.logger.debug('Starting virtual display...')
            try:
                from pyvirtualdisplay.display import Display
                self.display = Display()
                self.display.start()
            except ModuleNotFoundError:
                raise ValueError('Please install PyVirtualDisplay to start a virtual display by running `pip install PyVirtualDisplay`')
            except FileNotFoundError as e:
                if 'No such file or directory: \'Xvfb\'' in str(e):
                    raise ValueError('Please install Xvfb to start a virtual display by running `sudo apt install xvfb`')
                raise e

        self.logger.debug('Initializing browser...')
        
        options = ChromeOptions()
        options.add_argument('--window-size=1024,768')
        if self._proxy:
            options.add_argument(f'--proxy-server={self._proxy}')
        for arg in self._chrome_args:
            options.add_argument(arg)
        try:
            self.driver = ChatGPTDriver(options=options, headless=self._headless)
        except TypeError as e:
            if str(e) == 'expected str, bytes or os.PathLike object, not NoneType':
                raise ValueError('Chrome installation not found')
            raise e

        if self._session_token:
            self.logger.debug('Restoring session_token...')
            self.driver.execute_cdp_cmd(
                'Network.setCookie',
                {
                    'domain': 'chat.openai.com',
                    'path': '/',
                    'name': '__Secure-next-auth.session-token',
                    'value': self._session_token,
                    'httpOnly': True,
                    'secure': True,
                },
            )

        if self._disable_moderation:
            self.logger.debug('Blocking moderation...')
            self.driver.execute_cdp_cmd(
                'Network.setBlockedURLs',
                {'urls': ['https://chat.openai.com/backend-api/moderations']},
            )

        self.logger.debug('Ensuring Cloudflare cookies...')
        self._ensure_cf()

        self.logger.debug('Opening chat page...')
        self.driver.get(f'{CGPTV.chatgpt_chat_url}/{self._conversation_id}')
        self._check_blocking_elements()

        self._is_active = True
        Thread(target=self._keep_alive, daemon=True).start()

    def _keep_alive(self) -> None:
        """
        Keep the session alive by updating the local storage.
        """
        while self._is_active:
            self.logger.debug('Updating session...')
            payload = (
                '{"event":"session","data":{"trigger":"getSession"},"timestamp":%d}'
                % int(time())
            )
            try:
                self.driver.execute_script(
                    'window.localStorage.setItem("nextauth.message", arguments[0])',
                    payload,
                )
            except Exception as e:
                self.logger.debug(f'Failed to update session: {str(e)}')
            sleep(60)

    def _check_blocking_elements(self) -> None:
        """
        Check for blocking elements and dismiss them.
        """
        self.logger.debug('Looking for blocking elements...')
        try:
            intro = WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located(CGPTV.chatgpt_intro)
            )
            self.logger.debug('Dismissing intro...')
            self.driver.execute_script('arguments[0].remove()', intro)
        except TimeoutException:
            pass

        alerts = self.driver.find_elements(*CGPTV.chatgpt_alert)
        if alerts:
            self.logger.debug('Dismissing alert...')
            self.driver.execute_script('arguments[0].remove()', alerts[0])

    def _ensure_cf(self, retry: int = 3) -> None:
        """
        Ensure Cloudflare cookies are set.

        Args:
        ----------
            retry (int, optional): Number of retries. Defaults to 3.

        Raises:
        ----------
            TimeoutException: If the Cloudflare challenge fails.
        """
        self.logger.debug('Opening new tab...')
        original_window = self.driver.current_window_handle
        self.driver.switch_to.new_window('tab')

        self.logger.debug('Getting Cloudflare challenge...')
        self.driver.get('https://chat.openai.com/api/auth/session')
        try:
            WebDriverWait(self.driver, 10).until_not(
                EC.presence_of_element_located(CGPTV.cf_challenge_form)
            )
        except TimeoutException:
            self.logger.debug(f'Cloudflare challenge failed, retrying {retry}...')
            self.driver.save_screenshot(f'cf_failed_{retry}.png')
            if retry > 0:
                self.logger.debug('Closing tab...')
                self.driver.close()
                self.driver.switch_to.window(original_window)
                return self._ensure_cf(retry - 1)
            raise ValueError('Cloudflare challenge failed')
        self.logger.debug('Cloudflare challenge passed')

        self.logger.debug('Validating authorization...')
        response = self.driver.page_source
        if response[0] != '{':
            response = self.driver.find_element(By.TAG_NAME, 'pre').text
        response = loads(response)
        if (not response) or (
            'error' in response and response['error'] == 'RefreshAccessTokenError'
        ):
            raise ValueError('Invalid session token')
        self.logger.debug('Authorization is valid')

        self.logger.debug('Closing tab...')
        self.driver.close()
        self.driver.switch_to.window(original_window)

    def send_message(self, message: str) -> ChatGPTResponse:
        """
        Send a message to ChatGPT.

        Args:
        ----------
            message (str): Message to send.

        Returns:
        ----------
            ChatGPTResponse: Response from ChatGPT.

        Raises:
        ----------
            TimeoutException: If the message fails to send.
            ValueError: If the response is invalid.
            ValueError: If the response is not found.
        """
        self.logger.debug('Ensuring Cloudflare cookies...')
        self._ensure_cf()

        self.logger.debug('Sending message...')
        
        if not self._clicked_buttons:
            for button in CGPTV.chatgpt_info_buttons:
                btn = WebDriverWait(self.driver, 60).until(
                    EC.element_to_be_clickable(button)
                )
                btn.click()
            self._clicked_buttons = True

        textbox = WebDriverWait(self.driver, 60).until(
            EC.element_to_be_clickable(CGPTV.chatgpt_textbox)
        )
        # textbox.send_keys(message)
        self.driver.execute_script("arguments[0].value = arguments[1];", textbox, message)

        textbox.send_keys(Keys.ENTER)

        self.logger.debug('Waiting for completion...')
        WebDriverWait(self.driver, 240).until_not(
            EC.presence_of_element_located(CGPTV.chatgpt_streaming)
        )

        self.logger.debug('Getting response...')
        responses = self.driver.find_elements(*CGPTV.chatgpt_big_response)
        if responses:
            response = responses[-1]
            if 'text-red' in response.get_attribute('class'):
                self.logger.debug('Response is an error')
                raise ValueError(response.text)
        response = self.driver.find_elements(*CGPTV.chatgpt_small_response)
        try:
            response = response[-1]
        except IndexError:
            self.logger.debug('Response not found, resetting conversation...')
            self.reset_conversation()
            raise ValueError('Response not found')

        content = markdownify(response.get_attribute('innerHTML')).replace(
            'Copy code`', '`'
        )
        
        pattern = re.compile(
            r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'
        )
        matches = pattern.search(self.driver.current_url)
        if not matches:
            self.reset_conversation()
            WebDriverWait(self.driver, 60).until(
                EC.element_to_be_clickable(CGPTV.chatgpt_chats_list_first_node)
            ).click()
            sleep(0.5)
            matches = pattern.search(self.driver.current_url)
        try:
            conversation_id = matches.group() # type: ignore
        except:
            conversation_id = None
        return ChatGPTResponse(content, conversation_id)

    def reset_conversation(self) -> None:
        """
        Resets the conversation.
        """
        if not self.driver.current_url.startswith(CGPTV.chatgpt_chat_url):
            return self.logger.debug('Current URL is not chat page, skipping reset')

        self.logger.debug('Resetting conversation...')
        try:
            self.driver.find_element(*CGPTV.chatgpt_new_chat).click()
        except NoSuchElementException:
            self.logger.debug('New chat button not found')
            self.driver.save_screenshot('reset_conversation_failed.png')
