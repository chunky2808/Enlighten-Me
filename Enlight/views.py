from django.contrib.auth.models import User
from django.shortcuts import render,get_object_or_404,redirect
from .models import Forum,Topic,Post
from .forms import NewTopicForm
from django.contrib.auth.decorators import login_required


def forum_list(request):
	forums = Forum.objects.all()
	# for fori in forums:
	# 	print(fori.name)
	# 	print(fori.desc)
	return render(request,'home.html',{'forums':forums})

def topic_list(request, pk):
	forums = get_object_or_404(Forum,pk=pk)
	topics = forums.topics.all()
	return render(request,'topics.html',{'topics' : topics,'forums' : forums})

def topic_posts(request, pk, topic_pk):
    topic = get_object_or_404(Topic, forum__pk=pk, pk=topic_pk)
    return render(request, 'topic_posts.html', {'topic': topic})

@login_required
def new_topic(request, pk):
    forum = get_object_or_404(Forum, pk=pk)
    user = User.objects.first()
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.forum= forum
            topic.started_by = request.user
            topic.save()
            post = Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=request.user
            )
            return redirect('topic', pk=forum.pk)
    else:
        form = NewTopicForm()
    return render(request, 'new_topic.html', {'forum': forum, 'form': form})


#def reply_topic(request):
