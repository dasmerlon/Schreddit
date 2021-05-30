import redis as original_redis

# Initialize Redis DB for session management.
redis = original_redis.Redis(host="localhost", port=6379, db=0)
