import os

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required 
from django.http import Http404

from .models import Topic, Entry
from .forms import TopicForm, EntryForm

allowed_urls = [
    'https://www.youtube.com/',
    'https://youtu.be/',
]

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

    entries = topic.entry_set.order_by('-date_added')

    saved_images = saved_image_checker()

    owned_entries = topic.entry_set.filter(owner=request.user).order_by('-date_added')
    context = {'topic': topic, 'entries': entries, 'owned_entries': owned_entries, 'saved_images': saved_images}
    return render(request, 'learning_logs/topic.html', context)

@login_required
def new_topic(request):
    '''Defines new topic'''
    check_is_superuser(request.user)

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
def edit_topic(request, topic_id):
    topic = Topic.objects.get(id=topic_id)

    check_is_superuser(request.user)

    if request.method != 'POST':
        form = TopicForm(instance=topic)
    else:
        form = TopicForm(data=request.POST, instance=topic)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topics')
    
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_topic.html', context)

@login_required
def new_entry(request, topic_id):
    '''Adds new entry about specific topic'''
    topic = Topic.objects.get(id=topic_id)

    
    if request.method != 'POST':
        # Data isn't sent; Creates blanck form
        form = EntryForm()
    else:
        # Displays POST data; Processes data
        form = EntryForm(request.POST, request.FILES)
        if form.is_valid() and (form.clean()['text'] != '' or form.clean()['image'] != None):
            new_entry = form.save(commit=False)
            new_entry.owner = request.user
            new_entry.topic = topic

            if any([url in new_entry.text for url in allowed_urls]):
                new_entry.url = new_entry.text
                new_entry.text = ''

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

    saved_images = saved_image_checker()

    if request.method != 'POST':
        # Oroginal request; form is filling with a data of this entry
        form = EntryForm(instance=entry)
    else:
        # Sending POST data; Processing data
        form = EntryForm(files=request.FILES, data=request.POST, instance=entry)
        if form.is_valid() and (form.clean()['text'] != '' or form.clean()['image'] != None):
            form.save()
            return redirect('learning_logs:topic', topic_id=topic.id)

    context = {'entry': entry, 'topic': topic, 'form': form, 'saved_images': saved_images}
    return render(request, 'learning_logs/edit_entry.html', context)

def delete_entry(request, entry_id):
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic

    entry.delete()
    return redirect('learning_logs:topic', topic_id=topic.id)

def check_is_superuser(user):
    # Checks is the user is superuser
    if not(user.is_superuser):
        raise Http404
    
def check_entry_owner(owner, user):
    # Checks for the owner of the entry
    if owner != user and not(user.is_superuser):
        raise Http404

def handler404(request, exception=None):
    return render(request, "learning_logs/404.html")

def handler500(request, exception=None):
    return render(request, "learning_logs/500.html")

def saved_image_checker():
    '''Gets list of saved images of the server and returnes it'''
    dirname = "media\images"
    saved_images = [f"images/{image}" for image in os.listdir(dirname)]
    return saved_images

# test section
import json
from django.views.generic import ListView

class InfoListView(ListView):
    model = Topic
    template_name = 'learning_logs/search_test.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["qs_json"] = json.dumps(list(Topic.objects.values('id', 'text', 'descr')))
        return context