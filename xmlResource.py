from flask import Flask, abort, request, jsonify
from dataPretreatment import data_pretreatment
from createReportXml import create_report_xml

app = Flask(__name__)


@app.route('/add_task/', methods=['POST'])
def add_task():
    title_description, rolemap, dataset, sqlQuery, report_parameter = data_pretreatment(request)
    create_report_xml(title_description, rolemap, dataset, sqlQuery, report_parameter)
    return jsonify({'result': 'success'})


if __name__ == "__main__":
    # 将host设置为0.0.0.0，则外网用户也可以访问到这个服务
    app.run(host="0.0.0.0", port=8383, debug=True)
