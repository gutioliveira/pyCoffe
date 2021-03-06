from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from django.template import loader, RequestContext
from .forms import NameForm
import cv2

images_path = '../Desktop/VOCdevkit/VOC2007/JPEGImages'

import os.path

import numpy as np
import matplotlib.pyplot as plt

import urllib
import h5py

import sys
import os

from scipy import misc

labels = []

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
home_dir = os.getenv("HOME")
caffe_root = os.path.join(home_dir, 'caffe')
sys.path.insert(0, os.path.join(caffe_root, 'python'))

import caffe

caffe.set_mode_cpu()

model_def = os.path.join(caffe_root, 'models', 'bvlc_reference_caffenet','deploy.prototxt')
model_weights = os.path.join(caffe_root, 'models','bvlc_reference_caffenet','bvlc_reference_caffenet.caffemodel')

net = caffe.Net(model_def,
                model_weights,
                caffe.TEST)

mu = np.load(os.path.join(caffe_root, 'python','caffe','imagenet','ilsvrc_2012_mean.npy'))
mu = mu.mean(1).mean(1)  # average over pixels to obtain the mean (BGR) pixel values
print 'mean-subtracted values:', zip('BGR', mu)

# create transformer for the input called 'data'
transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})

transformer.set_transpose('data', (2,0,1))
transformer.set_mean('data', mu)
transformer.set_raw_scale('data', 255)
transformer.set_channel_swap('data', (2,1,0))

labels_file = os.path.join(caffe_root, 'data','ilsvrc12','synset_words.txt')
if not os.path.exists(labels_file):
    os.system("~/caffe/data/ilsvrc12/get_ilsvrc_aux.sh")

labels = np.loadtxt(labels_file, str, delimiter='\t')

def predict_imageNet(image_filename):
    image = caffe.io.load_image(image_filename)
    net.blobs['data'].data[...] = transformer.preprocess('data', image)

    net.forward()

    output_prob = net.blobs['prob'].data[0]

    top_inds = output_prob.argsort()[::-1][:5]

    plt.imshow(image)
    plt.axis('off')

    predictions = zip(output_prob[top_inds], labels[top_inds])

    return predictions

def get_image_url(url):
    cap = cv2.VideoCapture(url)
    ret,img = cap.read()

    return img

def index(request):

	template = loader.get_template('prob/index.html')

	context = {
        'latest_question_list': '',
    }

	return render(request,'prob/index.html')

def detail(request):

    my_image_url = request.POST['url']

    try:
        urllib.urlretrieve (my_image_url, PROJECT_ROOT + "/static/img/image.jpg")
        predictions = predict_imageNet('prob/static/img/image.jpg')
    except Exception:
        return image_not_found(request)

    predictions = format(predictions)

    image = get_image_url(my_image_url)
    image_detected = detect(image)

    context = {
        'predictions': predictions,
        'faces': image_detected,
    }

    return render(request,'prob/detail.html', context)

def localImage(request):

    print '$$$$$$$$$$$$$$$$$$$'
    try:
        image = request.FILES['image']
    except Exception:
        return image_not_found(request)

    with open(PROJECT_ROOT + "/static/img/image.jpg", "wb+") as destination:
        for chunk in image.chunks():
            destination.write(chunk)

    try:
        predictions = predict_imageNet('prob/static/img/image.jpg')
    except Exception:
        return image_not_found(request)
    print predictions

    predicitons = format(predictions)

    image = cv2.VideoCapture("prob/static/img/image.jpg")
    ret, img = image.read()

    faces = detect(img)

    context = {
        'predictions': predicitons,
        'faces': faces,
    }



    return render(request,'prob/detail.html', context)

def format(predictions):

    lista = []

    for p in predictions:
        S = []
        aux = 0
        for i in p:
            if aux == 0:
                i = float(i) * 100.0
                i = "{0:.2f}".format(i) + "%"
                S.append(i)
                aux = 1
            else:
                i = i.split(',')

                print i[0].split().pop(0)

                i[0] = i[0].split()

                i[0].pop(0)

                string = ""

                for k in i[0]:
                    string += " " + k

                i[0] = string

                count = 0

                for x in i:
                    i[count] = x.strip()
                    count += 1

                print i

                S.append(i)

        string = str(S[0]) + " "

        for x in S[1]:
            string += str(x) + ", "

        string = string[:-2]

        lista.append(string)

    return lista

def image_not_found(request):
    context = {
        'predictions': "error",
    }
    return render(request,'prob/detail.html', context)

def detect(frame):
    height, width, depth = frame.shape

    # create grayscale version
    grayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
 
    # equalize histogram
    cv2.equalizeHist(grayscale, grayscale)

    # detect objects
    classifier = cv2.CascadeClassifier(caffe_root+"/haarcascade_frontalface_alt.xml")

    # print classifier

    coords = []

    DOWNSCALE = 4
    minisize = (frame.shape[1]/DOWNSCALE,frame.shape[0]/DOWNSCALE)
    miniframe = cv2.resize(frame, minisize)
    faces = classifier.detectMultiScale(miniframe)
    if len(faces)>0:
        for i in faces:
            x, y, w, h = [ v*DOWNSCALE for v in i ]

            coords.append((x,y,w,h))
            print x,y,w,h
            cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0))
    
    cv2.imwrite("prob/static/img/image.jpg", frame)

    return str(len(faces)) + ' face(s) detectadas.'
