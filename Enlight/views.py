from django.contrib.auth.models import User
from django.db.models import Count
from django.shortcuts import render,get_object_or_404,redirect
from .models import Forum, Topic, Post
from .forms import NewTopicForm, PostForm
from django.contrib.auth.decorators import login_required
from newsapi import NewsApiClient
from django.http import HttpResponse

newsapi = NewsApiClient(api_key='')


def forum_list(request):
    forums = Forum.objects.all()
    # for fori in forums:
    # 	print(fori.name)
    # 	print(fori.desc)
    return render(request,'home.html',{'forums':forums})


def topic_list(request, pk):
    forums = get_object_or_404(Forum,pk=pk)
    topics = forums.topics.order_by('-last_updated').annotate(replies=Count('posts') - 1)
    return render(request,'topics.html',{'topics' : topics,'forums' : forums})


def topic_posts(request, pk, topic_pk):
    topic = get_object_or_404(Topic, forum__pk=pk, pk=topic_pk)
    topic.views += 1
    topic.save()
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
            return redirect('topic', pk=pk)
    else:
        form = NewTopicForm()
    return render(request, 'new_topic.html', {'forum': forum, 'form': form})


@login_required
def reply_topic(request, pk, topic_pk):
    topic = get_object_or_404(Topic, forum__pk=pk, pk=topic_pk)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()
            return redirect('topic_posts', pk=pk, topic_pk=topic_pk)
    else:
        form = PostForm()
    return render(request, 'reply_topic.html', {'topic': topic, 'form': form})


def delete(request, pk, topic_pk):
    topic = get_object_or_404(Topic, forum__pk=pk, pk=topic_pk)
    topic.delete()
    forums = get_object_or_404(Forum,pk=pk)
    topics = forums.topics.order_by('-last_updated').annotate(replies=Count('posts') - 1)
    return render(request,'topics.html',{'topics' : topics,'forums' : forums})

    # return render(request, 'topic_posts.html' , {'topic': topic})


def news(request):
    top_headlines = newsapi.get_top_headlines(
                                          sources='techradar,techcrunch,ars-technica,crypto-coins-news,engadget,hacker-news,recode,t3n,the-next-web,the-verge,wired',
                                          #sources='techradar',
                                          language='en',
                                          #pageSize = ,
                                          #page=5,
                                          )
    #print(top_headlines)
    li = []
    for i in top_headlines:
        if i == "articles":
            #print(top_headlines[i])
            p = top_headlines[i]
            for k in top_headlines[i]:
                for l in k:
                    #print(l)
                    abc = {}
                    if l == "title":
                        abc["Title"]  = k[l]
                        li.append(abc)
                    elif l == "description":
                        abc["Description"]  = k[l]
                        li.append(abc)
                    elif l == "url":
                        abc["Url"]  = k[l]
                        li.append(abc)   
                #print(k)
                # if k == "source":
                #     print(title)
        elif i == "totalResults":
            totalResults = top_headlines[i]
            #print(totalResults)
    #print(li)
    #return HttpResponse("hi")
    return render(request,'news.html',{'li' : li})


