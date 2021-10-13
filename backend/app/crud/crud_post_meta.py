from typing import Dict, List, Optional

from neomodel import db

from app import models, schemas
from app.crud.crud_thing_meta import CRUDThingBaseMeta
from app.crud.cypher import CypherGetPosts, CypherGetTree


class CRUDPostMeta(
    CRUDThingBaseMeta[models.PostMeta, schemas.PostMetaCreate, schemas.PostMetaUpdate]
):
    """CRUD class for post metadata"""

    @db.read_transaction
    def get_posts(
        self,
        subreddit: Optional[models.Subreddit],
        user: Optional[models.User],
        cursor: Optional[models.PostMeta],
        direction: Optional[schemas.CursorDirection],
        sort: schemas.PostSort,
        limit: int,
    ) -> List[Dict]:
        """
        Get the posts after the cursor.

        :param subreddit: if specified, the subreddit to get posts from;
            if ``None``, get all posts
        :param user: if specified, the user to get vote states for;
            if ``None``, don't get vote states
        :param cursor: cursor for pagination
        :param direction: if ``after``, get posts after the cursor;
            if ``before``, get posts before the cursor;
            if ``None`` get first posts
        :param sort: sorting order
        :param limit: number of posts to get
        :return: a list of dicts containing PostMeta data,
            author, sr, vote count and vote state
        """
        query = CypherGetPosts(sort, cursor, direction, subreddit, user).get_query()

        # set required parameters for query
        params = {"limit": limit}
        if subreddit:
            params["sr_uid"] = subreddit.uid
        if user:
            params["user_uid"] = user.uid
        if cursor:
            params["cursor_id"] = cursor.id
            if sort == schemas.PostSort.new:
                params["cursor_prop"] = cursor.created_at.timestamp()
            elif sort == schemas.PostSort.hot:
                params["cursor_prop"] = cursor.hot_score()
            elif sort == schemas.PostSort.top:
                params["cursor_prop"] = cursor.vote_count()

        results, columns = db.cypher_query(query, params)
        post_list = [row[0] for row in results]
        if direction == schemas.CursorDirection.before:
            # list needs to be reversed here, no easy way to do it in the query
            post_list.reverse()
        return post_list

    @db.read_transaction
    def get_post_tree(
        self, post: models.PostMeta, user: Optional[models.User]
    ) -> (Dict, List[str]):
        """
        Get the post tree for a post.

        :param post: post to get the post tree for
        :param user: if specified, the user to get vote states for;
            if ``None``, don't get vote states
        :return: a tree-like dict that contains the comments associated with the post
            and a list of all the thing UUIDs contained in the tree
        """
        cgt = CypherGetTree(user)
        query = cgt.get_tree_query()
        params = {"post_uid": post.uid}
        results, columns = db.cypher_query(query, params)
        tree = results[0][0]

        # collect uids of things
        uids = []
        stack = list(tree.items())
        while stack:
            k, v = stack.pop()
            if k == "parent" and isinstance(v, list):
                for comment in v:
                    stack.extend(comment.items())
            elif k == "uid":
                uids.append(v)

        # get vote state and vote count for uids
        query = cgt.get_votes_query()
        params = {"thing_uids": uids}
        if user:
            params["user_uid"] = user.uid
        results, columns = db.cypher_query(query, params)

        # iterate through tree and add authors and vote state/count
        stack = [tree]
        while stack:
            thing = stack.pop()
            thing_uid = thing["uid"]
            # search result index
            idx = [row[0] for row in results].index(thing_uid)
            thing["author"] = results[idx][1]
            thing["count"] = results[idx][2]
            thing["state"] = results[idx][3]
            children = thing.get("parent")
            if children and isinstance(children, list):
                for thing in children:
                    stack.append(thing)
            elif children is None:  # add empty children list if no children exist
                thing["parent"] = []
        return tree, uids

    @db.read_transaction
    def get_subreddit(self, db_obj: models.PostMeta) -> models.Subreddit:
        """
        Get the subreddit a post was posted in.

        :param db_obj: post node
        :return: the associated subreddit node
        """
        return db_obj.subreddit.single()

    @db.write_transaction
    def set_subreddit(
        self, db_obj: models.PostMeta, subreddit: models.Subreddit
    ) -> None:
        """
        Set the subreddit a post is posted in.

        :param db_obj: post node
        :param subreddit: associated subreddit node
        """
        db_obj.subreddit.connect(subreddit)


post_meta = CRUDPostMeta(models.PostMeta)
