from fastapi import HTTPException, status


class PaginationAfterAndBeforeException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The parameters 'after' and 'before' should not be specified both.",
        )


class PaginationInvalidCursorException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The cursor does not reference an existing post.",
        )


class PostNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND, detail="This post does not exist."
        )


class CommentNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND, detail="This comment does not exist."
        )


class ThingNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND, detail="This thing does not exist."
        )


class ThingAlreadyVoted(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_304_NOT_MODIFIED,
            detail="This thing is already voted in the specified direction.",
        )


class ParentNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The thing being replied to does not exist.",
        )


class PostTypeRequestInvalidException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Posts must only include either 'text' or 'url', "
            "depending of the post type.",
        )


class SubredditNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This subreddit does not exist.",
        )


class SubredditAlreadySubscribed(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="This subreddit is already subscribed.",
        )


class SubredditNotSubscribed(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="This subreddit is already unsubscribed.",
        )


class InvalidCredentialsException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials.",
            headers={"WWW-Authenticate": "Bearer"},
        )


class UnauthorizedUpdateException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not authorized to modify this resource.",
        )
