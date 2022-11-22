import os, json
import subprocess
from flask import Flask, request, jsonify
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)

### swagger specific ##########
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Python-Flask-REST-API"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
### end swagger specific ###

@app.route('/', methods = ['GET', 'POST'])
def get_transform():
    if request.method == 'GET':
        # with open('payload.json', 'w') as f:
        #     f.write('{"RequestType":"GET"}')
        # with open('transform.dw', 'w') as f:
        #     f.write('output json --- payload')
        # dataweave = subprocess.run(["./dw", "-i", "payload", "payload.json", "-f", "transform.dw"], stdout=subprocess.PIPE, text=True)
        # print(dataweave.stdout)
        return jsonify(RequestType="GET")
    
    elif request.method == 'POST':
        rdata = request.get_json()
        
        rawData = rdata['Data']
        DW_Script = rdata['DataWeaveScript']
        
        with open('payload.json', 'w') as f:
            json.dump(rawData, f)
        with open('transform.dwl', 'w') as ft:
            ft.write(DW_Script)
        
        dataweave = subprocess.run(["./dw", "-i", "payload", "payload.json", "-f", "transform.dwl"], stdout=subprocess.PIPE, text=True)
        # print(dataweave.stdout)
        return jsonify(Output=(dataweave.stdout))
        # return jsonify(rawData)


if __name__ == "__main__":
   # app.run(debug=True)
    app.run(debug=True, host=os.getenv('IP', '127.0.0.1'), port=int(os.getenv('PORT', 8888)))
