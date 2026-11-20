


from databases import Database
from app.config import Config

config = Config()

database = Database(
    config.DATABASE_URL.render_as_string(hide_password=False)
)
