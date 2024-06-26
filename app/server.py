from flask import Flask, request, jsonify
import os
# Import your script
from langchain_orcid2 import run as run_langchain
from auth import validate_api_key
import logging
import json
from logging.config import dictConfig

# Read environment variables
cr_mailto = os.getenv('CR_MAILTO')
pyalex_email = os.getenv('PYALEX_EMAIL')

# Configure logging
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
        }
    },
    'root': {
        'level': 'INFO',
        'handlers': ['stdout']
    }
})

app = Flask(__name__)

# @app.before_request
# def log_request_info():
#     app.logger.info('Request received', extra={
#         'method': request.method,
#         'url': request.url,
#         'headers': dict(request.headers),
#         'body': request.get_data(as_text=True)
#     })

@app.before_request
def log_request_info():
    try:
        body = request.get_data(as_text=True)
        if len(body) > 1000:  # Limit body size for logging
            body = body[:1000] + '... [truncated]'

        app.logger.info('Request received', extra={
            'method': request.method,
            'url': request.url,
            'headers': dict(request.headers),
            'body': body
        })
    except Exception as e:
        app.logger.error('Error logging request info', exc_info=e)


@app.route('/invoke-script', methods=['POST'])
@validate_api_key

def invoke_script():
    data = request.json  # Assuming JSON data is sent from the web app
    pdf = data.get("pdf")
    doi = data.get("doi")
    # Call your script with the appropriate inputs

    if doi is not None:
        output = run_langchain(pdf, doi, cr_mailto, pyalex_email)
    elif pdf is None and doi is not None: 
        output = run_langchain(doi, cr_mailto, pyalex_email)
    else: 
        output = run_langchain(pdf, cr_mailto, pyalex_email)
    return jsonify({'output': output})

@app.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'metadata server healthy'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)