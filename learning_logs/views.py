from django.shortcuts import render, redirect

from .models import Topic, Entry
from .forms import TopicForm, EntryForm

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

def new_entry(request, topic_id):
    '''Adds new entry about specific topic'''
    topic = Topic.objects.get(id=topic_id)
    if request.method != 'POST':
        # Data isn't sent; Creates blanck form
        form = EntryForm()
    else:
        # Displays POST data; Processes data
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('learning_logs:topic', topic_id=topic_id)
    
    # Displays blanck or unvalid form
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)

def edit_entry(request, entry_id):
    '''Edits edits'''
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic

    if request.method != 'POST':
        # Oroginal request; form is filling with a data of this entry
        form = EntryForm(instance=entry)
    else:
        # Sending POST data; Processing data
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic', topic_id=topic.id)

    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)