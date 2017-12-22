from django.shortcuts import render
from django.shortcuts import redirect
from django.views import generic, View

from .forms import TodoForm
from .models import ToDo


class IndexView(generic.ListView):
    def get_queryset(self):
        return ToDo.objects.all().order_by('id')

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


class ClearSelectedView(View):
    def get_queryset(self):
        return ToDo.objects.all()

    def post(self, request, *args, **kwargs):
        todos = self.get_queryset()
        for todo in todos:
            todo.is_selected = False
            todo.save()
        return redirect('toDo:index')


class CurateTodo(generic.DetailView):
    model = ToDo

    def post(self, request, *args, **kwargs):
        todo = self.get_object()
        todo.is_selected = not todo.is_selected
        todo.save()
        return redirect('toDo:index')