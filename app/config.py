


from pydantic_settings import BaseSettings
from sqlalchemy.engine import URL


class Config(BaseSettings):
    MYSQL_USER: str = "root"
    MYSQL_HOST: str = "127.0.0.1"
    MYSQL_PORT: int = 3306
    MYSQL_DATABASE: str = "poll_db"
    MYSQL_PASSWORD: str
    USER_SERVICE_URL: str = "http://127.0.0.1:8000"

    @property
    def DATABASE_URL(self):
        return URL.create(
            drivername="mysql+aiomysql",
            username=self.MYSQL_USER,
            password=self.MYSQL_PASSWORD,
            host=self.MYSQL_HOST,
            port=self.MYSQL_PORT,
            database=self.MYSQL_DATABASE
        )
