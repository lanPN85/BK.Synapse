bind = '0.0.0.0:5000'

workers = 8
worker_class = 'gevent'
worker_connections = 1000
timeout = 30
keepalive = 30
graceful_timeout = 30
