from .base_redis import session as redis
from .crud_comment_content import comment_content
from .crud_comment_meta import comment_meta
from .crud_post_content import post_content
from .crud_post_meta import post_meta
from .crud_subreddit import subreddit
from .crud_thing_content import thing_content
from .crud_thing_meta import thing_meta
from .crud_user import user

# For a new basic set of CRUD operations create a new file crud_newmodel with

# from app.crud.base import CRUDBase
# from app.models import NewFeature
# from app.schemas import NewFeatureCreate, NewFeatureUpdate
# new_feature = CRUDBase[NewFeature, NewFeatureCreate, NewFeatureUpdate](NewFeature)

# and import new_feature here.
