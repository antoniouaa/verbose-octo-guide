import dotenv
import os

dotenv.load_dotenv()

from sequencer import create_app
from sequencer.config import ProductionConfig, DevelopmentConfig

config = DevelopmentConfig if os.getenv("DEV_ENV_FLAG") else ProductionConfig
app, _ = create_app()
