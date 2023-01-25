import aioredis
import os
from aioredis import Redis


async def get_redis() -> Redis:
    """
    系统缓存
    :return: cache 连接池
    """
    # 从URL方式创建redis连接池
    sys_cache_pool = aioredis.ConnectionPool.from_url(
        f"redis://{os.getenv('REDIS_HOST', '127.0.0.1')}:{os.getenv('REDIS_PORT', 6379)}",
        password=os.getenv('REDIS_PASSWORD', 512512),
        db=os.getenv('REDIS_DB', 0),
        encoding='utf-8',
        decode_responses=True
    )

    return Redis(connection_pool=sys_cache_pool)
