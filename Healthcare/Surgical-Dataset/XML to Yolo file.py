import xml.etree.ElementTree as ET
from os import getcwd
import os

directory = r"XML_images"
yolo_file = r"yolo_file/yolo_file.txt"

try:
    os.mkdir(os.path.join(directory, "yolo_file"))
except:
    pass

with open(os.path.join(directory, yolo_file), "w") as f:
    pass

def write_one(fullname):
    bb = ""
    in_file = open(fullname)
    tree=ET.parse(in_file)
    root = tree.getroot()
    filename = root.find('filename').text
    for i, obj in enumerate(root.iter('object')):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        cls_id = int(cls)
        xmlbox = obj.find('bndbox')
        b = (int(xmlbox.find('xmin').text), int(xmlbox.find('ymin').text), int(xmlbox.find('xmax').text), int(xmlbox.find('ymax').text))
        bb += (" " + ",".join([str(a) for a in b]) + ',' + str(cls_id))

    print (bb)

    if bb != "":
        list_file = open(os.path.join(directory, yolo_file), 'a')
        file_string = str(fullname)[:-4]+filename[-4:]+bb+'\n'
        list_file.write(file_string)
        list_file.close()


filenames = os.listdir(directory)

for filename in filenames:
    if not filename.endswith('.xml'):
        continue
    fullname = os.path.join(directory, filename)
    print(fullname)
    write_one(fullname)

