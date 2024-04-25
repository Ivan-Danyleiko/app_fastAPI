class Config:
    SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://postgres:567234@localhost:5432/fine_app"


config = Config


class ConfigAuthKey:
    KEY = "974790aec4ac460bdc11645decad4dce7c139b7f2982b7428ec44e886ea588c6"
    ALG = "HS256"


config_auth_key = ConfigAuthKey
