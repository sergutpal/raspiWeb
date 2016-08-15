import redis

config = {
    'host': '192.168.1.20',
    'port': 6379,
    'db': 1,
}

r = redis.StrictRedis(**config)

r.publish('toPI', 'hola soy SGP y esto funciona :-)')
