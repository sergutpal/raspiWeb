import redis

def cbSGP(message):
  print 'El callback funciona: ', message['data']

config = {
    'host': '192.168.1.20',
    'port': 6379,
    'db': 1,
}

r = redis.StrictRedis(**config)

pubsub = r.pubsub()
pubsub.subscribe(**{'toPI': cbSGP})

while True:
  pass
