from flask import Flask
import logging
from config import Config# factory run app
import routes

def create_app()->Flask:
    app = Flask(__name__)
    # app.config.from_object(Config)
    app.config.from_object(Config)
    app.secret_key = "my_secret_key"

    # production logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )

    # from routes import api_bp
    # import routes
    # print("Loaded routes from:", routes.__file__)

    app.register_blueprint(routes.api_bp)
    # print("Registered routes:", app.url_map)
    return app


if __name__ == "__main__":
    # print("welcome to the weather ai agent!")
    app=create_app()
    app.run(host="127.0.0.1", port=5000, debug=True)


    # while True:
    #     query = input("\nenter your question!")
    #     if query.lower() in ['exit', 'bye', 'quit']:
    #         break
