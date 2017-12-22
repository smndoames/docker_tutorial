from django.test import TestCase
from django.urls import reverse

from .models import ToDo
from .forms import TodoForm


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
        self.client.post(reverse('toDo:index'), {'name': 'go to travel'})
        self.assertTrue(ToDo.objects.filter(name='go to travel').count() == 1)

    def test_should_do_not_add_to_db_when_item_has_empty_name(self):
        self.client.post(reverse('toDo:index'), {'name': ''})
        self.assertTrue(ToDo.objects.all().count() == 0)

    def test_should_show_warning_message_when_item_has_empty_name(self):
        response = self.client.post(reverse('toDo:index'), {'name': ''})
        self.assertContains(response, 'This field is required')

    def test_should_show_warning_message_when_name_charactor_more_than_100(self):
        response = self.client.post(
            reverse('toDo:index'),
                {'name':
                    '1234567890'
                    '1234567891'
                    '1234567892'
                    '1234567893'
                    '1234567894'
                    '1234567895'
                    '1234567896'
                    '1234567897'
                    '1234567898'
                    '1234567899'
                    '1'
                 })
        self.assertContains(response,
            'Ensure this value has at most '
            '100 characters')

    def test_should_redirect_to_index_after_finish(self):
        response = self.client.post(
            reverse('toDo:index'), {'name': 'go to travel'})
        self.assertEqual(response.status_code, 302)


class ClearSelectedViewTests(TestCase):
    def setUp(self):
        ToDo.objects.create(name='item1', is_selected=True)
        ToDo.objects.create(name='item2', is_selected=True)
        ToDo.objects.create(name='item3', is_selected=False)

    def test_should_de_selected_all_items(self):
        self.client.post(reverse('toDo:clear_selected'))
        self.assertEqual(ToDo.objects.get(name='item1').is_selected, False)
        self.assertEqual(ToDo.objects.get(name='item2').is_selected, False)
        self.assertEqual(ToDo.objects.get(name='item3').is_selected, False)

    def test_should_redirect_to_index_after_finish(self):
        response = self.client.post(reverse('toDo:clear_selected'))
        self.assertEqual(response.status_code, 302)


class CurateTodoViewTests(TestCase):
    def test_should_deselected_item_when_is_selected_is_true(self):
        item1 = ToDo.objects.create(name='item1', is_selected=True)
        self.client.post(
            reverse('toDo:curated_todo', kwargs={'pk': item1.id}))
        self.assertEqual(ToDo.objects.get(id=item1.id).is_selected, False)

    def test_should_selected_item_when_is_selected_is_False(self):
        item1 = ToDo.objects.create(
            name='item1', is_selected=False)
        self.client.post(
            reverse('toDo:curated_todo', kwargs={'pk': item1.id}))
        self.assertEqual(ToDo.objects.get(id=item1.id).is_selected, True)

    def test_should_redirect_page_after_finish(self):
        item1 = ToDo.objects.create(
            name='item1', is_selected=False)
        response = self.client.post(
            reverse('toDo:curated_todo', kwargs={'pk': item1.id}))
        self.assertEqual(response.status_code, 302)


class ToDoFormTests(TestCase):
    def test_should_return_false_if_name_is_empty(self):
        form = TodoForm({'name': ''})
        self.assertFalse(form.is_valid())

    def test_should_return_false_if_name_has_charactor_more_than_100(self):
        form = TodoForm({'name': '1234567890'
                                 '1234567891'
                                 '1234567892'
                                 '1234567893'
                                 '1234567894'
                                 '1234567895'
                                 '1234567896'
                                 '1234567897'
                                 '1234567898'
                                 '1234567899'
                                 '1'})
        self.assertFalse(form.is_valid())

    def test_should_return_true_when_name_is_not_empty_and_charactor_less_then_100(self):
        form = TodoForm({'name': 'Hello'})
        self.assertTrue(form.is_valid())