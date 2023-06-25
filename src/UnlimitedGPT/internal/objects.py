from datetime import datetime
from typing import Any, List, Optional


class ChatGPTResponse:
    """
    The response object returned by ChatGPT
    """

    def __init__(self, response: str, conversation_id: Optional[str] = None):
        """
        Initialize a ChatGPTResponse object.

        Args:
        ----------
            response (str): The response from ChatGPT.
            conversation_id (Optional[str]): The conversation ID.
        """
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
        intercom_hash: str,
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
        self, user: User, expires: str, accessToken: str, authProvider: str
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

class Conversation:
    """Class representing a conversation."""

    def __init__(self, name: str, conversation_id: str, create_time: str):
        """
        Initialize a Conversation object.

        Args:
        ----------
            name (str): The name of the conversation.
            conversation_id (str): The ID of the conversation.
            create_time (str): The time the conversation was created.
        """
        self.name = name
        self.conversation_id = conversation_id
        self.create_time = create_time
    
    def __str__(self):
        return f"Conversation(name='{self.name}', conversation_id='{self.conversation_id}', create_time={self.create_time})"

    def __repr__(self):
        return f"Conversation(name='{self.name}', conversation_id='{self.conversation_id}', create_time={self.create_time})"

class Conversations:
    """Class representing a list of conversations."""

    def __init__(
        self,
        conversations: dict,
        has_missing_conversations: bool,
        limit: int,
        offset: int,
        total: int,
    ):
        """
        Initialize a Conversations object.

        Args:
        ----------
            conversations (dict): The dict of conversations.
            has_missing_conversations (bool): Whether there are missing conversations.
            limit (int): The limit of conversations.
            offset (int): The offset of conversations.
            total (int): The total number of conversations.
        """
        self.conversations = [Conversation(**conversation) for conversation in conversations]
        self.has_missing_conversations = has_missing_conversations
        self.limit = limit
        self.offset = offset
        self.total = total
    
    def __str__(self):
        return f"<Conversations conversations={self.conversations} has_missing_conversations={self.has_missing_conversations} limit={self.limit} offset={self.offset} total={self.total}>"

    def __repr__(self):
        return f"<Conversations conversations={self.conversations} has_missing_conversations={self.has_missing_conversations} limit={self.limit} offset={self.offset} total={self.total}>"

class Account:
    """Class representing a ChatGPT account."""

    def __init__(
        self,
        account_user_role: str,
        account_user_id: str,
        processor: dict,
        account_id: str,
        is_most_recent_expired_subscription_gratis: bool,
        has_previously_paid_subscription: bool,
    ):
        """
        Initialize an Account object.

        Args:
        ----------
            account_user_role (str)
            account_user_id (str)
            processor (dict)
            account_id (str)
            is_most_recent_expired_subscription_gratis (bool)
            has_previously_paid_subscription (bool)            
        """
        self.account_user_role = account_user_role
        self.account_user_id = account_user_id
        self.processor = processor
        self.account_id = account_id
        self.is_most_recent_expired_subscription_gratis = is_most_recent_expired_subscription_gratis
        self.has_previously_paid_subscription = has_previously_paid_subscription

    def __str__(self):
        return f"<Account account_user_role={self.account_user_role} account_user_id={self.account_user_id} processor={self.processor} account_id={self.account_id} is_most_recent_expired_subscription_gratis={self.is_most_recent_expired_subscription_gratis} has_previously_paid_subscription={self.has_previously_paid_subscription}>"

    def __repr__(self):
        return f"<Account account_user_role={self.account_user_role} account_user_id={self.account_user_id} processor={self.processor} account_id={self.account_id} is_most_recent_expired_subscription_gratis={self.is_most_recent_expired_subscription_gratis} has_previously_paid_subscription={self.has_previously_paid_subscription}>"

class Entitlement:
    """Class representing an account's entitlement."""

    def __init__(
        self,
        subscription_id: Optional[Any],
        has_active_subscription: bool,
        subscription_plan: str,
        expires_at: Optional[Any],
    ):
        """
        Initialize an Entitlement object.

        Args:
        ----------
            subscription_id (Optional[Any])
            has_active_subscription (bool)
            subscription_plan (str)
            expires_at (Optional[Any])
        """
        self.subscription_id = subscription_id
        self.has_active_subscription = has_active_subscription
        self.subscription_plan = subscription_plan
        self.expires_at = expires_at
    
    def __str__(self):
        return f"<Entitlement subscription_id={self.subscription_id} has_active_subscription={self.has_active_subscription} subscription_plan={self.subscription_plan} expires_at={self.expires_at}>"

    def __repr__(self):
        return f"<Entitlement subscription_id={self.subscription_id} has_active_subscription={self.has_active_subscription} subscription_plan={self.subscription_plan} expires_at={self.expires_at}>"

