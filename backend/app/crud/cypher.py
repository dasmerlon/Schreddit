import re
from typing import Optional

from app import models, schemas

# label names
comment_lbl = models.CommentMeta.__name__
post_lbl = models.PostMeta.__name__
sr_lbl = models.Subreddit.__name__
thing_lbl = models.ThingMeta.__name__
user_lbl = models.User.__name__

# property names
created_at_prop = models.PostMeta.created_at.name
sr_prop = models.Subreddit.sr.name
username_prop = models.User.username.name

# relationship names
authored_by_rel = models.PostMeta.author.definition["relation_type"]
downvoted_rel = models.User.downvotes.definition["relation_type"]
parent_rel = models.CommentMeta.parent.definition["relation_type"]
posted_in_rel = models.PostMeta.subreddit.definition["relation_type"]
upvoted_rel = models.User.upvotes.definition["relation_type"]

base = (
    # match posts in subreddit
    f"MATCH (sr:{sr_lbl})-[:{posted_in_rel}]-(post:{post_lbl}) "
    f"WHERE sr.uid = $sr_uid "
    # match post authors
    f"OPTIONAL MATCH (post)-[:{authored_by_rel}]-(author:{user_lbl}) "
)
unite = (
    # put post properties into a map
    # put author, sr and vote count into a map
    f"WITH properties(post) AS postmap, {{"
    f"  author: author.{username_prop}, "
    f"  sr: sr.{sr_prop}, "
    f"  count: score, "
    f"  state: state"
    f"}} AS infomap "
    # merge both maps into one
    f"RETURN apoc.map.merge(postmap, infomap) AS output "
)

after_signs = ("<", "DESC")
before_signs = (">", "ASC")


class CypherGetPosts:
    """
    Build the Cypher query for retrieving a sorted list of posts
    """

    def __init__(
        self,
        sort: schemas.PostSort,
        cursor: Optional[models.PostMeta],
        direction: schemas.CursorDirection,
        subreddit: Optional[models.Subreddit],
        user: Optional[models.User],
    ):
        """
        Initialize the class.

        :param sort: sorting order of the posts
        :param cursor: the pagination cursor if pagination is required, else ``None``
        :param direction: the direction of the cursor
        :param subreddit: if specified, the subreddit to get posts from;
        if ``None``, get all posts
        :param user: if specified, the user to get vote states for;
        if ``None``, don't get vote states
        """
        self.sort = sort
        self.cursor = True if isinstance(cursor, models.PostMeta) else False
        self.signs = (
            before_signs if direction == schemas.CursorDirection.before else after_signs
        )
        self.subreddit = bool(subreddit)
        self.user = bool(user)

    def get_query(self):
        """
        Get the Cypher query.
        It is built by concatenating the variables
        ``base``, ``addon``, ``where``, ``order``, ``state`` and ``unite``.

        :return: the Cypher query
        """
        s = self.signs  # shortcut

        if self.subreddit:
            base = (
                # match posts in subreddit
                f"MATCH (sr:{sr_lbl})-[:{posted_in_rel}]-(post:{post_lbl}) "
                f"WHERE sr.uid = $sr_uid "
            )
        else:
            base = (
                # match all posts
                f"MATCH (sr:{sr_lbl})-[:{posted_in_rel}]-(post:{post_lbl}) "
            )
        # match posts authors
        base += f"OPTIONAL MATCH (post)-[:{authored_by_rel}]-(author:{user_lbl}) "

        addon = (
            # get upvote and downvote counts
            f"WITH post, sr, author, "
            f"     size((post)-[:{upvoted_rel}]-(:{user_lbl})) AS upvotes, "
            f"     size((post)-[:{downvoted_rel}]-(:{user_lbl})) AS downvotes "
            f"WITH post, sr, author, upvotes, downvotes, upvotes-downvotes AS score "
        )
        where = ""
        order = ""

        # limit results based on sorting order
        if self.sort == schemas.PostSort.new:
            if self.cursor:
                where = (
                    f"WHERE post.{created_at_prop} {s[0]} $cursor_prop "
                    f"OR ("
                    f"  post.{created_at_prop} = $cursor_prop AND "
                    f"  id(post) {s[0]} $cursor_id"
                    f") "
                )
            order = (
                f"WITH post, sr, author, score "
                f"ORDER BY post.{created_at_prop} {s[1]}, id(post) {s[1]} "
                f"LIMIT $limit "
            )
        elif self.sort == schemas.PostSort.hot:
            # CAUTION: THIS ALGORITHM MUST MATCH THE ONE IN THE MODEL DEFINITION
            addon += (
                f"WITH post, sr, author, upvotes, downvotes, score, "
                f"     post.{created_at_prop} - 1134028003 AS seconds, "
                f"     CASE "
                f"       WHEN score > 0 THEN 1 "
                f"       WHEN score < 0 THEN -1"
                f"       ELSE 0"
                f"     END AS sign, "
                f"     log10(apoc.coll.max([abs(score), 1])) AS ord "
                f"WITH post, sr, author, upvotes, downvotes, score, "
                f"     round(sign * ord + seconds / 45000, 7) AS hot "
            )
            if self.cursor:
                where = (
                    f"WHERE hot {s[0]} $cursor_prop "
                    f"OR (hot = $cursor_prop AND id(post) {s[0]} $cursor_id) "
                )
            order = (
                f"WITH post, sr, author, score, hot "
                f"ORDER BY hot {s[1]}, id(post) {s[1]} "
                f"LIMIT $limit "
            )
        elif self.sort == schemas.PostSort.top:
            if self.cursor:
                where = (
                    f"WHERE score {s[0]} $cursor_prop "
                    f"OR (score = $cursor_prop AND id(post) {s[0]} $cursor_id) "
                )
            order = (
                f"WITH post, sr, author, score "
                f"ORDER BY score {s[1]}, id(post) {s[1]} "
                f"LIMIT $limit "
            )

        if self.user:
            # match vote state of logged in user for every post
            state = (
                f"OPTIONAL MATCH (post)"
                f"               -[vote:{upvoted_rel}|{downvoted_rel}]-"
                f"               (user:User) "
                f"WHERE user.uid = $user_uid "
                f"WITH post, sr, author, score, CASE type(vote) "
                f"  WHEN '{upvoted_rel}' THEN 1 "
                f"  WHEN '{downvoted_rel}' THEN -1 "
                f"  ELSE 0 "
                f"END AS state "
            )
        else:
            state = "WITH post, sr, author, score, 0 AS state "

        # remove redundant whitespace and return query
        return re.sub(" +", " ", base + addon + where + order + state + unite)


