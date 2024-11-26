import os
import datetime
from gunicorn.glogging import Logger


class CustomLogger(Logger):

    def now(self):
        return datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')


logger_class = CustomLogger

access_log_format = '%({x-real-ip}i)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
accesslog = "logs/access.log"
bind = "0.0.0.0:" + os.environ.get("CONTAINER_PORT")
capture_output = True  # Capture stdio
enable_stdio_inheritance = True  # Django errors from stderr to error log
errorlog = "logs/error.log"
graceful_timeout = 3600
keep_alive = 3600
log_level = "debug"
pid = "payback.pid"
threads = 1
timeout = 3600
workers = os.environ.get("UWSGI_WORKERS")
