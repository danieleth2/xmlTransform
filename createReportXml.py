# -*- coding: utf-8 -*-
from xml.dom import minidom
import datetime
import os


# 写入xml文档
def create_report_xml(title_description, rolemap, dataset, sqlQuery, report_parameters):
    # 新建xml文档对象
    xml = minidom.Document()

    # 创建第一个节点，第一个节点就是根节点了
    report = xml.createElement('report')

    # 写入属性（xmlns:xsi是命名空间，同样还可以写入xsi:schemaLocation指定xsd文件）
    report.setAttribute('xmlns:xsi', "http://www.w3.org/2001/XMLSchema-instance")
    report.setAttribute('xsi:noNamespaceSchemaLocation', "http://www.sap.com/sme/occ/schema/report.xsd")
    report.setAttribute('namespace', "com.dzj")
    report.setAttribute('id', title_description[0])
    report.setAttribute('revision', "1")
    report.setAttribute('height', "2")
    xml.appendChild(report)

    # 报表标题
    title_node = xml.createElement('title')
    title_node.setAttribute('isExpression', 'false')
    report.appendChild(title_node)
    title_text = xml.createTextNode(title_description[1])
    title_node.appendChild(title_text)

    # 报表权限控制
    if rolemap:
        roles_node = xml.createElement('roles')
        report.appendChild(roles_node)
        for key in rolemap:
            role_node = xml.createElement('role')
            role_node.setAttribute('name', key[0])
            role_node.setAttribute('value', key[1])
            roles_node.appendChild(role_node)

    # 报表描述
    description_node = xml.createElement('description')
    report.appendChild(description_node)
    description = xml.createTextNode(title_description[2])
    description_node.appendChild(description)

    # 报表datasets
    datasets_node = xml.createElement('datasets')
    report.appendChild(datasets_node)
    # 获取单个dataset数值
    for idx, datasetValue in enumerate(dataset):
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

        query_text = xml.createCDATASection(sqlQuery[idx])
        query_text_node.appendChild(query_text)

    # 释放到前端的参数
    report_parameters_node = xml.createElement('report-parameters')
    report.appendChild(report_parameters_node)
    for idx, report_parameter in enumerate(report_parameters):
        if report_parameter:
            # report-parameter
            report_parameter_node = xml.createElement('report-parameter')
            report_parameter_node.setAttribute('name', report_parameter[0])
            report_parameter_node.setAttribute('isVisible', report_parameter[1])
            report_parameters_node.appendChild(report_parameter_node)

            # label标签
            r_label_node = xml.createElement('label')
            r_label_node.setAttribute('isExpression', report_parameter[2])
            report_parameter_node.appendChild(r_label_node)
            r_label_text = xml.createTextNode(report_parameter[3])
            r_label_node.appendChild(r_label_text)

            # 默认值
            r_data_type_node = xml.createElement('data-type')
            report_parameter_node.appendChild(r_data_type_node)
            r_data_type_text = xml.createTextNode(report_parameter[4])
            r_data_type_node.appendChild(r_data_type_text)

            # 默认值
            r_default_value_node = xml.createElement('default-value')
            report_parameter_node.appendChild(r_default_value_node)
            r_default_value_text = xml.createTextNode(report_parameter[5])
            r_default_value_node.appendChild(r_default_value_text)

            targe_bindings_node = xml.createElement('target-bindings')
            report_parameter_node.appendChild(targe_bindings_node)

            # 绑定dataset 指定该参数的作用范围,映射到某个数据集的某些字段
            for bindings in report_parameter[6]:
                if bindings:
                    target_binding = xml.createElement('target-binding')
                    target_binding.setAttribute('id', bindings[0])
                    target_binding.setAttribute('parameterName', bindings[1])
                    targe_bindings_node.appendChild(target_binding)

    # sheet 图标  暂时只支持table
    sheet_node = xml.createElement('sheet')
    sheet_node.setAttribute('widget', 'table')
    report.appendChild(sheet_node)

    for idx, tableValue in enumerate(dataset):
        table_node = xml.createElement('table')
        sheet_node.appendChild(table_node)
        # table绑定的dataset
        declare_binding = xml.createElement('declare-binding')
        declare_binding.setAttribute('datasetid', tableValue[0])
        table_node.appendChild(declare_binding)

        # cloumns 所有的列
        s_columns_node = xml.createElement('columns')
        table_node.appendChild(s_columns_node)

        for column in tableValue[4]:
            s_column_node = xml.createElement('column')
            s_columns_node.appendChild(s_column_node)

            sc_label_node = xml.createElement('label')
            s_column_node.appendChild(sc_label_node)
            sc_label_text = xml.createTextNode(column[1])
            sc_label_node.appendChild(sc_label_text)

            dataset_column_name_node = xml.createElement('dataset-column-name')
            s_column_node.appendChild(dataset_column_name_node)
            dataset_column_name_text = xml.createTextNode(column[0])
            dataset_column_name_node.appendChild(dataset_column_name_text)
    return xml


# 生成文件
def create_files(xml, file_name):
    today = datetime.date.today()
    formatted_today = today.strftime('%y%m%d')

    if not os.path.exists('DirectoryLister/' + formatted_today):
        os.makedirs('DirectoryLister/' + formatted_today)

    f = open('DirectoryLister/' + formatted_today + '/' + file_name + '.srdl', 'wb')
    f.write(xml.toprettyxml(encoding='utf-8'))
    f.close()