class CypherGetTree:
    """
    Build the Cypher query for retrieving the comment tree for a post.
    """

    def __init__(self, user: Optional[models.User]):
        """
        Initialize the class.

        :param user: if specified, the user to get vote states for;
        if ``None``, don't get vote states
        """
        self.user = bool(user)

    @staticmethod
    def get_tree_query():
        """
        Get the Cypher query for retrieving the post tree for a post.

        :return: the Cypher query
        """
        query = (
            # match post
            f"MATCH path = (post:{post_lbl})-[:{parent_rel}*0..]-()  "
            f"WHERE post.uid = $post_uid "
            # collect all paths and transform them to one list
            f"WITH collect(path) AS paths "
            # transform the list of paths to a tree
            f"CALL apoc.convert.toTree(paths) "
            f"YIELD value "
            f"RETURN value"
        )
        return query

    def get_votes_query(self):
        """
        Get the Cypher query for retrieving vote state and vote count.

        :return: the Cypher query
        """
        base = (
            # match things with a list of uids
            f"MATCH (thing:{thing_lbl}) "
            f"WHERE thing.uid IN $thing_uids "
            # match thing authors
            f"OPTIONAL MATCH (thing)-[:{authored_by_rel}]-(author:{user_lbl}) "
            # match vote score
            f"WITH thing, author, "
            f"     size((thing)-[:{upvoted_rel}]-(:{user_lbl})) AS upvotes, "
            f"     size((thing)-[:{downvoted_rel}]-(:{user_lbl})) AS downvotes "
            f"WITH thing, author, upvotes-downvotes AS score "
        )
        # match vote state
        if self.user:
            state = (
                f"OPTIONAL MATCH (thing)"
                f"               -[vote:{upvoted_rel}|{downvoted_rel}]-"
                f"               (user:User) "
                f"WHERE user.uid = $user_uid "
                f"WITH thing, author, score, CASE type(vote) "
                f"  WHEN '{upvoted_rel}' THEN 1 "
                f"  WHEN '{downvoted_rel}' THEN -1 "
                f"  ELSE 0 "
                f"END AS state "
            )
        else:
            state = "WITH thing, author, score, 0 AS state "
        ret = (
            f"RETURN thing.uid AS thing, "
            f"       author.{username_prop} AS author, "
            f"       score, state"
        )
        return re.sub(" +", " ", base + state + ret)
