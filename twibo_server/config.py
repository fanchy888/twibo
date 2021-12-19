class Config:
    def __init__(self):
        pass

    @property
    def sqldb_url(self):
        return 'mysql+pymysql://root:fan4308832@localhost:3306/twibo'


config = Config()