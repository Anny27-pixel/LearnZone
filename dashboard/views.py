from django.shortcuts import render
from . forms import *
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.views import generic

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
    form = HomeworkForm()
    homeworks = Homework.objects.filter(user=request.user)
    if len(homeworks) == 0:
        homework_done = True  # No homework available
    else:
        homework_done = False  # Homework exists

    context = {
        'homeworks': homeworks,
        'homework_done': homework_done,
        'form':form,
    }
    return render(request, 'dashboard/homework.html', context)
    


