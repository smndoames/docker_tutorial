from django.shortcuts import render
from django.shortcuts import redirect
from django.views import generic

from .forms import TodoForm
from .models import ToDo


class IndexView(generic.ListView):
    def get_queryset(self):
        return ToDo.objects.all()

    def get(self, request, *args, **kwargs):
        todos = self.get_queryset()
        form = TodoForm()
        return render(request, 'toDo/content.html',
                      {'form': form, 'todos': todos})

    def post(self, request, *args, **kwargs):
        todos = self.get_queryset()
        form = TodoForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('toDo:index')
        return render(request, 'toDo/content.html',
                      {'form': form, 'todos': todos})


class CurateTodo():
    def post(self, request, *args, **kwargs):
        todos = self.get_queryset()
        form = TodoForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('toDo:index')
        return render(request, 'toDo/content.html',
                      {'form': form, 'todos': todos})
