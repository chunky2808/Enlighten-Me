from django.shortcuts import render,get_object_or_404
from .models import Forum

def forum_list(request):
	forums = Forum.objects.all()
	# for fori in forums:
	# 	print(fori.name)
	# 	print(fori.desc)
	return render(request,'home.html',{'forums':forums})
