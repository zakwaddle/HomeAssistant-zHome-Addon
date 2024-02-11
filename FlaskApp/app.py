from flask import Flask, send_from_directory
from blueprints.logs import log_blueprint
from blueprints.devices import device_blueprint
from blueprints.sensors import sensor_blueprint
from blueprints.configs import config_blueprint
from flask_cors import CORS
import os

app = Flask(__name__, static_folder='static')
CORS(app)


# Serve React App
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_react_app(path):
    if path != "" and os.path.exists(app.static_folder + '/react/' + path):
        return send_from_directory(app.static_folder + '/react', path)
    else:
        return send_from_directory(app.static_folder + '/react', 'index.html')


app.register_blueprint(log_blueprint, url_prefix='/api/home/logs')
app.register_blueprint(device_blueprint, url_prefix='/api/home/devices')
app.register_blueprint(sensor_blueprint, url_prefix='/api/home/sensors')
app.register_blueprint(config_blueprint, url_prefix='/api/home/configs')


if __name__ == "__main__":
    app.run("0.0.0.0")
