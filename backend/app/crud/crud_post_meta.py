from typing import Dict, List, Optional

from neomodel import db

from app import models, schemas
from app.crud.crud_thing_meta import CRUDThingBaseMeta
from app.crud.cypher import CypherGetPosts


class CRUDPostMeta(
    CRUDThingBaseMeta[models.PostMeta, schemas.PostMetaCreate, schemas.PostMetaUpdate]
):
    """Post meta class for CRUD operations"""

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
        :param cursor: a cursor for pagination
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
            elif sort == schemas.PostSort.best:  # TODO: implement best sorting order
                pass

        results, columns = db.cypher_query(query, params)
        post_list = [row[0] for row in results]
        if direction == schemas.CursorDirection.before:
            # TODO: need to reverse the list here, because I couldn't find an easy
            #  way to do this in the Cypher query yet
            post_list.reverse()
        return post_list

    @db.write_transaction
    def set_subreddit(
        self, db_obj: models.PostMeta, subreddit: models.Subreddit
    ) -> models.Subreddit:
        post_subreddit = db_obj.subreddit.connect(subreddit)
        return post_subreddit


post_meta = CRUDPostMeta(models.PostMeta)
