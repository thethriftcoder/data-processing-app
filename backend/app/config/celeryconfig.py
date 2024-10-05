from app.config.redis import redis_url


broker_url = result_backend = redis_url

# list of all modules that contain celery tasks
include = ["app.services.sensor"]
