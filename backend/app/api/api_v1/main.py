from fastapi import APIRouter

from app.api.api_v1.endpoints import account, auth, submit, subreddits, users

router = APIRouter()
router.include_router(account.router, prefix="/account")
router.include_router(auth.router, prefix="/auth")
router.include_router(submit.router)
router.include_router(subreddits.router, prefix="/subreddits")
router.include_router(users.router, prefix="/users")
