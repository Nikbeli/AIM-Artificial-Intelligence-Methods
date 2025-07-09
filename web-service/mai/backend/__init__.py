import importlib
import os
import traceback

import matplotlib
from apiflask import APIBlueprint, APIFlask
from flask_cors import CORS

matplotlib.use("agg")

cors = CORS()
api_bp = APIBlueprint("api", __name__, url_prefix="/api/v1")
dataset_path: str | None = None


class Config:
    SECRET_KEY = "secret!"
    SEND_FILE_MAX_AGE_DEFAULT = -1


def create_app():
    global dataset_path

    # Create and configure app
    app = APIFlask(
        "MAI Service",
        title="MAI Service API",
        docs_path="/",
        version="1.0",
        static_folder="",
        template_folder="",
    )
    app.config.from_object(Config)

    dataset_path = os.path.join(app.instance_path, "dataset")
    os.makedirs(dataset_path, exist_ok=True)

    @app.errorhandler(Exception)
    def my_error_processor(error):
        traceback.print_exception(error)
        return {"message": str(error), "detail": "No details"}, 500

    # Import custom REST methods
    importlib.import_module("backend.api")

    # Enable REST API
    app.register_blueprint(api_bp)

    # Enable app extensions
    cors.init_app(app)

    return app
