# pyCoffe

pyCoffe is a web-app developed with Django-Framework for the purpose of image recognition.

## Dependencies

- [Python language](https://www.python.org/) version 2.7
- [Django Framework](https://www.djangoproject.com) version 1.10.3
- [Caffe library](http://caffe.berkeleyvision.org)

## How to install dependencies

To install Django, just type:
```bash
sudo pip install django
```
To install Caffe, you can check the official [instalation guide](http://caffe.berkeleyvision.org/installation.html)
or if you are using Ubuntu 14.04, check [this](http://sunshineatnoon.github.io/How-to-install-caffe/) amazing tutorial.

## How to use pyCoffe

Clone this repository.

It is necessary to set up where Caffe is installed on your machine, go to pyCoffe/prob/views.py and change this line of code:
```bash
caffe_root = os.path.join(home_dir, 'caffe')
```
Download this [file](https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_alt.xml) and save it on your caffe directory, it is necessary for the face recognition to work.

If your caffe folder is inside your home directory, no reason to change it.

After you set up your caffe path, just type inside pyCoffe folder:

```bash
python manage.py runserver
```
And go to this url on your browser:
```bash
http://localhost:8000/
```
