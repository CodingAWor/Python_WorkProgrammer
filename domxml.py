import xml.etree.ElementTree as ET
tree = ET.parse('demo.xml')
root = tree.getroot()
# tag 节点表示
# attrib 对应全属性
print(root.tag)
print(root.attrib)
for moudle in root.iter('Moudle'):
    print(moudle.attrib)
    for node in moudle.findall('Library'):
        print(node.tag)
        print(node.attrib)
        print(node.text)
        print(node.get('name'))

# 创建新的book节点
new_book = ET.Element('book', {'category': 'MYSTERY'})
ET.SubElement(new_book, 'title', {'lang': 'en'}).text = 'The Da Vinci Code'
ET.SubElement(new_book, 'author').text = 'Dan Brown'
ET.SubElement(new_book, 'year').text = '2003'
ET.SubElement(new_book, 'price').text = '15.50'

# 将新节点添加到树中
root.insert(0, ET.Element('\n'))
root.insert(0, new_book)
root.insert(0, ET.Element('\n'))
tree.write('demo.xml')
