from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required 
from django.http import Http404

from .models import Topic, Entry
from .forms import TopicForm, EntryForm

def index(request):
    '''Home page of Learning Log'''
    return render(request, 'learning_logs/index.html')

@login_required
def topics(request):
    '''Displays list of topics'''
    topics = Topic.objects.order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)

@login_required
def topic(request, topic_id):
    '''Displays only one topic and all its entries'''
    topic = Topic.objects.get(id=topic_id)

    # Checks if the topic is owned by current user
    # check_topic_owner(topic.owner, request.user)
    
    entries = topic.entry_set.order_by('-date_added')
    owned_entries = topic.entry_set.filter(owner=request.user).order_by('-date_added')
    context = {'topic': topic, 'entries': entries, 'owned_entries': owned_entries}
    return render(request, 'learning_logs/topic.html', context)

@login_required
def new_topic(request):
    '''Defines new topic'''
    if request.method != 'POST':
        # Data isn't sent; creates blanck form
        form = TopicForm()
    else:
        # Data sent; Data processing
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('learning_logs:topics')

    # Displays blanck or unvalid form
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
    '''Adds new entry about specific topic'''
    topic = Topic.objects.get(id=topic_id)

    # check_topic_owner(topic.owner, request.user)
    
    if request.method != 'POST':
        # Data isn't sent; Creates blanck form
        form = EntryForm()
    else:
        # Displays POST data; Processes data
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.owner = request.user
            new_entry.topic = topic
            new_entry.save()
            return redirect('learning_logs:topic', topic_id=topic_id)
    
    # Displays blanck or unvalid form
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    '''Edits edits'''
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic

    check_entry_owner(entry.owner, request.user)

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

def check_topic_owner(owner, request):
    # Checks for the owner of the topic
    if owner != request:
        raise Http404
    
def check_entry_owner(owner, request):
    # Checks for the owner of the entry
    if owner != request:
        raise Http404

def handler404(request, exception=None):
    return render(request, "learning_logs/404.html")

def handler500(request, exception=None):
    return render(request, "learning_logs/500.html")