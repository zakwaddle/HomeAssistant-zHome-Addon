from flask import Flask
from blueprints.logs import log_blueprint
from blueprints.devices import device_blueprint
from blueprints.sensors import sensor_blueprint
from blueprints.configs import config_blueprint
from flask_cors import CORS, cross_origin
from flask_sse import sse
import os

app = Flask(__name__)
app.config["REDIS_URL"] = os.getenv('REDIS_URL')
CORS(app)


@app.route('/api/home/stream', methods=['GET', 'OPTIONS'])
@cross_origin()
def stream():
    print("stream request")
    return sse.stream()


app.register_blueprint(sse, url_prefix='/api/home/stream')
app.register_blueprint(log_blueprint, url_prefix='/api/home/logs')
app.register_blueprint(device_blueprint, url_prefix='/api/home/devices')
app.register_blueprint(sensor_blueprint, url_prefix='/api/home/sensors')
app.register_blueprint(config_blueprint, url_prefix='/api/home/configs')


if __name__ == "__main__":
    app.run("0.0.0.0")
