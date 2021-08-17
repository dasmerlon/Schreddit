from neomodel import DateTimeProperty, StructuredRel


class Friendship(StructuredRel):
    since = DateTimeProperty(default_now=True)


class Vote(StructuredRel):
    __abstract_node__ = True
    timestamp = DateTimeProperty(default_now=True)


class Downvote(Vote):
    pass


class Upvote(Vote):
    pass
