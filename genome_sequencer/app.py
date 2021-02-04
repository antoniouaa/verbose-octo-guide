# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy

# import os
# import dotenv

# from . import views

# dotenv.load_dotenv()

# app = Flask(__name__, instance_relative_config=True)
# app.register_blueprint(views.genome_blueprint)

# app.config.from_object(os.getenv("APP_SETTINGS"))
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# db = SQLAlchemy(app)


# if __name__ == "__main__":
#     app.run()
