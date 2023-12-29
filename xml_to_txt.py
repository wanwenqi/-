# coding: utf-8

import xml.etree.ElementTree as ET
import os

def fun(path):
    fileArray = []
    for root, dirs, files in os.walk(path):
        for fn in files:
            eachpath = str(root+'/'+fn)
            fileArray.append(eachpath)
    return fileArray

names_dict = {}
cnt = 0
f = open('data.names', 'r').readlines()
for line in f:
    line = line.strip()
    names_dict[line] = cnt
    cnt += 1

path = './Ichihara/Annotations'
save_path = ''

def parse_xml(path):
    tree = ET.parse(path)
    img_name = path.split('/')[-1][:-4]

    height = int(tree.findtext("./size/height"))
    width = int(tree.findtext("./size/width"))

    objects = []

    for obj in tree.findall('object'):
        name = obj.find('name').text
        bbox = obj.find('bndbox')
        xmin = int(bbox.find('xmin').text)
        ymin = int(bbox.find('ymin').text)
        xmax = int(bbox.find('xmax').text)
        ymax = int(bbox.find('ymax').text)

        name = str(names_dict[name])
        x_center = (xmin + xmax) / 2 / width
        y_center = (ymin + ymax) / 2 / height
        Width = (xmax - xmin) / width
        Height = (ymax - ymin) / height
        objects.extend([name, x_center, y_center, Width, Height])
    if len(objects) > 1:
        return objects
    else:
        return None

train_cnt = 0
def gen_train_txt(txt_path,path):
    global train_cnt
    #f = open(txt_path, 'w')
    objects = parse_xml(path)
    if objects:
        #objects = ' '.join(objects) + '\n'
        print(objects)
        #f.write(objects)
    #f.close()

def main():
    fileArray = fun(path)
    for i in fileArray:
        gen_train_txt(save_path,i)
        break

if __name__ == '__main__':
    main()