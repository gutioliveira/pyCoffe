from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from django.template import loader, RequestContext
from .forms import NameForm

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

def index(request):

	template = loader.get_template('prob/index.html')

	context = {
        'latest_question_list': '',
    }

	return render(request,'prob/index.html')

def detail(request):

    my_image_url = request.POST['url']

    urllib.urlretrieve (my_image_url, PROJECT_ROOT + "/static/img/image.jpg")

    predictions = predict_imageNet('prob/static/img/image.jpg')

    template = loader.get_template('prob/detail.html')

    context = {
        'predictions': predictions,
    }

    return render(request,'prob/detail.html', context)

def localImage(request):

    print '$$$$$$$$$$$$$$$$$$$'

    image = request.FILES['image']
    with open(PROJECT_ROOT + "/static/img/image.jpg", "wb+") as destination:
        for chunk in image.chunks():
            destination.write(chunk)

    predictions = predict_imageNet('prob/static/img/image.jpg')

    print predictions

    predicitons = format(predictions)

    context = {
        'predictions': predicitons,
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
