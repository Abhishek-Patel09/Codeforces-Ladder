from django.shortcuts import render, redirect
from . utility import CFQuery
from django.http import HttpResponse
#from . forms import IndexForm
from . models import Category, Problem


# Create your views here.
def index(request):
	if(request.method == 'POST'):
		cfHandle = request.POST.get('handle')
		gotoUrl = 'http://127.0.0.1:8000/ladder/'+cfHandle+'/'
		return redirect(gotoUrl)
	else:
		return render(request, 'index.html')


def home(request, cfHandle) :
	cf = CFQuery()
	cf.allProblemStat()
	print('ok')
	solvedProblemsByUser, stats, rating = cf.UserSubmissions(cfHandle=cfHandle)
	print("home : ", stats)
	#print("home : ",accuracystats)
	print("cfHandle : ", cfHandle)

	return render(request, 'home.html', {'cfHandle':cfHandle, 'rating':rating, 'stats':stats,})


def ladder(request, cfHandle, category):
	cf = CFQuery()
	#category_object = Category.objects.get(name=category)
	problems, stats, rating = cf.LadderProblem(cfHandle=cfHandle, category_name=category)
	print(category," : ",problems)

	return render(request, 'ladder.html', {'cfHandle':cfHandle, 'rating':rating, 'category':category, 'problems':problems, 'stats':stats,})
