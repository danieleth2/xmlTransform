# -*- coding: utf-8 -*-
from flask import Flask, abort, request, jsonify
from dataPretreatment import *
from createReportXml import create_report_xml, create_files
from createDataset import *
from flask import send_file, send_from_directory
import os
from flask_cors import *

app = Flask(__name__)
CORS(app, supports_credentials=True)


@app.route('/create', methods=['POST'])
def add_task():
    title_description, rolemap, dataset, sqlQuery, report_parameter = data_pretreatment(request)
    xml = create_report_xml(title_description, rolemap, dataset, sqlQuery, report_parameter)
    file_name = title_description[0]
    create_files(xml, file_name)
    return jsonify({'result': '创建报表srdl成功，文件名为' + file_name + '.srdl'})


@app.route('/dataset', methods=['POST'])
def add_dataset():
    dataset, sqlQuery = dataset_pretreatment(request)
    xml = create_dataset(dataset, sqlQuery)
    file_name = dataset[0]
    create_dataset_file(xml, file_name)
    return jsonify({'result': '创建dataset成功，文件名为' + file_name + '.dataset'})


@app.route("/test", methods=['GET'])
def test():
    return jsonify({'result': 'success'})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8383, debug=True)
