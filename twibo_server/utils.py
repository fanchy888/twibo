import random
import time
from base64 import b64encode, b64decode
from datetime import datetime
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5

from config import config


def rsa_decrypt(message):
    private_key = RSA.import_key(config.rsa_private_key)
    cipher_rsa = PKCS1_v1_5.new(private_key)
    return cipher_rsa.decrypt(b64decode(message), 0).decode('utf-8')


def generate_id(prefix=''):
    ts = time.time() + random.uniform(-1000, 1000)
    ts = datetime.fromtimestamp(ts).strftime('%y%m%d%H%M%S')
    encode_ts = ts.encode('utf-8')
    return f'{prefix}-{b64encode(encode_ts).decode("utf-8")}'
