import io
import random
import time
import logging
from PIL import Image

from base64 import b64encode, b64decode
from datetime import datetime
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5

from twibo_server.config import config

logging.basicConfig(level=logging.DEBUG, format="[%(asctime)s][%(name)s][%(levelname)s]%(message)s",
                    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger('twibo')
logger.setLevel(logging.DEBUG)


def rsa_decrypt(message):
    private_key = RSA.import_key(config.rsa_private_key)
    cipher_rsa = PKCS1_v1_5.new(private_key)
    return cipher_rsa.decrypt(b64decode(message), 0).decode('utf-8')


def generate_id(prefix=''):
    ts = time.time() + random.uniform(-1000, 1000)
    ts = datetime.fromtimestamp(ts).strftime('%y%m%d%H%M%S')
    encode_ts = ts.encode('utf-8')
    return f'{prefix}-{b64encode(encode_ts).decode("utf-8")}'


def create_thumbnail(file, target_size=300):
    image = Image.open(io.BytesIO(file))
    x, y = image.size
    factor = max(x/target_size, y/target_size)
    thumb = image.resize((int(x/factor), int(y/factor)), Image.ANTIALIAS)
    return thumb


def create_avatar(file, target_size=200):
    image = Image.open(io.BytesIO(file))
    x, y = image.size
    half_edge = int(min(x, y)/2)
    center = (int(x/2), int(y/2))
    square = image.crop((center[0]-half_edge, center[1]-half_edge, center[0]+half_edge, center[1]+half_edge))
    return square.resize((target_size, target_size), Image.ANTIALIAS)


def generate_pwd():
    new = random.sample('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMOPQRSTUVWXYZ!@#$%^&*', 16)
    print(''.join(new))
    return ''.join(new)


def send_email():
    pass


if __name__ == '__main__':
    generate_pwd()