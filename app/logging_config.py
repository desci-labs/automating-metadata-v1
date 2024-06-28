# logging_config.py
import logging
import json
from logging.config import dictConfig

class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            'level': record.levelname,
            'time': self.formatTime(record, self.datefmt),
            'message': record.getMessage(),
            'name': record.name,
            'pathname': record.pathname,
            'lineno': record.lineno,
        }
        if record.exc_info:
            log_record['exc_info'] = self.formatException(record.exc_info)
        return json.dumps(log_record)

def setup_logging():
    dictConfig({
        'version': 1,
        'formatters': {
            'json': {
                '()': JsonFormatter,
            }
        },
        'handlers': {
            'stdout': {
                'class': 'logging.StreamHandler',
                'formatter': 'json',
                'stream': 'ext://sys.stdout',
            },
            'file': {
                'class': 'logging.FileHandler',
                'formatter': 'json',
                'filename': 'app.log',
            }
        },
        'root': {
            'level': 'INFO',
            'handlers': ['stdout', 'file']
        }
    })

setup_logging()
