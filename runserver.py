from debuild import app
from debuild.utils import load_modules_from_json

load_modules_from_json('modules.json')

app.run(debug=True)
