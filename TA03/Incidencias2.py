import xml.etree.ElementTree as ET

from PIL.ImageOps import contain

tree = ET.parse("TA03.xml")
root = tree.getroot()

root.tag
"row"
root.attrib
{}
cont = 0
for child in root:
    print(child.tag, child.attrib)
    cont =cont +1
print(cont)