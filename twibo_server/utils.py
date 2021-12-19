import random
import time
from datetime import datetime
from base64 import b64encode


def generate_id(prefix=''):
    ts = time.time() + random.uniform(-1000, 1000)
    ts = datetime.fromtimestamp(ts).strftime('%y%m%d%H%M%S')
    encode_ts = ts.encode('utf-8')
    return f'{prefix}-{b64encode(encode_ts).decode("utf-8")}'


if __name__ == '__main__':
    for _ in range(10):
        print(generate_id())