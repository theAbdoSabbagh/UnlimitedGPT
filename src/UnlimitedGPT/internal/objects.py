from typing import Optional, List
from datetime import datetime

class ChatGPTResponse:
    """
    The response object returned by ChatGPT
    """
    def __init__(
        self,
        response: str,
        conversation_id: Optional[str] = None
    ):
        self.response = response
        self.conversation_id = conversation_id
    
    def __str__(self):
        return self.response
    
    def __repr__(self):
        return f'<ChatGPTResponse response="{self.response}" conversation_id="{self.conversation_id}">'

class User:
    """
    The user object returned by ChatGPT.
    """
    def __init__(
        self,
        id: str,
        name: str,
        email: str,
        image: str,
        picture: str,
        idp: str,
        iat: int,
        mfa: bool,
        groups: List[str],
        intercom_hash: str
    ) -> None:
        """
        Initialize a User object.

        Args:
        ----------
            id (str): The user ID.
            name (str): The user's name.
            email (str): The user's email.
            image (str): The URL of the user's image.
            picture (str): The URL of the user's picture.
            idp (str): The identity provider.
            iat (int): The token's issued at timestamp.
            mfa (bool): Whether MFA (Multi-Factor Authentication) is enabled for the user.
            groups (List[str]): The user's groups.
            intercom_hash (str): The Intercom hash.
        """
        self.id = id
        self.name = name
        self.email = email
        self.image = image
        self.picture = picture
        self.idp = idp
        self.iat = iat
        self.mfa = mfa
        self.groups = groups
        self.intercom_hash = intercom_hash
    
    def __str__(self):
        return self.name

    def __repr__(self):
        return f'<User name="{self.name}" id="{self.id}" email="{self.email}" image="{self.image}" picture="{self.picture}" idp="{self.idp}" iat="{self.iat}" mfa="{self.mfa}" groups="{self.groups}" intercom_hash="{self.intercom_hash}">'

class SessionData:
    """Class representing session data."""

    def __init__(
        self,
        user: User,
        expires: str,
        accessToken: str,
        authProvider: str
    ) -> None:
        """
        Initialize a SessionData object.

        Args:
        ----------
            user (User): The user associated with the session.
            expires (str): The expiration date and time of the session.
            accessToken (str): The access token for the session.
            authProvider (str): The authentication provider.
        """
        self.user = user
        self.expires = datetime.strptime(expires, "%Y-%m-%dT%H:%M:%S.%fZ")
        self.accessToken = accessToken
        self.authProvider = authProvider

    def __str__(self):
        return self.user.name

    def __repr__(self):
        return f'<SessionData user="{self.user}" expires="{self.expires}" accessToken="{self.accessToken}" authProvider="{self.authProvider}">'
