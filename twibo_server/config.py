
class Config:
    def __init__(self):
        self._rsa_privat_key = None

    @property
    def sqldb_url(self):
        return 'mysql+pymysql://root:fan4308832@localhost:3306/twibo'

    @property
    def rsa_private_key(self):
        if not self._rsa_privat_key:
            path = './private.rsa'
            with open(path, 'r') as f:
                self._rsa_privat_key = str(f.read())
        return self._rsa_privat_key

    @property
    def static_path(self):
        return '../static/'

    @property
    def avatar_type(self):
        return {'jpg', 'png', 'jpeg', 'gif'}


config = Config()
