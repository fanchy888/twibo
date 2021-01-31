import os
from flask import Flask
from dotenv import load_dotenv


APP_ROOT = os.path.join(os.path.dirname(__file__), '..')
env_path = os.path.join(APP_ROOT, '.env')

load_dotenv(env_path)


