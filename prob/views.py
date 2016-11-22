from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from django.template import loader, RequestContext
from .forms import NameForm

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
	
	print(request.POST)

	template = loader.get_template('prob/detail.html')

	context = {
        'latest_question_list': '',
    }

	return HttpResponse("template.render(request)")

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