import os
from logging import config as log_config

LOG_DIR = os.getenv('LOG_DIR', 'logs')

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "root": {
        "level": "DEBUG",
        "handlers": ["debug", "info", 'error']
    },
    "handlers": {
        "debug": {
            "formatter": "stdout",
            "class": "logging.StreamHandler",
            "level": "DEBUG"
        },
        "info": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": os.path.join(LOG_DIR, 'info.log'),
            "formatter": "info",
        },
        "error": {
            "level": "ERROR",
            "class": "logging.FileHandler",
            "filename": os.path.join(LOG_DIR, 'error.log'),
            "formatter": "error",
        },
        "message_sender": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": os.path.join(LOG_DIR, 'msg.log'),
            "formatter": "message_sender",
        }
    },
    "loggers": {
        "debug": {
            "handlers": ['debug'],
            'level': 'DEBUG',
            'propagate': False,
        },

        "info": {
            "handlers": ["info"],
            "level": "INFO",
            "propagate": False,
        },
        "error": {
            "handlers": ["error"],
            "level": "ERROR",
            "propagate": False,
        },
        "message_sender": {
            "handlers": ["message_sender"],
            "level": "INFO",
            "propagate": False,
        },
    },
    "formatters": {
        "message_sender": {
            "format": (
                u"%(asctime)s %(message)s "
            ),
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },

        "stdout": {
            "format": ("%(asctime)s : %(levelname)s : %(module)s : %(funcName)s : %(lineno)d : "
                       "(Process Details : (%(process)d, %(processName)s), "
                       "Thread Details : (%(thread)d, %(threadName)s))\n"
                       "Log : %(message)s"),
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "info": {
            "format": (
                u"%(asctime)s [%(levelname)-8s] "
                "(%(module)s.%(funcName)s) : %(lineno)d : %(message)s "
            ),
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "error": {
            "format": (
                u"%(asctime)s [%(levelname)-8s] "
                "(%(module)s.%(funcName)s) : %(lineno)d : %(message)s"
            ),
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
}

log_config.dictConfig(LOGGING)
