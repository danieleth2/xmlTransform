from flask import Flask, abort, request, jsonify
import json
from dataPretreatment import data_pretreatment

app = Flask(__name__)


@app.route('/add_task/', methods=['POST'])
def add_task():
    data_pretreatment(request)

    return jsonify({'result': 'success'})


if __name__ == "__main__":
    # 将host设置为0.0.0.0，则外网用户也可以访问到这个服务
    app.run(host="0.0.0.0", port=8383, debug=True)