class LastActiveSubscription:
    """Class representing an account's last active subscription."""

    def __init__(
        self,
        subscription_id: Optional[Any],
        purchase_origin_platform: str,
        will_renew: bool
    ):
        """
        Initialize a LastActiveSubscription object.

        Args:
        ----------
            subscription_id (Optional[Any])
            purchase_origin_platform (str)
            will_renew (bool)
        """
        self.subscription_id = subscription_id
        self.purchase_origin_platform = purchase_origin_platform
        self.will_renew = will_renew

    def __str__(self):
        return f"<LastActiveSubscription subscription_id={self.subscription_id} purchase_origin_platform={self.purchase_origin_platform} will_renew={self.will_renew}>"

    def __repr__(self):
        return f"<LastActiveSubscription subscription_id={self.subscription_id} purchase_origin_platform={self.purchase_origin_platform} will_renew={self.will_renew}>"

class DefaultAccount:
    """Class representing the ChatGPT default account."""

    def __init__(
        self,
        account: dict,
        features: List[str],
        entitlement: dict,
        last_active_subscription: dict
    ):
        """
        Initialize an Account object.

        Args:
        ----------
        """
        self.account = Account(**account)
        self.features = features
        self.entitlement = Entitlement(**entitlement)
        self.last_active_subscription = LastActiveSubscription(**last_active_subscription)
    
    def __str__(self):
        return f"<DefaultAccount account={self.account} features={self.features} entitlement={self.entitlement} last_active_subscription={self.last_active_subscription}>"

    def __repr__(self):
        return f"<DefaultAccount account={self.account} features={self.features} entitlement={self.entitlement} last_active_subscription={self.last_active_subscription}>"

class Accounts:
    """Class representing a list of ChatGPT accounts."""

    def __init__(
        self,
        data: dict
    ):
        """
        Initialize an Accounts object.

        Args:
        ----------
            data (dict)
        """
        self.default = DefaultAccount(**data["accounts"]['default'])

    def __str__(self):
        return f"<Accounts default={self.default}>"

    def __repr__(self):
        return f"<Accounts default={self.default}>"

class SharedConversation:
    """Class representing a shared conversation."""

    def __init__(
        self,
        id: str,
        title: str,
        create_time: str,
        update_time: str,
        mapping: Optional[Any],
        current_node: Optional[Any],
        conversation_id: str,
    ):
        """
        Initialize a SharedConversation object.

        Args:
        ----------
            id (str)
            title (str)
            create_time (str)
            update_time (str)
            mapping (Optional[Any])
            current_node (Optional[Any])
            conversation_id (str)
        """
        self.id = id
        self.title = title
        self.create_time = create_time
        self.update_time = update_time
        self.mapping = mapping
        self.current_node = current_node
        self.conversation_id = conversation_id
    
    def __str__(self):
        return f"<SharedConversation id={self.id} title={self.title} create_time={self.create_time} update_time={self.update_time} mapping={self.mapping} current_node={self.current_node} conversation_id={self.conversation_id}>"

    def __repr__(self):
        return f"<SharedConversation id={self.id} title={self.title} create_time={self.create_time} update_time={self.update_time} mapping={self.mapping} current_node={self.current_node} conversation_id={self.conversation_id}>"

class SharedConversations:
    """Class representing a list of shared conversations."""

    def __init__(
        self,
        conversations: dict,
        total: int,
        limit: int,
        offset: int,
        has_missing_conversations: bool,
    ):
        """
        Initialize a SharedConversations object.

        Args:
        ----------
            conversations (dict)
            total (int)
            limit (int)
            offset (int)
            has_missing_conversations (bool)
        """
        self.conversations = [SharedConversation(**conversation) for conversation in conversations]
        self.total = total
        self.limit = limit
        self.offset = offset
        self.has_missing_conversations = has_missing_conversations
    
    def __str__(self):
        return f"<SharedConversations conversations={self.conversations} has_missing_conversations={self.has_missing_conversations} limit={self.limit} offset={self.offset} total={self.total}>"

    def __repr__(self):
        return f"<SharedConversations conversations={self.conversations} has_missing_conversations={self.has_missing_conversations} limit={self.limit} offset={self.offset} total={self.total}>"
