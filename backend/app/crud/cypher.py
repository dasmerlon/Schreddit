import re
from typing import Optional

from app import models, schemas

# label names
sr_lbl = models.Subreddit.__name__
post_lbl = models.PostMeta.__name__
user_lbl = models.User.__name__

# property names
username_prop = models.User.username.name
sr_prop = models.Subreddit.sr.name
created_at_prop = models.PostMeta.created_at.name

# relationship names
posted_in_rel = models.PostMeta.subreddit.definition["relation_type"]
authored_by_rel = models.PostMeta.author.definition["relation_type"]
upvoted_rel = models.User.upvotes.definition["relation_type"]
downvoted_rel = models.User.downvotes.definition["relation_type"]

base = (
    # match posts in subreddit
    f"MATCH (sr:{sr_lbl})-[:{posted_in_rel}]-(post:{post_lbl}) "
    f"WHERE sr.uid = $sr_uid "
    # match post authors
    f"OPTIONAL MATCH (post)-[:{authored_by_rel}]-(author:{user_lbl}) "
)
state = (
    # match vote state of logged in user for every post
    f"OPTIONAL MATCH (post)-[vote:{upvoted_rel}|{downvoted_rel}]-(user:User) "
    f"WHERE user.uid = $user_uid "
    f"WITH post, sr, author, score, CASE type(vote) "
    f"  WHEN '{upvoted_rel}' THEN 1 "
    f"  WHEN '{downvoted_rel}' THEN -1 "
    f"  ELSE 0 "
    f"END AS state "
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
    ):
        """
        Initialize the class.

        :param sort: sorting order of the posts
        :param cursor: the pagination cursor if pagination is required, else ``None``
        :param direction: the direction of the cursor
        """
        self.sort = sort
        self.cursor = True if isinstance(cursor, models.PostMeta) else False
        self.signs = (
            before_signs if direction == schemas.CursorDirection.before else after_signs
        )

    def get_query(self):
        """
        Get the Cypher query.
        It is built by concatenating the variables
        ``base``, ``addon``, ``where``, ``order``, ``state`` and ``unite``.

        :return: the Cypher query
        """
        s = self.signs  # shortcut

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
                    f"  post.uid {s[0]} $cursor_uid"
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
                f"     sign * ord + seconds / 45000 AS hot "
            )
            if self.cursor:
                where = (
                    f"WHERE hot {s[0]} $cursor_prop "
                    f"OR (hot = $cursor_prop AND post.uid {s[0]} $cursor_uid) "
                )
            order = (
                f"WITH post, sr, author, score, hot "
                f"ORDER BY hot {s[1]}, id(post) {s[1]} "
                f"LIMIT $limit "
            )
        elif self.sort == schemas.PostSort.top:
            if self.cursor:
                where = (
                    f"WHERE upvotes {s[0]} $cursor_prop "
                    f"OR (upvotes = $cursor_prop AND post.uid {s[0]} $cursor_uid) "
                )
            order = (
                f"WITH post, sr, author, score, upvotes "
                f"ORDER BY upvotes {s[1]}, id(post) {s[1]} "
                f"LIMIT $limit "
            )

        # remove redundant whitespace and return query
        return re.sub(" +", " ", base + addon + where + order + state + unite)
