from django.shortcuts import render
from . forms import *
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.views import generic
from datetime import datetime
from django.utils import timezone






# Create your views here.
def home(request):
    return render(request, 'dashboard/home.html')

def notes(request):
    if request.method == 'POST':
        form = NotesFrom(request.POST)
        if form.is_valid():
            notes = Notes(user = request.user,title=request.POST['title'],description=request.POST['description'])
            notes.save()
        messages.success(request, f"Notes added from {request.user.username} successfully")
    else:
        form = NotesFrom()
    notes = Notes.objects.filter(user = request.user)
    context = {'notes':notes, 'form':form}
    return render(request, 'dashboard/notes.html',context)

def delete_note(request, pk=None):
    Notes.objects.get(id=pk).delete()
    return redirect("notes")

class NotesDetailView(generic.DetailView):
    model = Notes

def homework(request):
    if request.method == 'POST':
        form = HomeworkForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST.get('is_finished', 'off')
                finished = True if finished == 'on' else False
            except:
                finished = False
            
            # Check if the 'due' field contains time, if not add default time
            due = request.POST['due']
            if len(due) == 10:  # Date only (YYYY-MM-DD)
                due += " 00:00:00"  # Add default time

            # Convert to timezone-aware datetime
            due = timezone.make_aware(datetime.strptime(due, "%Y-%m-%d %H:%M:%S"))

            # Create the Homework object
            homeworks = Homework(
                user=request.user,
                subject=request.POST['subject'],
                title=request.POST['title'],
                description=request.POST['description'],
                due=due,
                is_finished=finished
            )
            homeworks.save()
            
            form = HomeworkForm()  # Reset the form
            messages.success(request, f'Homework added from {request.user.username}')
    else:
        form = HomeworkForm()

    # Fetch all homework for the user
    homeworks = Homework.objects.filter(user=request.user)
    homework_done = True if not homeworks else False  # No homework available if empty

    context = {
        'homeworks': homeworks,
        'homework_done': homework_done,
        'form': form,
    }
    return render(request, 'dashboard/homework.html', context)

def update_homework(request, pk=None):
    homework = Homework.objects.get(id=pk)
    
    # Toggle the is_finished field
    homework.is_finished = not homework.is_finished
    homework.save()
    
    return redirect('homework')

def delete_homework(request, pk=None):
    Homework.objects.get(id=pk).delete()
    return redirect('homework')

from django.shortcuts import render, redirect
from .forms import DashboardFom
from youtubesearchpython import VideosSearch

def youtube(request):
    if request.method == 'POST':
        form = DashboardFom(request.POST)
        text = request.POST['text']
        video = VideosSearch(text, limit=10)
        result_list =[]
        for i in video.result()['result']:
            result_dict = {
                'input':text,
                'title':i['title'],
                'duration':i['duration'],
                'thumbnail':i['thumbnails'][0]['url'],
                'channel':i['channel']['name'],
                'link':i['link'],
                'views':i['viewCount']['short'],
                'published':i['publishedTime']
            }
            desc = ''
            if i['descriptionSnippet']:
                for j in i['descriptionSnippet']:
                    desc += j['text']
            result_dict['description'] = desc
            result_list.append(result_dict)
            context = {
                'form':form,
                'results':result_list
            }
        return render(request, 'dashboard/youtube.html',context)
    else:
        form = DashboardFom()
    context ={'form':form}
    return render(request, 'dashboard/youtube.html',context)



def todo(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST['is_finished']
                if finished == 'on':
                    finished = True
                else:
                    finished = False
            except:
                finished = False
            todos = Todo(
                user = request.user,
                title = request.POST['title'],
                is_finished = finished
            )
            todos.save()
            messages.success(request, f"Todo added from {request.user.username}")
    else:
        form = TodoForm()
    todo = Todo.objects.filter(user = request.user)
    if len(todo) == 0:
        todos_done = True
    else:
        todos_done = False
    context = {
        'form':form,
        'todos':todo,
        'todos_done':todos_done
    }
    return render(request, 'dashboard/todo.html',context)