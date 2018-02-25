from django.shortcuts import render,get_object_or_404
from .models import Forum,Topic

def forum_list(request):
	forums = Forum.objects.all()
	# for fori in forums:
	# 	print(fori.name)
	# 	print(fori.desc)
	return render(request,'home.html',{'forums':forums})

def topic_list(request, pk):
	topics = Topic.objects.all()
	#topics = Topic.objects.get(pk=pk)
	print(topics)
	return render(request,'topics.html',{'topics' : topics})

