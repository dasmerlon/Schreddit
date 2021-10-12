from typing import Optional

from fastapi import APIRouter, Depends, Query, Request, Response, status
from pydantic import UUID4

from app import crud, models, schemas
from app.api import deps
from app.api.api_v1.exceptions import (PaginationAfterAndBeforeException,
                                       PaginationInvalidCursorException,
                                       PostNotFoundException,
                                       PostTypeRequestInvalidException,
                                       SubredditNotFoundException,
                                       UnauthorizedUpdateException)

router = APIRouter()


@router.get(
    "/list",
    name="Get a list of posts",
    response_model=schemas.PostList,
    status_code=status.HTTP_200_OK,
)
def get_posts(
    request: Request,
    sr: Optional[str] = None,
    after: Optional[UUID4] = None,
    before: Optional[UUID4] = None,
    sort: Optional[schemas.PostSort] = schemas.PostSort.new,
    size: Optional[int] = Query(25, gt=0, le=100),
    current_user: Optional[models.User] = Depends(deps.get_current_user_or_none),
):
    """
    Return a range of up to `size` posts sorted by the order given by the `sort`
    parameter.

    Cursor-based pagination is available via the `after` and `before` parameters.

    - `sr`: if specified, only posts from this subreddit are considered;
      if not specified, all posts are considered
    - `after`: UUID of a post; get posts after this cursor
    - `before`: UUID of a post; get posts before this cursor
    - `sort`: sorting order
    - `size`: maximum number of posts to return
    """
    if sr is not None:
        subreddit = crud.subreddit.get_by_sr(sr)
        if not subreddit:
            raise SubredditNotFoundException
    else:
        subreddit = None

    # act depending on which cursor is passed
    if not after and not before:
        results = crud.post_meta.get_posts(
            subreddit, current_user, None, None, sort, size
        )
    elif after:
        cursor = crud.post_meta.get(after)
        if cursor is None:
            raise PaginationInvalidCursorException
        results = crud.post_meta.get_posts(
            subreddit, current_user, cursor, schemas.CursorDirection.after, sort, size
        )
    elif before:
        cursor = crud.post_meta.get(before)
        if cursor is None:
            raise PaginationInvalidCursorException
        results = crud.post_meta.get_posts(
            subreddit, current_user, cursor, schemas.CursorDirection.before, sort, size
        )
    else:  # both after and before specified
        raise PaginationAfterAndBeforeException

    # convert list of dicts to list of PostMeta schemas
    meta_list = [schemas.PostMeta(**row) for row in results]

    # retrieve post content
    content_list = crud.post_content.filter_by_uids([meta.uid for meta in meta_list])

    # build new cursors for pagination
    basepath = f"{request.url.path}?sort={sort}"
    next = f"{basepath}&after={meta_list[-1].uid}" if meta_list else None
    prev = f"{basepath}&before={meta_list[0].uid}" if meta_list else None
    links = schemas.Pagination(next=next, prev=prev)

    # create list of Post schemas by matching metadata and content
    post_list = [
        schemas.Post(metadata=meta, content=content_list.get(uid=meta.uid))
        for meta in meta_list
    ]

    return schemas.PostList(links=links, data=post_list)


@router.get(
    "/{uid}",
    name="Get a Post",
    response_model=schemas.Post,
    status_code=status.HTTP_200_OK,
)
def get_post(uid: UUID4):
    """
    Return a post.

    - `uid`: UUID of the post to return
    """
    post_meta = crud.post_meta.get(uid)
    post_content = crud.post_content.get(uid)
    if not post_meta or not post_content:
        raise PostNotFoundException

    return schemas.Post(metadata=post_meta, content=post_content)


