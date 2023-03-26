import xml.etree.ElementTree as ET


def get_module_properties(file_path, module_name='all'):
    """
    获取指定 module_name 下的所有属性

    :param file_path: XML 文件路径
    :type file_path: str

    :param module_name: 要查询的 Moudle name
    :type module_name: str

    :return: 指定 module_name 下的所有属性
    :rtype: dict
    """
    # 加载 XML 文件
    tree = ET.parse(file_path)
    root = tree.getroot()

    # 用于存储查询结果的字典
    properties = {}

    # 遍历所有 Moudle 元素
    for modules in root.findall('Moudle') or root.findall('Enviorment'):
        # 判断 Moudle name 是否与指定名称相同
        if module_name == 'all' or modules.attrib['name'] == module_name:
            # 遍历当前 Moudle 下的所有 Library 元素
            for module in modules:
                # 将当前 module 元素的所有属性添加到字典中
                properties[module.attrib['name']] = {
                    'target': module.attrib['target'],
                    'mkcmd': module.attrib['mkcmd'],
                    'url': module.attrib['url'],
                    'reversion': module.attrib['reversion']
                }

    return properties


def insert_node_and_attrs(file_path, node_name, attrs):
    """
    将指定节点和其属性插入到 XML 文件的开头

    :param file_path: XML 文件路径
    :type file_path: str

    :param node_name: 要插入的节点名
    :type node_name: str

    :param attrs: 要插入的属性字典
    :type attrs: dict
    """
    # 加载 XML 文件
    tree = ET.parse(file_path)
    root = tree.getroot()

    # 创建要插入的节点并添加属性
    new_node = ET.Element(node_name)
    for attr_name, attr_value in attrs.items():
        new_node.set(attr_name, attr_value)

    new_node.tail = '\n    '
    # 将新节点添加到根元素的开头
    root.insert(0, new_node)

    # 保存修改后的 XML 文件
    tree.write(file_path, encoding='utf-8', xml_declaration=True)


def add_diff_node(file_path, module_name, diff_attrs):
    """
    在指定 module name 节点下新增子节点 Diff，并添加指定属性

    :param module_name: 指定的 module name
    :type module_name: str

    :param diff_attrs: 新增 Diff 节点的属性
    :type diff_attrs: dict

    :param root: XML 文件的根节点
    :type root: Element
    """
    # 加载 XML 文件
    tree = ET.parse(file_path)
    root = tree.getroot()
    print("-----")
    print(module_name)

    # 找到所有满足 module name 的节点
    target_nodes = [node for node in root.iter(
    ) if node.attrib.get('name', '') == module_name]

    # 在每个目标节点下插入新节点
    for target_node in target_nodes:
        new_node = ET.Element('Diff', attrib=diff_attrs)
        new_node.tail = '\n        '
        target_node.insert(0, new_node)

    # 保存修改后的 XML 文件
    tree.write(file_path, encoding='utf-8', xml_declaration=True)


def update_submodule(file_path, module_name, url, revision):
    """
    修改指定 module name 节点的 submodule URL 和 revision 属性

    :param module_name: 指定的 module name
    :type module_name: str

    :param url: 新的 submodule URL
    :type url: str

    :param revision: 新的 submodule revision
    :type revision: str

    :param root: XML 文件的根节点
    :type root: Element
    """

    tree = ET.parse(file_path)
    root = tree.getroot()

    # 找到目标节点
    # 找到目标节点
    target_nodes = [node for node in root.iter(
    ) if node.attrib.get('name', '') == module_name]

    # 更新属性
    for target_node in target_nodes:
        target_node.set('url', url)
        target_node.set('revision', revision)

    # 保存修改后的 XML 文件
    tree.write(file_path, encoding='utf-8', xml_declaration=True)


def get_library_properties(file_path, library_name='all'):
    """
    获取指定 library_name 下的所有属性

    :param file_path: XML 文件路径
    :type file_path: str

    :param module_name: 要查询的 Moudle name
    :type module_name: str

    :return: 指定 module_name 下的所有属性
    :rtype: dict
    """
    # 加载 XML 文件
    tree = ET.parse(file_path)
    root = tree.getroot()

    # 用于存储查询结果的字典
    properties = {}

    # 遍历所有 Moudle 元素
    for module in root.findall('Moudle') or root.findall('Enviorment'):
        # 遍历当前 Moudle 下的所有 Library 元素
        for library in module.findall('Library'):
            # 将当前 Library 元素的所有属性添加到字典中
            print(library)
            if library.attrib['name'] == library_name:
                print('123456')
                properties[library.attrib['name']] = {
                    'target': library.attrib['target'],
                    'mkcmd': library.attrib['mkcmd'],
                    'url': library.attrib['url'],
                    'reversion': library.attrib['reversion']
                }

    return properties


def main():
    # 设定要查询的 XML 文件路径和 Moudle name
    file_path = 'demo.xml'
    module_name = 'ptz'

    # 获取指定 Moudle 下的所有属性
    properties = get_module_properties(file_path)

    properties2 = get_library_properties(file_path, 'libPtz.a')

    # 打印查询结果
    print(f"{module_name} module properties:")
    for key, value in properties2.items():
        print(f"{key}: {value}")

    key = list(properties2)
    print(key)
    print(properties2['libPtz.a'].get('url'))

    # insert_node_and_attrs('demo.xml', 'new_node', {'attr1': 'value1', 'attr2': 'value2'})

    # add_diff_node(module_name, {'attr1': 'value1','attr2': 'value2'}, )

    update_submodule('demo.xml', 'Function',
                     'https://new-url.com/submodule', '123456')


if __name__ == '__main__':
    main()
