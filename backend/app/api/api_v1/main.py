from fastapi import APIRouter

from app.api.api_v1.endpoints import (account, auth, blob, comments, posts,
                                      subreddits, subscription, users, vote)

router = APIRouter()
router.include_router(account.router, prefix="/account")
router.include_router(auth.router, prefix="/auth")
router.include_router(blob.router, prefix="/upload")
router.include_router(comments.router, prefix="/comments")
router.include_router(posts.router, prefix="/posts")
router.include_router(subreddits.router, prefix="/subreddits")
router.include_router(subscription.router, prefix="/subscription")
router.include_router(users.router, prefix="/users")
router.include_router(vote.router, prefix="/vote")
