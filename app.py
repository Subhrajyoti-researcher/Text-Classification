from flask import Flask,request,jsonify
from flask_cors import CORS
import main
import SSGLog

logger = SSGLog.setup_custom_logger('Neurobot')
logger.info("********************Loger APP******************")





app = Flask(__name__)
CORS(app)


@app.route("/predict",methods=['POST'])
def predict():
    
    
    try:

        doc = request.json["document"]
        logger.debug("Input--> %s",doc)
        out = main.email_classification(doc)
        return jsonify({"result":out})
    
    except Exception as e:
        print(e)
        return jsonify({"result":"Something went wrong! Contact with developer team!"})

if __name__ == "__main__":
    app.run('172.25.1.26',port=8009)