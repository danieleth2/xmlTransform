# coding:utf-8
from xml.dom import minidom
import json
from collections import OrderedDict


# 写入xml文档的方法
def create_xml_test(filename):
    # 输入参数
    report_id = filename
    title = '医院信息列表'
    # rolemap ={}

    rolemap = {'运营管理员': 'OPERATOR_ADMIN', '省总': 'MSL_LEADER'}

    description = '医院获取详细列表'

    dataset = [
        ["1", 'NATIVE', '医院列表数据', [['regionCode', 'STRING', "100000"], ['limit', 'INTEGER', "10"]],
         [['name', '医院名称', 'STRING'], ['province', '省', 'STRING']]],
        ["2", 'KYLIN', '医院列表数据2', [], []]]

    sqlQuery=["", ""]

    # 新建xml文档对象
    xml = minidom.Document()

    # 创建第一个节点，第一个节点就是根节点了
    report = xml.createElement('report')

    # 写入属性（xmlns:xsi是命名空间，同样还可以写入xsi:schemaLocation指定xsd文件）
    report.setAttribute('xmlns:xsi', "http://www.w3.org/2001/XMLSchema-instance")
    report.setAttribute('xsi:noNamespaceSchemaLocation', "http://www.sap.com/sme/occ/schema/report.xsd")
    report.setAttribute('namespace', "com.dzj")
    report.setAttribute('id', report_id)
    report.setAttribute('revision', "1")
    report.setAttribute('height', "2")
    xml.appendChild(report)

    # 报表标题
    title_node = xml.createElement('title')
    title_node.setAttribute('isExpression', 'false')
    report.appendChild(title_node)
    title_text = xml.createTextNode(title)
    title_node.appendChild(title_text)

    # 报表权限控制
    if rolemap:
        roles_node = xml.createElement('roles')
        report.appendChild(roles_node)
        for key in rolemap:
            role_node = xml.createElement('role')
            role_node.setAttribute('name', key)
            role_node.setAttribute('value', rolemap[key])
            roles_node.appendChild(role_node)

    # 报表描述
    description_node = xml.createElement('description')
    report.appendChild(description_node)
    description = xml.createTextNode(description)
    description_node.appendChild(description)

    # 报表datasets
    datasets_node = xml.createElement('datasets')
    report.appendChild(datasets_node)

    for datasetValue in dataset:
        dataset_node = xml.createElement('dataset')
        datasets_node.appendChild(dataset_node)

        dataset_node.setAttribute('id', datasetValue[0])
        dataset_node.setAttribute('data-source-type', datasetValue[1])

        # label数据
        label_node = xml.createElement('label')
        dataset_node.appendChild(label_node)
        label_node.setAttribute('isExpression', 'false')
        label_text = xml.createTextNode(datasetValue[2])
        label_node.appendChild(label_text)

        # dataset输入参数数组
        parameters_node = xml.createElement('parameters')
        dataset_node.appendChild(parameters_node)

        # dataset输出参数数组
        columns_node = xml.createElement('columns')
        dataset_node.appendChild(columns_node)

        for parametersValue in datasetValue[3]:
            if parametersValue:
                # 输入参数
                parameter_node = xml.createElement('parameter')
                parameters_node.appendChild(parameter_node)
                parameter_node.setAttribute('name', parametersValue[0])
                # 数据类型
                p_data_type_node = xml.createElement('data-type')
                parameter_node.appendChild(p_data_type_node)
                p_data_type_text = xml.createTextNode(parametersValue[1])
                p_data_type_node.appendChild(p_data_type_text)
                # 默认值
                p_default_value_node = xml.createElement('default-value')
                parameter_node.appendChild(p_default_value_node)
                p_default_value_text = xml.createTextNode(parametersValue[2])
                p_default_value_node.appendChild(p_default_value_text)

        for columnsValue in datasetValue[4]:
            if columnsValue:
                column_node = xml.createElement('column')
                columns_node.appendChild(column_node)
                column_node.setAttribute('name', columnsValue[0])

                c_data_type_node = xml.createElement('data-type')
                column_node.appendChild(c_data_type_node)
                c_data_type_text = xml.createTextNode(columnsValue[1])
                c_data_type_node.appendChild(c_data_type_text)


                c_label_node = xml.createElement('label')
                column_node.appendChild(c_label_node)
                c_label_text = xml.createTextNode(columnsValue[2])
                c_label_node.appendChild(c_label_text)






    # 写好之后，就需要保存文档了
    f = open(filename + '.srdl', 'wb')
    f.write(xml.toprettyxml(encoding='utf-8'))
    f.close()


if __name__ == '__main__':
    # 在当前目录下，创建1.xml
    create_xml_test('ok_hospital_info_list')
