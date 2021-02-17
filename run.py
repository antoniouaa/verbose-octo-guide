import dotenv
import os

dotenv.load_dotenv()

from sequencer import create_app, db
from sequencer.config import ProductionConfig, DevelopmentConfig

config = DevelopmentConfig if os.getenv("DEV_ENV_FLAG") else ProductionConfig
app, db = create_app()
with app.app_context():
    db.create_all()
