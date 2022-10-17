from django.shortcuts import render, redirect

from .models import Topic
from .forms import TopicForm

def index(request):
    '''Home page of Learning Log'''
    return render(request, 'learning_logs/index.html')

def topics(request):
    '''Displays list of topics'''
    topics = Topic.objects.order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)

def topic(request, topic_id):
    '''Displays only one topic and all its entries'''
    topic = Topic.objects.get(id=topic_id)
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)

def new_topic(request):
    '''Defines new topic'''
    if request.method != 'POST':
        # Data isn't sent; creates blanck form
        form = TopicForm()
    else:
        # Data sent; Data processing
        form = TopicForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topics')

    # Displays blanck or unvalid form
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)