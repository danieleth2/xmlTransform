# -*- coding: utf-8 -*-
from flask import Flask, abort, request, jsonify
from dataPretreatment import data_pretreatment
from createReportXml import create_report_xml, create_files
from flask import send_file, send_from_directory
import os
app = Flask(__name__)


@app.route('/create/', methods=['POST'])
def add_task():
    title_description, rolemap, dataset, sqlQuery, report_parameter = data_pretreatment(request)
    xml = create_report_xml(title_description, rolemap, dataset, sqlQuery, report_parameter)
    file_name = title_description[0]
    create_files(xml, file_name)
    return jsonify({'result': '创建报表srdl成功，文件名为' + file_name + '.srdl'})


@app.route("/download/<filename>", methods=['GET'])
def download_file(filename):
    # 需要知道2个参数, 第1个参数是本地目录的path, 第2个参数是文件名(带扩展名)
    directory = os.getcwd('xml/181015/')  # 假设在当前目录
    return send_from_directory(directory, filename, as_attachment=True)



@app.route("/test",methods=['GET'])
def test():
    return jsonify({'result':'success'})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8383, debug=True)
