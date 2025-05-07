from flask import Flask
from api.routes import api
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)
app.register_blueprint(api)

@app.route('/')
def index():
    return 'Сервер працює!'

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
