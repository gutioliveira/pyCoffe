from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from django.template import loader, RequestContext
from .forms import NameForm

images_path = '../Desktop/VOCdevkit/VOC2007/JPEGImages'

import numpy as np
import matplotlib.pyplot as plt

import urllib 
import h5py # to save/load data files

import sys
import os

from scipy import misc # To load/save images without Caffe

labels = [] # Initialising labels as an empty array.

home_dir = os.getenv("HOME")
caffe_root = os.path.join(home_dir, 'caffe')  # this file should be run from {caffe_root}/examples (otherwise change this line)
sys.path.insert(0, os.path.join(caffe_root, 'python'))

import caffe

caffe.set_mode_cpu()

model_def = os.path.join(caffe_root, 'models', 'bvlc_reference_caffenet','deploy.prototxt')
model_weights = os.path.join(caffe_root, 'models','bvlc_reference_caffenet','bvlc_reference_caffenet.caffemodel')

net = caffe.Net(model_def,      # defines the structure of the model
                model_weights,  # contains the trained weights
                caffe.TEST)

mu = np.load(os.path.join(caffe_root, 'python','caffe','imagenet','ilsvrc_2012_mean.npy'))
mu = mu.mean(1).mean(1)  # average over pixels to obtain the mean (BGR) pixel values
print 'mean-subtracted values:', zip('BGR', mu)

# create transformer for the input called 'data'
transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})

transformer.set_transpose('data', (2,0,1))  # move image channels to outermost dimension
transformer.set_mean('data', mu)            # subtract the dataset-mean value in each channel
transformer.set_raw_scale('data', 255)      # rescale from [0, 1] to [0, 255]
transformer.set_channel_swap('data', (2,1,0))  # swap channels from RGB to BGR


# In[ ]:

# load ImageNet labels
labels_file = os.path.join(caffe_root, 'data','ilsvrc12','synset_words.txt')
if not os.path.exists(labels_file):
    os.system("~/caffe/data/ilsvrc12/get_ilsvrc_aux.sh")
    
labels = np.loadtxt(labels_file, str, delimiter='\t')

def predict_imageNet(image_filename):
    image = caffe.io.load_image(image_filename)
    net.blobs['data'].data[...] = transformer.preprocess('data', image)

    # perform classification
    net.forward()

    # obtain the output probabilities
    output_prob = net.blobs['prob'].data[0]

    # sort top five predictions from softmax output
    top_inds = output_prob.argsort()[::-1][:5]

    plt.imshow(image)
    plt.axis('off')

    print 'probabilities and labels:'
    predictions = zip(output_prob[top_inds], labels[top_inds]) # showing only labels (skipping the index)

    string = ""

    for p in predictions:
        string += str(p) + "</br>"
    
    # plt.figure(figsize=(15, 3))
    # plt.plot(output_prob)

    print '#######################'
    print string
    print '#######################'
    return string

def index(request):

	template = loader.get_template('prob/index.html')

	context = {
        'latest_question_list': '',
    }
	
	# c = {csrf(request)}
	# return render_to_response('my_template.html', c)
	# return render_to_response(template, RequestContext(request))
	return render(request,'prob/index.html')
    
	# return HttpResponse("Hello, world. You're at the polls index.")

def detail(request):

	# return HttpResponse("nois")

	# return True

	# my_image_url = "http://cdn1-www.dogtime.com/assets/uploads/gallery/german-shepherd-dog-breed-pictures/happysitting-8.jpg"

	# if request.method == 'POST':
		# pass
#         # create a form instance and populate it with data from the request:
		# form = NameForm(request.POST)
#         # check whether it's valid:
    	# if form.is_valid():
#             # process the data in form.cleaned_data as required
#             # ...
#             # redirect to a new URL:
			# return HttpResponseRedirect('/thanks/')
	
	my_image_url = request.POST['url']

	urllib.urlretrieve (my_image_url, "image.jpg")

	string = predict_imageNet('image.jpg')

	template = loader.get_template('prob/detail.html')

	context = {
        'latest_question_list': '',
    }

	return HttpResponse(string)

# def get_name(request):
#     # if this is a POST request we need to process the form data
#     if request.method == 'POST':
#         # create a form instance and populate it with data from the request:
#         form = NameForm(request.POST)
#         # check whether it's valid:
#         if form.is_valid():
#             # process the data in form.cleaned_data as required
#             # ...
#             # redirect to a new URL:
#             return HttpResponseRedirect('/thanks/')

#     # if a GET (or any other method) we'll create a blank form
#     else:
#         form = NameForm()

#     return render(request, 'name.html', {'form': form})