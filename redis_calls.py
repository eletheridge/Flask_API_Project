import redis


class RedisClient:
    """
    Class for interfacing with redis server
    """
    def __init__(self):
        self.r = redis.Redis(host='redis', port=6379, decode_responses=True)

    def set(self, key, value):
        results = self.r.set(key, value)
        return results

    def get(self, key):
        try:
            if self.r.exists(key):
                return self.r.get(f'{key}')
            else:
                return "Key does not exist"
        except Exception as e:
            return e

