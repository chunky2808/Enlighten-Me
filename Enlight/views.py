from django.contrib.auth.models import User
from django.shortcuts import render,get_object_or_404,redirect
from .models import Forum,Topic,Post
from .forms import NewTopicForm

def forum_list(request):
	forums = Forum.objects.all()
	# for fori in forums:
	# 	print(fori.name)
	# 	print(fori.desc)
	return render(request,'home.html',{'forums':forums})

def topic_list(request, pk):
	forums = get_object_or_404(Forum,pk=pk)
	topics = forums.topics.all()
	print(topics)
	print(forums)
	return render(request,'topics.html',{'topics' : topics,'forums' : forums})

def new_topic(request, pk):
    forum = get_object_or_404(Forum, pk=pk)
    user = User.objects.first()
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.forum= forum
            topic.started_by = user
            topic.save()
            post = Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=user
            )
            return redirect('topic', pk=forum.pk)
    else:
        form = NewTopicForm()
    return render(request, 'new_topic.html', {'forum': forum, 'form': form})

