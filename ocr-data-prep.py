import os
import json
import shutil
import cv2
import random
import re
import glob

# DATA_DIR = './Mansoor_container_numbers/ann'

# filetags = set()
# fileobjects = set()
# vals = 0 
# trains = 0
# tests = 0

# for file in os.listdir(DATA_DIR):
#     with open(os.path.join(DATA_DIR, file), 'r') as openfile:
#         filedata = json.load(openfile)
#         for tag in filedata['tags']:
#             filetags.add(tag)
#             if tag=='train':
#                 trains+=1
#             elif tag=='val':
#                 vals+=1
#             else:
#                 tests+=1
#         print(filedata['tags'])
#         for obj in filedata['objects']:
#             fileobjects.add(obj)

# print(filetags)
# print(fileobjects)
# print(vals)
# print(trains)
# print(tests)

DATA_DIR = './cropped'
CROPPED_DIR = './dataset/'

# make directory for annotations
if not os.path.exists('./dataset/img'):
    os.makedirs(os.path.join(CROPPED_DIR, 'img'))
if not os.path.exists('./dataset/ann'):
    os.makedirs(os.path.join(CROPPED_DIR, 'ann'))

# sort image files in numerical order
filelist = os.listdir(DATA_DIR)
filelist = sorted(filelist,key=lambda x: int(os.path.splitext(x)[0]))
print(filelist)

idx = 0

# ask where to continue from
while True:
    inputval = input('type which file to continue from (complete file name): ')
    if inputval in filelist:
        idx = filelist.index(inputval)
        break
    else:
        print('invalid filename! select again.')

filelist = filelist[idx:]

# iterate over images, take ground truth num input and store annotation
counter = 0
for image in filelist:
    counter+=1
    img = cv2.imread(os.path.join(DATA_DIR, image))
    desc = input('enter plate number for {}'.format(image))
    # check if the image file already exists
    tempimgs = glob.glob('{}/img/*{}*'.format(CROPPED_DIR, desc))
    if len(tempimgs)==0:
        imgname = desc + '-0'
    else:
        templist = []
        for file in tempimgs:
            templist.append(int((file.split('-')[1]).split('.')[0]))
        templist.sort(reverse = True)
        imgname = '{}-{}'.format(desc, str(templist[0]+1))

    shutil.copy(os.path.join(DATA_DIR, image), os.path.join(CROPPED_DIR, 'img/{}.jpg'.format(imgname)))
    height, width, _ = img.shape
    if int(counter/len(os.listdir(DATA_DIR))*100) >= 90:
        tag = 'test'
    elif int(counter/len(os.listdir(DATA_DIR))*100) >= 70 and int(counter/len(os.listdir(DATA_DIR))*100) < 90:
        tag = 'val'
    else:
        tag = 'train'
    annotation = {
        "description": desc,
        "objects": [],
        "size": {
            "height": height,
            "weight": width
        },
        "tags": [tag]
    }
    # check if the csv file aready exists
    tempcsvs = glob.glob('{}/ann/*{}*'.format(CROPPED_DIR, desc))
    if len(tempcsvs)==0:
        csvname = desc + '-0'
    else:
        templist2 = []
        for file in tempcsvs:
            templist2.append(int((file.split('-')[1]).split('.')[0]))
        templist.sort(reverse = True)
        csvname = '{}-{}'.format(desc, str(templist[0]+1))

    with open('{}/ann/{}.json'.format(CROPPED_DIR, csvname), 'w') as outfile:
        json.dump(annotation, outfile)
 