@router.get(
    "/{uid}/tree",
    name="Get a post tree",
    response_model=schemas.PostTree,
    status_code=status.HTTP_200_OK,
)
def get_post_tree(
    uid: UUID4,
    sort: Optional[schemas.CommentSort] = schemas.CommentSort.top,
    current_user: Optional[models.User] = Depends(deps.get_current_user_or_none),
):
    """
    Return the post tree for a post with the comments sorted by order given by the
    `sort` parameter.

    - `uid`: UUID of the post whose post tree to return
    - `sort`: sorting order
    """
    post_meta = crud.post_meta.get(uid)
    if not post_meta:
        raise PostNotFoundException

    # get nested metadata tree-like dict and list of thing uids
    meta_tree, thing_uids = crud.post_meta.get_post_tree(post_meta, current_user)

    # add subreddit sr to post
    subreddit = crud.post_meta.get_subreddit(post_meta)
    meta_tree["sr"] = subreddit.sr

    # get associated contents of things
    thing_contents = crud.thing_content.filter_by_uids(thing_uids)

    # restructure dict to match schema and match content to metadata
    stack = [meta_tree]
    while stack:
        thing = stack.pop()
        meta_list = list(thing)  # assign all metadata keys to a list
        thing["metadata"] = dict()  # new key for holding all metadata
        thing["content"] = thing_contents.get(uid=thing["uid"])  # match content
        for i in meta_list:
            if i != "parent":  # move metadata to 'metadata' dict
                thing["metadata"][i] = thing[i]
                del thing[i]
            if i == "parent":  # rename 'parent' key to 'children' key
                thing["children"] = thing.pop(i)
                for child in thing["children"]:
                    stack.append(child)

    # sort tree
    stack = [meta_tree]
    while stack:
        thing = stack.pop()
        if isinstance(thing.get("children"), list):
            if sort == schemas.CommentSort.new:
                thing["children"].sort(
                    key=lambda child: (
                        child["metadata"]["created_at"],
                        child["metadata"]["_id"],
                    ),
                    reverse=True,
                )
            elif sort == schemas.CommentSort.old:
                thing["children"].sort(
                    key=lambda child: (
                        child["metadata"]["created_at"],
                        child["metadata"]["_id"],
                    )
                )
            elif sort == schemas.CommentSort.top:
                thing["children"].sort(
                    key=lambda child: (
                        child["metadata"]["count"],
                        child["metadata"]["_id"],
                    ),
                    reverse=True,
                )
            for child in thing["children"]:
                stack.append(child)

    return meta_tree


@router.post(
    "",
    name="Submit a post",
    response_model=schemas.Post,
    status_code=status.HTTP_201_CREATED,
)
def submit_post(
    post: schemas.PostCreate, current_user: models.User = Depends(deps.get_current_user)
):
    """
    Submit a post to the subreddit `sr`.

    For posts with type `self`, the `text` parameter should contain the body of the self
    post.
    For all other types, the `url` parameter must contain a valid URL.


    Otherwise, `text` will be the body of the self-post.

    - `nsfw`: `boolean` value
    - `spoiler`: `boolean` value
    - `sr`: subreddit name
    - `text`: content of the post
    - `title`: title of the post, up to 300 characters long
    - `type`: one of `link`, `self`, `image`, `video`
    - `url`: a valid URL
    """
    # check if subreddit exists
    sr = crud.subreddit.get_by_sr(post.metadata.sr)
    if sr is None:
        raise SubredditNotFoundException

    # create post
    created_post_meta = crud.post_meta.create(post.metadata)
    created_post_content = crud.post_content.create(created_post_meta.uid, post.content)
    crud.post_meta.set_author(created_post_meta, current_user)
    crud.post_meta.set_subreddit(created_post_meta, sr)

    return schemas.Post(metadata=created_post_meta, content=created_post_content)


@router.put(
    "/{uid}",
    name="Update a post",
    response_class=Response,
    status_code=status.HTTP_204_NO_CONTENT,
)
def update_post(
    uid: UUID4,
    post: schemas.PostUpdate,
    current_user: models.User = Depends(deps.get_current_user),
):
    """
    Update a post.

    - `uid`: UUID of the post to update
    - `nsfw`: `boolean` value
    - `spoiler`: `boolean` value
    - `text`: content of the post
    - `title`: title of the submission, up to 300 characters long
    - `url`: a valid URL
    """
    old_post_meta = crud.post_meta.get(uid)
    old_post_content = crud.post_content.get(uid)
    if not old_post_meta or not old_post_content:
        raise PostNotFoundException
    if crud.post_meta.get_author(old_post_meta) != current_user:
        raise UnauthorizedUpdateException
    if old_post_meta.type == schemas.PostType.link.value and (
        post.content.text is not None or post.content.url is None
    ):
        raise PostTypeRequestInvalidException
    elif old_post_meta.type != schemas.PostType.link.value and (
        post.content.text is None or post.content.url is not None
    ):
        raise PostTypeRequestInvalidException

    crud.post_meta.update(old_post_meta, post.metadata)
    crud.post_content.update(old_post_content, post.content)
