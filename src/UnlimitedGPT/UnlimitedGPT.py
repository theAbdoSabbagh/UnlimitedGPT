import re
from json import loads
from logging import DEBUG, Formatter, StreamHandler, getLogger
from os import environ
from platform import system
from threading import Thread
from time import sleep, time
from typing import Literal, Optional
from weakref import finalize

from markdownify import markdownify
from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
    TimeoutException,
)
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from undetected_chromedriver import ChromeOptions

from .internal.chatgpt_data import ChatGPTVariables as CGPTV
from .internal.driver import ChatGPTDriver
from .internal.exceptions import InvalidConversationID
from .internal.objects import ChatGPTResponse, Conversations, SessionData, SharedConversations, User, Accounts

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
        InvalidConversationID: If the conversation ID is invalid.
        ValueError: If the session token is not provided.
        ValueError: If the proxy is invalid.
    """

    def __init__(
        self,
        session_token: str,
        conversation_id: str = "",
        proxy: Optional[str] = None,
        disable_moderation: bool = False,
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
        self._history_and_training_enabled = True
        self._init_logger(verbose)

        if self._proxy and not re.findall(
            r"(https?|socks(4|5)?):\/\/.+:\d{1,5}", self._proxy  # type: ignore
        ):
            raise ValueError("Invalid proxy format")

        self._init_browser()
        finalize(self, self.__del__)

    def __del__(self) -> None:
        """
        Close the browser and display.
        """
        self._is_active = False
        if hasattr(self, "driver"):
            self.logger.debug("Closing browser...")
            self.driver.quit()
        if hasattr(self, "display"):
            self.logger.debug("Closing display...")
            self.display.stop()

    def _get_out_of_menu(self) -> None:
        """
        Get out of any menu present.
        """
        for i in range(5):
            # First escape click is to remove the options menu
            # Second escape click is to get out of the settings menu
            # The rest are just to be safe
            self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)

    def _init_logger(self, verbose: bool) -> None:
        """
        Initialize the logger.

        Args:
        ----------
            verbose (bool): Whether to enable verbose logging.
        """
        self.logger = getLogger("pyChatGPT")
        self.logger.setLevel(DEBUG)
        if verbose:
            formatter = Formatter("[%(funcName)s] %(message)s")
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
        if system() == "Linux" and "DISPLAY" not in environ:
            self.logger.debug("Starting virtual display...")
            try:
                from pyvirtualdisplay.display import Display

                self.display = Display()
                self.display.start()
            except ModuleNotFoundError:
                raise ValueError(
                    "Please install PyVirtualDisplay to start a virtual display by running `pip install PyVirtualDisplay`"
                )
            except FileNotFoundError as e:
                if "No such file or directory: 'Xvfb'" in str(e):
                    raise ValueError(
                        "Please install Xvfb to start a virtual display by running `sudo apt install xvfb`"
                    )
                raise e

        self.logger.debug("Initializing browser...")

        options = ChromeOptions()
        options.add_argument("--window-size=1024,768")
        options.add_argument("--disable-popup-blocking")
        if self._proxy:
            options.add_argument(f"--proxy-server={self._proxy}")
        for arg in self._chrome_args:
            options.add_argument(arg)
        try:
            self.driver = ChatGPTDriver(options=options, headless=self._headless)
        except TypeError as e:
            if str(e) == "expected str, bytes or os.PathLike object, not NoneType":
                raise ValueError("Chrome installation not found")
            raise e

        if self._session_token:
            self.logger.debug("Restoring session_token...")
            self.driver.execute_cdp_cmd(
                "Network.setCookie",
                {
                    "domain": "chat.openai.com",
                    "path": "/",
                    "name": "__Secure-next-auth.session-token",
                    "value": self._session_token,
                    "httpOnly": True,
                    "secure": True,
                },
            )

        if self._disable_moderation:
            self.logger.debug("Blocking moderation...")
            self.driver.execute_cdp_cmd(
                "Network.setBlockedURLs",
                {"urls": ["https://chat.openai.com/backend-api/moderations"]},
            )

        self.logger.debug("Ensuring Cloudflare cookies...")
        self._ensure_cf()

        self.logger.debug("Opening chat page...")
        self.driver.get(f"{CGPTV.chat_url}/{self._conversation_id}")
        self._check_blocking_elements()

        self._is_active = True
        Thread(target=self._keep_alive, daemon=True).start()

    def _keep_alive(self) -> None:
        """
        Keep the session alive by updating the local storage.
        """
        while self._is_active:
            self.logger.debug("Updating session...")
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
                self.logger.debug(f"Failed to update session: {str(e)}")
            sleep(60)

    def _check_blocking_elements(self) -> None:
        """
        Check for blocking elements and dismiss them.
        """
        self.logger.debug("Looking for blocking elements...")
        try:
            intro = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(CGPTV.intro)
            )
            self.logger.debug("Dismissing intro...")
            self.driver.execute_script("arguments[0].remove()", intro)
        except TimeoutException:  # type: ignore
            pass

        alerts = self.driver.find_elements(*CGPTV.alert)
        if alerts:
            if "unable to load conversation" in alerts[0].text.lower():
                raise InvalidConversationID(alerts[0].text)
            self.logger.debug("Dismissing alert...")
            self.driver.execute_script("arguments[0].remove()", alerts[0])

        if not self._clicked_buttons:
            for button in CGPTV.info_buttons:
                self.driver.safe_click(button, timeout=60)
            self._clicked_buttons = True

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
        self.logger.debug("Opening new tab...")
        original_window = self.driver.current_window_handle
        self.driver.switch_to.new_window("tab")

        self.logger.debug("Getting Cloudflare challenge...")
        self.driver.get("https://chat.openai.com/api/auth/session")
        try:
            WebDriverWait(self.driver, 10).until_not(
                EC.presence_of_element_located(CGPTV.cf_challenge_form)
            )
        except TimeoutException:  # type: ignore
            self.logger.debug(f"Cloudflare challenge failed, retrying {retry}...")
            if retry > 0:
                self.logger.debug("Closing tab...")
                self.driver.close()
                self.driver.switch_to.window(original_window)
                return self._ensure_cf(retry - 1)
            raise ValueError("Cloudflare challenge failed")
        self.logger.debug("Cloudflare challenge passed")

        self.logger.debug("Validating authorization...")
        response = self.driver.page_source
        if response[0] != "{":
            response = self.driver.find_element(By.TAG_NAME, "pre").text
        response = loads(response)
        if (not response) or (
            "error" in response and response["error"] == "RefreshAccessTokenError"
        ):
            raise ValueError("Invalid session token")
        self.logger.debug("Authorization is valid")

        self.logger.debug("Closing tab...")
        self.driver.close()
        self.driver.switch_to.window(original_window)

    def _continue_generating(self, timeout: int) -> Optional[str]:
        """
        Continue generating the response.

        Args:
        ----------
            timeout (int): Time to wait for the message to continue regenerating before timing out.

        Returns:
        ----------
            Optional[str]: The newly generated response.
        """
        self.logger.debug("Continuing generating...")
        # Click "Continue generating" button
        continue_response_clicked = self.driver.safe_click(
            CGPTV.continue_regenerating, timeout=5
        )
        if not continue_response_clicked:
            self.logger.debug("Could not click continue regenerating button")
            return None

        # Get the response, same way as send_message without the part of sending the message
        self.logger.debug("Waiting for completion...")
        try:
            WebDriverWait(self.driver, timeout).until_not(
                EC.presence_of_element_located(CGPTV.streaming)
            )
        except:
            self.logger.debug("Could not continue generating")
            return None

        self.logger.debug("Getting response...")
        responses = self.driver.find_elements(*CGPTV.big_response)
        if responses:
            response = responses[-1]
            if "text-red" in response.get_attribute("class"):
                self.logger.debug("Response is an error")
                return None
        response = self.driver.find_elements(*CGPTV.small_response)
        try:
            response = response[-1]
        except IndexError:
            self.logger.debug("Response not found, resetting conversation...")
            self.reset_conversation()
            return None

        content = (
            markdownify(
                response.get_attribute("innerHTML"),
                escape_asterisks=False,
                escape_underscores=False,
            )
            .replace("Copy code`", "`")
            .rstrip("\n")
        )

        self.logger.debug("Continued regenerating the response")
        return content

    def _get_conversation_id(self):
        """
        Gets the conversation ID.
        """
        logs_raw = self.driver.get_log("performance")

        conv_response_id = next(
            log_["params"]["requestId"]
            for log_ in reversed([loads(lr["message"])["message"] for lr in logs_raw])
            if
            log_["method"] == "Network.responseReceived"
            # and json
            and "json" in log_["params"]["response"]["mimeType"]
            # and status 200
            and log_["params"]["response"]["status"] == 200
            # and conversations
            and "/backend-api/conversations" in log_["params"]["response"]["url"]
        )

        ret = self.driver.execute_cdp_cmd("Network.getResponseBody", {"requestId": conv_response_id})

        self._conversation_id = loads(ret["body"])["items"][0]["id"]

        self.logger.debug(f"Conversation id: {self._conversation_id}")

    def _open_shared_conversations_popup(self):
        """
        Opens the shared conversations popup.
        """
        self.logger.debug("Opening shared conversations popup...")
        try:
            menu_button_clicked = self.driver.safe_click(CGPTV.menu_button)
            if not menu_button_clicked:
                self.logger.debug("Could not click menu button")
                return self._get_out_of_menu()

            self.logger.debug("Clicked menu button")

            settings_button_clicked = self.driver.safe_click(CGPTV.menu_settings)
            if not settings_button_clicked:
                self.logger.debug("Could not click settings button")
                return self._get_out_of_menu()

            self.logger.debug("Clicked settings button")

            # Click "Data controls" button
            data_controls_clicked = self.driver.safe_click(
                CGPTV.data_controls, timeout=60
            )
            if not data_controls_clicked:
                self.logger.debug("Could not click data controls button")
                return self._get_out_of_menu()
            
            self.logger.debug("Clicked data controls button")

            # Click the "Manage" button for Shared Links
            shared_links_manage_clicked = self.driver.safe_click(
                CGPTV.shared_links_manage, timeout=60
            )
            if not shared_links_manage_clicked:
                self.logger.debug("Could not click shared links manage button")
                return self._get_out_of_menu()

            self.logger.debug("Clicked shared links manage button")
        except:
            self.logger.debug("Could not open shared conversations popup")

        return self._get_out_of_menu()

    def get_user_data(self) -> Optional[Accounts]:
        """
        Gets the user data.

        Returns
        ---------
            Optional[Accounts]: a list of the accounts.
        """
        self.logger.debug("Getting user data...")

        logs_raw = self.driver.get_log("performance")

        datas = (
            log_["params"]["requestId"]
            for log_ in reversed([loads(lr["message"])["message"] for lr in logs_raw])
            if (
                log_["method"] == "Network.responseReceived"
                and "json" in log_["params"]["response"]["mimeType"]
                and int(log_["params"]["response"]["status"]) == 200
                and "backend-api/accounts/check/" in log_["params"]["response"]["url"]
            )
        )
        try:
            data = next(datas)
        except StopIteration:
            self.logger.debug("Could not find user data")
            return None

        ret = self.driver.execute_cdp_cmd("Network.getResponseBody", {"requestId": data})

        response_data = loads(ret["body"])

        return Accounts(response_data)

    def get_conversations(self) -> Conversations:
        """
        Get a list of conversations.

        Returns:
        ----------
            Conversations: A list of conversations.
        """
        self.logger.debug("Getting conversations...")
        logs_raw = self.driver.get_log("performance")

        datas = (
            log_["params"]["requestId"]
            for log_ in reversed([loads(lr["message"])["message"] for lr in logs_raw])
            if (
                log_["method"] == "Network.responseReceived"
                and "json" in log_["params"]["response"]["mimeType"]
                and log_["params"]["response"]["status"] == 200
                and "/backend-api/conversations" in log_["params"]["response"]["url"]
            )
        )
        try:
            data = next(datas)
        except StopIteration:
            self.logger.debug("Could not find conversations")
            return None

        self.logger.debug("Found conversations")

        ret = self.driver.execute_cdp_cmd("Network.getResponseBody", {"requestId": data})

        response_data = loads(ret["body"])

        return Conversations(
            response_data["items"],
            response_data["has_missing_conversations"],
            response_data["limit"],
            response_data["offset"],
            response_data["total"]
        )

    def get_shared_conversations(self, timeout: float = 5) -> SharedConversations:
        """
        Get a list of shared conversations.

        Args:
        ----------
            timeout (float, optional): Time to wait for the message to continue regenerating before timing out.

        Returns:
        ----------
            SharedConversations: A list of shared conversations, or None if unsuccessful.
        """
        self.logger.debug("Getting shared conversations...")
        logs_raw = self.driver.get_log("performance")

        start_time = time()
        end_time = start_time + timeout
        opened_popup = False

        while time() < end_time:
            try:
                data = next(
                    log_["params"]["requestId"]
                    for log_ in reversed([loads(lr["message"])["message"] for lr in logs_raw])
                    if (
                        log_["method"] == "Network.responseReceived"
                        and "json" in log_["params"]["response"]["mimeType"]
                        and log_["params"]["response"]["status"] == 200
                        and "/backend-api/shared_conversations" in log_["params"]["response"]["url"]
                    )
                )
                break  # Found data, exit the loop
            except StopIteration:
                if not opened_popup:
                    self.logger.debug("Could not find conversations, opening shared conversations popup...")
                    self._open_shared_conversations_popup()
                    opened_popup = True
                else:
                    self.logger.debug("Could not find conversations, refreshing logs...")
                logs_raw = self.driver.get_log("performance")  # Refresh logs

        else:
            self.logger.debug("Timeout reached, failed to get shared conversations")
            return None

        self.logger.debug("Found shared conversations")

        ret = self.driver.execute_cdp_cmd("Network.getResponseBody", {"requestId": data})

        response_data = loads(ret["body"])

        return SharedConversations(
            response_data["items"],
            response_data["has_missing_conversations"],
            response_data["limit"],
            response_data["offset"],
            response_data["total"]
        )

    def send_message(
        self,
        message: str,
        timeout: int = 240,
        input_mode: Literal["INSTANT", "SLOW"] = "INSTANT",
        input_delay: float = 0.1,
        continue_generating: bool = True,
    ) -> ChatGPTResponse:
        """
        Send a message to ChatGPT.

        Args:
        ----------
            message (str): Message to send.
            timeout (int, optional): Timeout in seconds. Defaults to 240.
            input_mode(list, optional): The input mode. Defaults to 'INSTANT'.
            input_delay(float, optional): The input delay. Defaults to 0.1.
            continue_generating(bool, optional): Whether to continue generating the response or not. Defaults to True.

        Returns:
        ----------
            ChatGPTResponse: Response from ChatGPT.

        Raises:
        ----------
            TimeoutException: If the message fails to send.
            ValueError: If the response is invalid.
            ValueError: If the response is not found.
        """
        assert input_mode in ["INSTANT", "SLOW"], "Invalid input mode"
        self.logger.debug(
            f'Sending message with mode {input_mode}{f" with {input_delay} delay" if input_mode == "SLOW" else ""}...'
        )

        textbox = WebDriverWait(self.driver, 60).until(
            EC.element_to_be_clickable(CGPTV.textbox)
        )
        if input_mode == "INSTANT":
            self.driver.execute_script(
                "arguments[0].value = arguments[1];", textbox, message
            ) # TODO: This isn't working, its just using SLOW mode instead
        else:
            for char in message:
                try:
                    textbox.send_keys(char)
                except StaleElementReferenceException:
                    textbox = WebDriverWait(self.driver, 60).until(
                        EC.element_to_be_clickable(CGPTV.textbox)
                    )
                    textbox.send_keys(char)

        textbox.send_keys("a")
        textbox.send_keys(Keys.BACKSPACE)

        textbox.send_keys(Keys.ENTER)

        self.logger.debug("Waiting for completion...")
        WebDriverWait(self.driver, timeout).until_not(
            EC.presence_of_element_located(CGPTV.streaming)
        )

        self.logger.debug("Getting response...")
        responses = self.driver.find_elements(*CGPTV.big_response)
        if responses:
            response = responses[-1]
            if "text-red" in response.get_attribute("class"):
                self.logger.debug("Response is an error")
                raise ValueError(response.text)
        response = self.driver.find_elements(*CGPTV.small_response)
        try:
            response = response[-1]
        except IndexError:
            self.logger.debug("Response not found, resetting conversation...")
            self.reset_conversation()
            raise ValueError("Response not found")

        content = (
            markdownify(
                response.get_attribute("innerHTML"),
                escape_asterisks=False,
                escape_underscores=False,
            )
            .replace("Copy code`", "`")
            .rstrip("\n")
        )

        if continue_generating:
            continuation = self._continue_generating(timeout=timeout)
            if continuation:
                content = continuation

        self.logger.debug(f"Message sent")

        if not self._conversation_id:
            self.logger.debug(f"New conversation, cathing the id.")
            self._get_conversation_id()

        return ChatGPTResponse(content, self._conversation_id)

    def regenerate_response(
        self,
        message_timeout: int = 240,
        click_timeout: int = 20,
        continue_generating: bool = True,
    ) -> ChatGPTResponse:
        """
        Regenerate the response.

        Args:
        ----------
            message_timeout (int, optional): Time to wait for the message to regenerate before timing out. Defaults to 240.
            click_timeout (int, optional): Time to wait for the click to succeed before timing out. Defaults to 20.
            continue_generating(bool, optional): Whether to continue generating the response or not. Defaults to True.

        Returns:
        ----------
            response (ChatGPTResponse): The newly regenerated response data.

        Raises:
        ----------
            TimeoutException: If the message fails to send.
            TimeoutException: If the click fails to succeed.
            ValueError: If the response is invalid.
            ValueError: If the response is not found.
        """
        self.logger.debug("Regenerating response...")

        # Click "Regenerate response" button
        regenerate_response_clicked = self.driver.safe_click(
            CGPTV.regenerate_response, timeout=click_timeout
        )
        if not regenerate_response_clicked:
            self.logger.debug("Could not click regenerate response button")
            raise TimeoutException("Could not click regenerate response button")

        # Get the response, same way as send_message without the part of sending the message
        self.logger.debug("Waiting for completion...")
        WebDriverWait(self.driver, message_timeout).until_not(
            EC.presence_of_element_located(CGPTV.streaming)
        )

        self.logger.debug("Getting response...")
        responses = self.driver.find_elements(*CGPTV.big_response)
        if responses:
            response = responses[-1]
            if "text-red" in response.get_attribute("class"):
                self.logger.debug("Response is an error")
                raise ValueError(response.text)
        response = self.driver.find_elements(*CGPTV.small_response)
        try:
            response = response[-1]
        except IndexError:
            self.logger.debug("Response not found, resetting conversation...")
            self.reset_conversation()
            raise ValueError("Response not found")

        content = (
            markdownify(
                response.get_attribute("innerHTML"),
                escape_asterisks=False,
                escape_underscores=False,
            )
            .replace("Copy code`", "`")
            .rstrip("\n")
        )

        if continue_generating:
            continuation = self._continue_generating(timeout=message_timeout)
            if continuation:
                content = continuation

        self.logger.debug("Regenerated response")
        return ChatGPTResponse(content, self._conversation_id)

    def reset_conversation(self) -> None:
        """
        Resets the conversation.
        """
        if not self.driver.current_url.startswith("https://chat.openai.com/"):
            return self.logger.debug("Current URL is not chat page, skipping reset")

        self.logger.debug("Resetting conversation...")
        button = CGPTV.new_chat if self._history_and_training_enabled else CGPTV.clear_chat
        clicked = self.driver.safe_click(button, timeout=60)
        if not clicked:
            self.logger.debug(f"{button[1]} button not found")
            return self._get_out_of_menu()
        self.logger.debug("Conversation reset")

    def clear_conversations(self) -> None:
        """
        Clears all conversations.
        """
        self.logger.debug("Clearing all conversations...")
        try:
            menu_button_clicked = self.driver.safe_click(CGPTV.menu_button, timeout=60)
            if not menu_button_clicked:
                self.logger.debug("Could not click menu button")
                return self._get_out_of_menu()
            self.logger.debug("Clicked menu button")

            clear_conversations_button_clicked = self.driver.safe_click(
                CGPTV.menu_clear_conversations, timeout=60
            )
            if not clear_conversations_button_clicked:
                self.logger.debug("Could not click clear conversations button")
                return self._get_out_of_menu()
            self.logger.debug("Clicked clear conversations button")

            confirm_clear_button_clicked = self.driver.safe_click(
                CGPTV.menu_confirm_clear_conversations, timeout=60
            )
            if not confirm_clear_button_clicked:
                self.logger.debug("Could not click confirm clear conversations button")
                return self._get_out_of_menu()
            self.logger.debug("Clicked confirm clear conversations button")

            self.logger.debug("Cleared all conversations")
            self._get_out_of_menu()
        except NoSuchElementException: # type: ignore
            self.logger.debug("Could not find menu buttons")
            return self._get_out_of_menu()

    def switch_theme(
        self, theme: Literal["LIGHT", "DARK", "OPPOSITE", "SYSTEM"]
    ) -> None:
        """
        Switch the theme.

        Args:
        ----------
            theme (Literal['LIGHT', 'DARK', 'OPPOSITE']): The theme to switch to.

        Notes:
        ----------
            - `LIGHT`: Light theme.
            - `DARK`: Dark theme.
            - `OPPOSITE`: Switch to the opposite theme.
            - `SYSTEM`: Switch to the system theme.
        """
        self.logger.debug(f"Switching theme to {theme}...")
        try:
            menu_button_clicked = self.driver.safe_click(CGPTV.menu_button)
            if not menu_button_clicked:
                self.logger.debug("Could not click menu button")
                return self._get_out_of_menu()
            self.logger.debug("Clicked menu button")

            settings_button_clicked = self.driver.safe_click(CGPTV.menu_settings)
            if not settings_button_clicked:
                self.logger.debug("Could not click settings button")
                return self._get_out_of_menu()
            self.logger.debug("Clicked settings button")

            current_theme_value = self.driver.find_element(
                *CGPTV.outer_html
            ).get_attribute("class")
            current_theme = "LIGHT" if "light" in current_theme_value else "DARK"
            if theme == current_theme:
                self.logger.debug("Theme is already set to the desired theme")
                return self._get_out_of_menu()
            self.logger.debug(f"Current theme is {current_theme}")

            button_element = self.driver.find_element(*CGPTV.theme_button)
            ActionChains(self.driver).move_to_element(button_element).perform()
            button_clicked = self.driver.safe_click(CGPTV.theme_button, timeout=60)
            if not button_clicked:
                self.logger.debug("Could not click theme button")
                return self._get_out_of_menu()
            self.logger.debug("Clicked theme button")

            try:
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[role='option']")))
            except TimeoutException: # type: ignore
                self.logger.debug("Could not load theme options")
                return self._get_out_of_menu()

            options = self.driver.find_elements(By.CSS_SELECTOR, "[role='option']")
            if not options:
                self.logger.debug("Could not find theme options")
                return self._get_out_of_menu()
            
            if theme == "OPPOSITE":
                if current_theme == "SYSTEM":
                    self.logger.debug("Theme cannot be set to opposite of system theme")
                    return self._get_out_of_menu()

                opposite_theme = "dark" if current_theme == "LIGHT" else "light"
                try:
                    for option in options:
                        safe_option = WebDriverWait(self, 10).until(
                            EC.element_to_be_clickable(option)
                        )
                        if safe_option.text.lower() == opposite_theme.lower():
                            try:
                                safe_option.click()
                            except:
                                self.logger.debug("Could not click opposite theme option")
                                return self._get_out_of_menu()
                except:
                    self.logger.debug(f"Could not find theme option {theme}")
                    return self._get_out_of_menu()

                self.logger.debug(f"Selected opposite theme of {current_theme}")
            else:
                try:
                    for option in options:
                        safe_option = WebDriverWait(self, 10).until(
                            EC.element_to_be_clickable(option)
                        )
                        if safe_option.text.lower() == theme.lower():
                            try:
                                safe_option.click()
                            except:
                                self.logger.debug("Could not click opposite theme option")
                                return self._get_out_of_menu()
                except:
                    self.logger.debug(f"Could not find theme option {theme}")
                    return self._get_out_of_menu()

                self.logger.debug(f"Selected theme {theme}")

            self.logger.debug("Theme switched")
            self._get_out_of_menu()
        except NoSuchElementException as e: # type: ignore
            self.logger.debug("Could not find theme buttons")
            return self._get_out_of_menu()

    def switch_account(self, session_token: str) -> SessionData:
        """
        Switch the account.

        Args:
        ----------
            session_token (str): The session token for authentication.

        Returns:
        ----------
            SessionData: The new account's session data.

        Raises:
        ----------
            ValueError: If the session token is not provided.
            ValueError: If the response is invalid.
        """
        self.logger.debug("Switching account...")
        self.conversation_id = (
            ""  # Old conversation ID cannot be loaded in the new account
        )
        self.driver.execute_cdp_cmd(
            "Network.setCookie",
            {
                "domain": "chat.openai.com",
                "path": "/",
                "name": "__Secure-next-auth.session-token",
                "value": session_token,
                "httpOnly": True,
                "secure": True,
            },
        )
        self.logger.debug("Executed CDP command")

        self.logger.debug("Validating authorization...")
        self.driver.get("https://chat.openai.com/api/auth/session")
        response = self.driver.page_source
        if response[0] != "{":
            response = self.driver.find_element(By.TAG_NAME, "pre").text
        response = loads(response)
        if (not response) or (
            "error" in response and response["error"] == "RefreshAccessTokenError"
        ):
            raise ValueError("Invalid session token")
        session_data = SessionData(
            User(**response["user"]),
            response["expires"],
            response["accessToken"],
            response["authProvider"],
        )
        self.logger.debug("Authorization is valid")

        self.logger.debug("Opening chat page...")
        self.driver.get(f"{CGPTV.chat_url}/{self._conversation_id}")
        self.logger.debug("Opened chat page")
        self._check_blocking_elements()
        self.logger.debug("Switched account")
        return session_data

    def get_session_data(self) -> SessionData:
        """
        Get the session data.

        Returns:
        ----------
            SessionData: The current account's session data.
        """
        self.logger.debug("Getting account data...")
        self.logger.debug("Opening new tab...")
        self.driver.execute_script("window.open();")
        self.driver.switch_to.window(self.driver.window_handles[-1])
        self.driver.get("https://chat.openai.com/api/auth/session")
        response = self.driver.page_source
        if response[0] != "{":
            response = self.driver.find_element(By.TAG_NAME, "pre").text
        response = loads(response)
        session_data = SessionData(
            User(**response["user"]),
            response["expires"],
            response["accessToken"],
            response["authProvider"],
        )
        self.logger.debug("Closing tab...")
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])
        return session_data

    def logout(self) -> None:
        """
        Logs out of the current account signed into https://chat.openai.com
        """
        self.logger.debug("Logging out...")
        self.driver.execute_cdp_cmd(
            "Network.deleteCookies",
            {
                "name": "__Secure-next-auth.session-token",
                "url": "https://chat.openai.com",
            },
        )
        self.logger.debug("Executed CDP command")
        self.driver.get("https://chat.openai.com/api/auth/session")
        response = self.driver.page_source
        if response[0] != "{":
            response = self.driver.find_element(By.TAG_NAME, "pre").text
        response = loads(response)
        if response == {}:
            self.logger.debug("Logout successful")
            return

    def toggle_chat_history(self, state: bool = False) -> None:
        """
        Toggle chat history.

        Args:
        ----------
            state (bool, optional): The state to set the chat history toggle to. Defaults to False.
        """
        self.logger.debug("Disabling chat history...")
        try:
            menu_button_clicked = self.driver.safe_click(CGPTV.menu_button)
            if not menu_button_clicked:
                self.logger.debug("Could not click menu button")
                return self._get_out_of_menu()

            self.logger.debug("Clicked menu button")

            settings_button_clicked = self.driver.safe_click(CGPTV.menu_settings)
            if not settings_button_clicked:
                self.logger.debug("Could not click settings button")
                return self._get_out_of_menu()

            self.logger.debug("Clicked settings button")

            wait = WebDriverWait(self.driver, 60)

            # Click "Data controls" button
            data_controls_clicked = self.driver.safe_click(
                CGPTV.data_controls, timeout=60
            )
            if not data_controls_clicked:
                self.logger.debug("Could not click data controls button")
                return self._get_out_of_menu()

            # Click "Disable chat history" button
            # Not using safe_click because it there are some checks that need to be done before clicking
            chat_history_toggle = wait.until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, f'button[aria-label="Chat history & training"]')
                )
            )
            current_state = (
                True
                if chat_history_toggle.get_attribute("aria-checked") == "true"
                else False
            )
            if current_state == state:
                self.logger.debug("Chat history is already set to the desired state")
                return self._get_out_of_menu()

            chat_history_toggle.click()
            self.logger.debug(
                f'Chat history is now {"enabled" if state else "disabled"}'
            )
        except:
            self.logger.debug(
                f'Could not {"enable" if state else "disable"} chat history'
            )
        
        self._history_and_training_enabled = state

        return self._get_out_of_menu()

    def switch_conversation(self, conversation_id: str) -> None:
        """
        Switch the conversation.

        Args:
        ----------
            conversation_id (str): The conversation ID to switch to.

        Raises:
        ----------
            InvalidConversationID: If the conversation ID is invalid.
        """
        self.logger.debug("Switching conversation...")
        self.driver.get(f"{CGPTV.chat_url}/{conversation_id}")
        self._check_blocking_elements()
        self._conversation_id = conversation_id
        self.logger.debug(f"Switched conversation to {conversation_id}")
