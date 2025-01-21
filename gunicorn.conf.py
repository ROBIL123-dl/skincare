bind = "unix:/run/gunicorn.sock"
workers = 3
threads = 2
timeout = 120
accesslog = "-"
errorlog = "-"
loglevel = "info"
