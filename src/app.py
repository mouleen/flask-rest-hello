"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, jsonify,request
from flask_cors import CORS
from utils import APIException
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

# db_url = os.getenv("DATABASE_URL")
#if db_url is not None:
#    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
#else:
#    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#MIGRATE = Migrate(app, db)
#db.init_app(app)
CORS(app)
#setup_admin(app)
image_url=os.getenv("IMAGE_URL")
bg_color=os.getenv("BG_COLOR")
fg_color=os.getenv("FG_COLOR")
# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def handle_hello():
     links_html=""
     return """
        <div style="width:800px;background-color:#"""+bg_color+""";background-image: linear-gradient(#"""+bg_color+""", white);color:#"""+fg_color+"""; text-align: center; margin:50px auto; border-radius: 25px;padding:20px auto;font-family: Monaco, monospace;font-size:16px;">
        <img style="max-height: 80px;margin:50px auto;" src='"""+image_url+"""' />
        <h2>Default Endpoint</h2>
        <p style="font-size:24px;">APP PATH </p><script>document.write('<input style="margin:0px 20px 100px 20px; border-radius: 15px;padding:20px; width: 600px;font-size:14px;font-family: Monaco, monospace;background:honeydew;" type="text" value="'+window.location.href+'" />');</script></div>"""
    #response_body = {
    ##    "msg": "Hello, this is your GET /user response "
    #}

    #return jsonify(response_body), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 8081))
    app.run(host='0.0.0.0', port=PORT, debug=False)
