from django.test import TestCase
from django.urls import reverse
from .models import ToDo

class IndexViewTests(TestCase):
    def test_should_return_empty_list_when_no_items(self):
        response = self.client.get(reverse('toDo:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['todos'], [])

    def test_should_return_3_items_when_there_are_3_items_in_db(self):
        ToDo.objects.create(name='item1')
        ToDo.objects.create(name='item2')
        ToDo.objects.create(name='item3')
        response = self.client.get(reverse('toDo:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['todos'], ['<ToDo: item1>', '<ToDo: item2>', '<ToDo: item3>'])
