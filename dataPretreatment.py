def data_pretreatment(request):
    title_description = request.json['title_description']
    rolemap = request.json['rolemap']
    dataset = request.json['dataset']
    sqlQuery = request.json['sqlQuery']
    report_parameters = request.json['report_parameters']

    title_description = title_data(title_description)
    rolemap = role_data(rolemap)
    dataset = dataset_data(dataset)


    print(title_description)
    print(rolemap)
    print(dataset)
    print(sqlQuery)
    print(report_parameters)


def title_data(title_description):
    title_description_list = []
    title_description_list.append(title_description['id'])
    title_description_list.append(title_description['title'])
    title_description_list.append(title_description['description'])
    return title_description_list


def role_data(rolemap):
    role_all = {'OPERATOR_ADMIN': '运营管理员', 'MSL_LEADER': '省总'}
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
            dataset = []
            dataset.append(dataset_json['id'])
            dataset.append(dataset_json['source'])
            dataset.append(dataset_json['label'])
            parameters = []
            for parameter_json in dataset_json['parameter']:
                if parameter_json:
                    parameter = [parameter_json['name'], parameter_json['name'], parameter_json['default_value']]
                    parameters.append(parameter)

            columns = []
            for columns_json in dataset_json['columns']:
                if columns_json:
                    column = [columns_json['name'], columns_json['label'], columns_json['datatype']]
                    columns.append(column)
            dataset.append(parameters)
            dataset.append(columns)

            datasets.append(dataset)
    return datasets



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
