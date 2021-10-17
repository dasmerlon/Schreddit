from fastapi import APIRouter

from app.api.api_v1.endpoints import (auth, blob, comments, posts, search,
                                      subreddits, subscriptions, users, vote)

router = APIRouter()
router.include_router(auth.router, prefix="/auth", tags=["users"])
router.include_router(blob.router, prefix="/blob", tags=["content"])
router.include_router(comments.router, prefix="/comments", tags=["content"])
router.include_router(posts.router, prefix="/posts", tags=["content"])
router.include_router(search.router, prefix="/search", tags=["subreddits"])
router.include_router(subreddits.router, prefix="/r", tags=["subreddits"])
router.include_router(subscriptions.router, prefix="/subscription", tags=["subreddits"])
router.include_router(users.router, prefix="/users", tags=["users"])
router.include_router(vote.router, prefix="/vote", tags=["content"])
