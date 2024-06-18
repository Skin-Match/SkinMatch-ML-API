import os
from flask import Flask
from compatibility import compatibility_blueprint
from imageSave import image_save_blueprint
from recSystem import rec_system_blueprint
from recommendation import recommendations_blueprint


app = Flask(__name__)

app.register_blueprint(compatibility_blueprint, url_prefix='')
app.register_blueprint(image_save_blueprint, url_prefix='')
app.register_blueprint(rec_system_blueprint, url_prefix='')
app.register_blueprint(recommendations_blueprint, url_prefix='')


if __name__ == '__main__':
    # Set the port to the value of the PORT environment variable if available, or 8080 if not
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=True)
