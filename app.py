from flask import Flask
from debuild.blueprints.frontend import frontend
from debuild.blueprints.apiv1 import api as apiv1


app = Flask(__name__)

app.register_blueprint(frontend)
app.register_blueprint(apiv1, url_prefix='/api/v1')


if __name__ == '__main__':
    app.run(debug=True)
