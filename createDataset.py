from xml.dom import minidom
import datetime
import os


def create_dataset(datasetValue, sqlQuery):
    xml = minidom.Document()

    datasets = xml.createElement('datasets')
    datasets.setAttribute('xmlns:xsi', "http://www.w3.org/2001/XMLSchema-instance")
    datasets.setAttribute('xsi:noNamespaceSchemaLocation', "http://www.sap.com/sme/occ/schema/report.xsd")
    datasets.setAttribute('namespace', "com.dzj")
    xml.appendChild(datasets)

    dataset_node = xml.createElement('dataset')
    datasets.appendChild(dataset_node)
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
            # 输出参数
            column_node = xml.createElement('column')
            columns_node.appendChild(column_node)
            column_node.setAttribute('name', columnsValue[0])
            # 数据类型
            c_data_type_node = xml.createElement('data-type')
            column_node.appendChild(c_data_type_node)
            c_data_type_text = xml.createTextNode(columnsValue[1])
            c_data_type_node.appendChild(c_data_type_text)
            # label标签
            c_label_node = xml.createElement('label')
            column_node.appendChild(c_label_node)
            c_label_text = xml.createTextNode(columnsValue[2])
            c_label_node.appendChild(c_label_text)

    # sql
    query_node = xml.createElement('query')
    dataset_node.appendChild(query_node)

    query_text_node = xml.createElement('text')
    query_node.appendChild(query_text_node)
    if sqlQuery:
        query_text = xml.createCDATASection(sqlQuery)
        query_text_node.appendChild(query_text)

    return xml


def create_dataset_file(xml, file_name):
    today = datetime.date.today()
    formatted_today = 'dataset/' + today.strftime('%y%m%d')

    if not os.path.exists('DirectoryLister/' + formatted_today):
        os.makedirs('DirectoryLister/' + formatted_today)

    f = open('DirectoryLister/' + formatted_today + '/' + file_name + '.dataset', 'wb')
    f.write(xml.toprettyxml(encoding='utf-8'))
    f.close()
