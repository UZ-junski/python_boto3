from PIL import Image
import boto3
import time
import os
import json

base = os.getcwd()
manPhotoDir = os.path.join(base,'ver_3')
#photo = '3.png'
region='eu-west-1'

#with open(photo, 'rb') as source_image:
#    source_bytes = source_image.read()
xVectors = [-50, 0, 50]
yVectors = [100, 150, 200, 250, 300]
savedPhotos = [1, 2, 3, 4, 5, 6]
photosType = ['FrontOff1', 'FrontOff2', 'FrontOn1', 'FrontOn2', 'Back1', 'Back2']
fileNames =list()
print('geting paths of files')
for y in yVectors:
    for x in xVectors:
        for photoNo in savedPhotos:
            fileNames.append(os.path.join(os.path.join(manPhotoDir, str(y) + '_' + str(x) ), str(photoNo) +'.bmp'))
resultDictionary = dict.fromkeys(fileNames , '')
formatTimes = list()
print('convert bmps to png')
for fName in fileNames:
    start_time = time.time()
    Image.open(fName).save(fName.replace('.bmp', '.png'))
    resultDictionary[fName]=str((time.time() - start_time)*1000)
#    formatTimes.append()
#print("Times for coverting files")
#print(', '.join(str(x) for x in formatTimes))
print('sending requests')
client = boto3.client('rekognition')
for fName in fileNames:
    with open(fName.replace('.bmp', '.png'), 'rb') as source_image:
        source_bytes = source_image.read()
    start_time = time.time()
    response = client.detect_labels(Image={'Bytes': source_bytes}, MaxLabels = 3)
    resultDictionary[fName]+=';'+str((time.time() - start_time)*1000)+os.linesep+json.dumps(response)
print('saving responses')
a_file = open('results.json', 'w')
json.dump(resultDictionary, a_file)
a_file.close()

