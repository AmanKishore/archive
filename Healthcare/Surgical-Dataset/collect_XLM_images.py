from textwrap import dedent
from lxml import etree
import glob
import os
import cv2
import time
import matplotlib.pyplot as plt
import numpy as np

# input is result of cv.imread(image)

def CreateXMLfile(image, ObjectsList, filename):
    Folder_to_save = "XML_images"
    os.chdir(Folder_to_save)
    image_num = len(glob.glob("*.jpg"))
    print("Number of .jpg files =", image_num)

    img_name = filename[:-4]+".jpg"
    
    cv2.imwrite(img_name,image)

    annotation = etree.Element("annotation")

    folder = etree.Element("folder")
    folder.text = os.path.basename(os.getcwd())
    annotation.append(folder)

    filename_xml = etree.Element("filename")
    filename_str = img_name
    filename_xml.text = img_name
    annotation.append(filename_xml)

    path = etree.Element("path")
    path.text = os.path.join(os.path.basename(os.getcwd()), filename_str)
    annotation.append(path)

    source = etree.Element("source")
    annotation.append(source)

    database = etree.Element("database")
    database.text = "Unknown"
    source.append(database)

    size = etree.Element("size")
    annotation.append(size)

    width = etree.Element("width")
    height = etree.Element("height")
    depth = etree.Element("depth")

    img = cv2.imread(filename_xml.text)

    width.text = str(img.shape[1])
    height.text = str(img.shape[0])
    depth.text = str(img.shape[2])

    size.append(width)
    size.append(height)
    size.append(depth)

    segmented = etree.Element("segmented")
    segmented.text = "0"
    annotation.append(segmented)

    for Object in ObjectsList:
        class_name = int(Object[0]) + 1
        xmin_l = str(int(float(Object[1])))
        ymin_l = str(int(float(Object[2])))
        xmax_l = str(int(float(Object[3])))
        ymax_l = str(int(float(Object[4])))

        obj = etree.Element("object")
        annotation.append(obj)

        name = etree.Element("name")
        name.text = str(class_name)
        obj.append(name)

        pose = etree.Element("pose")
        pose.text = "Unspecified"
        obj.append(pose)

        truncated = etree.Element("truncated")
        truncated.text = "0"
        obj.append(truncated)

        difficult = etree.Element("difficult")
        difficult.text = "0"
        obj.append(difficult)

        bndbox = etree.Element("bndbox")
        obj.append(bndbox)

        xmin = etree.Element("xmin")
        xmin.text = xmin_l
        bndbox.append(xmin)

        ymin = etree.Element("ymin")
        ymin.text = ymin_l
        bndbox.append(ymin)

        xmax = etree.Element("xmax")
        xmax.text = xmax_l
        bndbox.append(xmax)

        ymax = etree.Element("ymax")
        ymax.text = ymax_l
        bndbox.append(ymax)

    # write xml to file
    s = etree.tostring(annotation, pretty_print=True)
    with open(filename[:-4] + ".xml", 'wb') as f:
        f.write(s)
        f.close()

    os.chdir("..")
    #time.sleep(1)

def get_object_list(label_path):
    label = np.loadtxt(label_path)
    if label.ndim < 2:
        label = label.reshape((1,label.shape[0]))
    print(label)
    
    obj_list = np.empty(label.shape)
    
    for i, obj in enumerate(label):
        for j, value in enumerate(obj):
            if j == 0: #class name
                obj_list[i][j] = value
            if j == 1: #xmin
                obj_list[i][j] = (obj[1]-obj[3]/2)*resolution[0]
            if j == 2: #ymin
                obj_list[i][j] = (obj[2]-obj[4]/2)*resolution[1]
            if j == 3: #xmax
                obj_list[i][j] = (obj[1]+obj[3]/2)*resolution[0]
            if j == 4: #ymax
                obj_list[i][j] = (obj[2]+obj[4]/2)*resolution[1]
                
    print(obj_list)

    return list(obj_list)


directory = r"Images/All/images"
filenames = os.listdir(directory)
label_directory = r"Labels/label object names"
label_filenames = os.listdir(label_directory)

resolution = (640, 480)

try:
    os.mkdir("XML_images")
except:
    pass

for i, (filename, label_filename) in enumerate(zip(filenames, label_filenames)):
    print (filename)
    print(label_filename)
    
    image_path = os.path.join(directory, filename)
    image = cv2.imread(image_path)

    label_path = os.path.join(label_directory, label_filename)
    object_list = get_object_list(label_path)

    CreateXMLfile(image, object_list, filename)



    

    






