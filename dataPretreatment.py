# -*- coding: utf-8 -*-
def data_pretreatment(request):
    title_description = request.json['title_description']
    rolemap = request.json['rolemap']
    dataset = request.json['dataset']
    sqlQuery = request.json['sqlQuery']
    report_parameter = request.json['report_parameter']

    title_description = title_data(title_description)
    rolemap = role_data(rolemap)
    dataset = dataset_data(dataset)

    report_parameter = parametes_data(report_parameter)

    return title_description, rolemap, dataset, sqlQuery, report_parameter


def title_data(title_description):
    title_description_list = [title_description['id'], title_description['title'], title_description['description']]
    return title_description_list


def role_data(rolemap):
    role_all = {'OPERATOR_ADMIN': '运营管理员', 'MSL_LEADER': '省总', 'OPERATOR': '运营人员', 'ALL': '所有人',
                'ENTERPRISE_OPERATOR': '企业管理员', 'DOCTOR': '医生', 'MSL': '联络员'}
    role_all_list = []
    for role in rolemap:
        if role:
            role_name = role_all[role]
            role_list = [role_name, role]
            role_all_list.append(role_list)
    return role_all_list


def dataset_data(dataset):
    datasets = []
    for dataset_json in dataset:
        if dataset_json:

            parameters = []
            for parameter_json in dataset_json['parameter']:
                if parameter_json:
                    parameter = [parameter_json['name'], parameter_json['datatype'], parameter_json['default_value']]
                    parameters.append(parameter)

            columns = []
            for columns_json in dataset_json['columns']:
                if columns_json:
                    column = [columns_json['name'], columns_json['datatype'], columns_json['label']]
                    columns.append(column)

            dataset_list = [dataset_json['id'], dataset_json['source'], dataset_json['label'], parameters, columns]
            datasets.append(dataset_list)
    return datasets


def parametes_data(report_parameter):
    report_parameters = []
    for report_parameter_json in report_parameter:
        if report_parameter_json:
            bindings = []
            for binding_json in report_parameter_json['binding']:
                if binding_json:
                    binding = [binding_json['id'], binding_json['parameterName']]
                    bindings.append(binding)
            report_parameter_list = [report_parameter_json['name'], report_parameter_json['isVisible'],
                                     report_parameter_json['isExpression'], report_parameter_json['label'],
                                     report_parameter_json['data_type'], report_parameter_json['default_value'],
                                     bindings]
            report_parameters.append(report_parameter_list)
    return report_parameters


def dataset_pretreatment(request):
    dataset_json = request.json['dataset']

    if dataset_json:

        parameters = []
        for parameter_json in dataset_json['parameter']:
            if parameter_json:
                parameter = [parameter_json['name'], parameter_json['datatype'], parameter_json['default_value']]
                parameters.append(parameter)

        columns = []
        for columns_json in dataset_json['columns']:
            if columns_json:
                column = [columns_json['name'], columns_json['datatype'], columns_json['label']]
                columns.append(column)

        dataset = [dataset_json['id'], dataset_json['source'], dataset_json['label'], parameters, columns]

    sqlQuery = request.json['sqlQuery']

    return dataset, sqlQuery

# title_description = ['ok_hospital_info_list', '医院信息列表', '医院获取详细列表']
#
# rolemap = [['运营管理员', 'OPERATOR_ADMIN'], ['省总', 'MSL_LEADER']]
#
# # 1.dataset 的id  2.数据来源  3.label标签名称
# # 4.parameter 数组 其中每个都有 name datatype default value
# # 5.columns 数组  其中每个都有 name label datatype
# dataset = [["1", 'NATIVE', '医院列表数据', [['regionCode', 'STRING', "100000"], ['limit', 'INTEGER', "10"]],
#          [['name', '医院名称', 'STRING'], ['province', '省', 'STRING']]]
#        ]
#
# sqlQuery = ['select * from b_hospital']
#
# # 释放到前端的参数
# report_parameters = [['regionCode', 'true', 'false', '区域代码', 'STRING', '100000', [['1', 'regionCode']]]]
