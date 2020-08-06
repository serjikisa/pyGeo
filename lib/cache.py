"""
Cache or get cached IP addresses from Redis
"""
import redis
from datetime import datetime


class RedisCache:
  def __init__(self, host, port):
    self.r = redis.StrictRedis(
        host=host,
        port=port,
        charset="utf-8",
        decode_responses=True,
        password='')

  def set_time(self, key):
    self.r.set(key, str(datetime.now()))

  def get_time(self, key):
    val = self.r.get(key)
    if val is None:
      return None

    return datetime.strptime(val, '%Y-%m-%d %H:%M:%S.%f')

  def get_duration(self, key):
    val = self.get_time(key)
    if val is None:
      return None
    return (datetime.now() - val).seconds
