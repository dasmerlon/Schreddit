from neomodel import DateTimeProperty, StructuredRel


class Friendship(StructuredRel):
    since = DateTimeProperty(default_now=True)


class Vote(StructuredRel):
    """
    Abstract base class for ``Downvote`` and ``Upvote``.
    """

    timestamp = DateTimeProperty(default_now=True)


class Downvote(Vote):
    pass


class Upvote(Vote):
    pass


class Subscription(StructuredRel):
    pass
