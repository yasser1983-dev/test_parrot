import redis
from django.conf import settings
from redis.exceptions import ConnectionError

def is_rq_worker_alive():
    """
    Verifica si hay al menos un worker de RQ escuchando la cola 'default'.
    """
    try:
        redis_conn = redis.from_url(settings.CACHES['default']['LOCATION'])
        workers = redis_conn.smembers('rq:workers')
        return len(workers) > 0  # True si hay workers registrados
    except ConnectionError:
        return False