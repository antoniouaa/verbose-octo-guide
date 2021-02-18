import dotenv
import os
from sqlalchemy.exc import IntegrityError

dotenv.load_dotenv()

from sequencer import create_app, db
from sequencer.user import models
from sequencer.config import ProductionConfig, DevelopmentConfig

config = DevelopmentConfig if os.getenv("DEV_ENV_FLAG") else ProductionConfig
app = create_app()
with app.app_context():
    db.create_all()
    username = os.getenv("ROOT_USERNAME")
    password = os.getenv("ROOT_PASSWORD")
    if models.User.query.filter_by(username=username).first() is None:
        models.create_user(username=username, password=password)
