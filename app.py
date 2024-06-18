from flask import Flask
from compatibility import compatibility_blueprint
from imageSave import image_save_blueprint
from recSystem import rec_system_blueprint

app = Flask(__name__)
app.register_blueprint(compatibility_blueprint, url_prefix='/compatibility')
app.register_blueprint(image_save_blueprint, url_prefix='/image_save')
app.register_blueprint(rec_system_blueprint, url_prefix='/rec_system')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
