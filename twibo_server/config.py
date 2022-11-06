import yaml


def load():
    with open('./config.yaml') as f:
        cfg_data = f.read()
    return yaml.load(cfg_data, Loader=yaml.FullLoader)


class Config:
    def __init__(self):
        self.cfg_data = load()['twibo']

    @property
    def sqldb_url(self):
        return self.cfg_data['sqldb']

    @property
    def rsa_private_key(self):
        path = self.cfg_data['rsa_path']
        with open(path, 'r') as f:
            rsa_privat_key = str(f.read())
        return rsa_privat_key

    @property
    def static_url(self):
        return self.cfg_data['static_file_path']

    @property
    def img_url(self):
        return self.cfg_data['static_file_path'] + 'img/'

    @property
    def img_type(self):
        return {'jpg', 'png', 'jpeg', 'gif'}


config = Config()
