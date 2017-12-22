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
        self.assertQuerysetEqual(
            response.context['todos'],
                    ['<ToDo: item1>', '<ToDo: item2>', '<ToDo: item3>'])

    def test_should_add_new_item_to_db_after_call_post_method(self):
        response = self.client.post(reverse('toDo:index'), {'name': 'go to travel'})
        self.assertTrue(ToDo.objects.filter(name='go to travel').count() == 1)

    def test_should_not_add_the_item_that_has_empty_name_and_show_warning_message(self):
        response = self.client.post(reverse('toDo:index'), {'name': ''})
        self.assertTrue(ToDo.objects.all().count() == 0)
        self.assertContains(response, 'This field is required')


class ClearSelectedViewTests(TestCase):
    def setUp(self):
        ToDo.objects.create(name='item1', is_selected=True)
        ToDo.objects.create(name='item2', is_selected=True)
        ToDo.objects.create(name='item3', is_selected=False)

    def test_should_de_selected_all_items(self):
        response = self.client.post(reverse('toDo:clear_selected'))
        self.assertEqual(ToDo.objects.get(name='item1').is_selected, False)
        self.assertEqual(ToDo.objects.get(name='item2').is_selected, False)
        self.assertEqual(ToDo.objects.get(name='item3').is_selected, False)

    def test_should_redirect_to_index_after_finish(self):
        response = self.client.post(reverse('toDo:clear_selected'))
        self.assertEqual(response.status_code, 302)