import xml.etree.ElementTree as ET
tree = ET.parse("resultado_formateado.xml")
root = tree.getroot()

root.tag
"data"
root.attrib
{}

for child in root:
    print(child.tag, child.attrib)