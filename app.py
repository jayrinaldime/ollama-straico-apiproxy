from flask import Flask
import logging
import os

log_level = os.environ.get('LOG_LEVEL', 'ERROR').upper()

# Configure the logging
logging.basicConfig(
    level=log_level,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

app = Flask(__name__)
