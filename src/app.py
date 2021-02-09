from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import os
import dotenv

dotenv.load_dotenv()


app = Flask(__name__)
app.config.from_object(os.getenv("APP_SETTINGS"))
db = SQLAlchemy(app)


from views import genome_blueprint

app.register_blueprint(genome_blueprint)


if __name__ == "__main__":
    app.run()
