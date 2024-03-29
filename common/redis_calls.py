import redis


class RedisClient:
    """
    Class for interfacing with redis server
    """
    def __init__(self):
        self.r = redis.Redis(host='redis', port=6379, decode_responses=True)

    def set(self, key, value):
        """
        Sets key/value pair in redis
        :return: Result of set
        """
        results = self.r.set(key, value)
        return results

    def get(self, key):
        """
        Gets value from redis
        :param key: Key to be retrieved
        :return: Value of key
        """
        try:
            if self.r.exists(key):
                return self.r.get(f'{key}')
            else:
                return "Key does not exist"
        except Exception as e:
            return e

    def expire(self, key, exp_time):
        """
        Sets key to expire in specified time frame.
        :param key: Key to be expired
        :param exp_time: Time in seconds for key to expire
        :return: Result of expire - Boolean value
        """
        try:
            if self.r.exists(key):
                return self.r.expire(key, exp_time)
            else:
                return "Key does not exist"
        except Exception as e:
            return e
