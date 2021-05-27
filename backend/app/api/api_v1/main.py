from fastapi import APIRouter

from app.api.api_v1.endpoints import account, auth, posts, subreddits, users

router = APIRouter()
router.include_router(account.router, prefix="/account")
router.include_router(auth.router, prefix="/auth")
router.include_router(posts.router, prefix="/posts")
router.include_router(subreddits.router, prefix="/subreddits")
router.include_router(users.router, prefix="/users")
