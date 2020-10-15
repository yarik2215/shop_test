from django.test import SimpleTestCase
from shop_app.forms import AddToCartForm, OrderForm

class AddToCartFormTest(SimpleTestCase):

    def test_add_correct_items_amount(self):
        form = AddToCartForm(data={'quantity':321})
        self.assertTrue(form.is_valid())

    def test_add_zero_items(self):
        form = AddToCartForm(data={'quantity':0})
        self.assertFalse(form.is_valid())

    def test_add_to_much_items(self):
        form = AddToCartForm(data={'quantity':9999999})
        self.assertFalse(form.is_valid())



class OrderFormTest(SimpleTestCase):
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.correct_data = {
            'first_name' : 'Bob',
            'last_name' : 'Bobston',
            'email' : 'bob@mail.com',
            'phone' : '380959484855',
            'comment' : 'Some text.',
        }

    def test_form_with_correct_data(self):
        data = self.correct_data.copy()
        form = OrderForm(data=data)
        self.assertTrue(form.is_valid())

    def test_empty_first_name(self):
        data = self.correct_data.copy()
        data['first_name'] = ''
        form = OrderForm(data=data)
        self.assertFalse(form.is_valid())

    def test_empty_last_name(self):
        data = self.correct_data.copy()
        data['last_name'] = ''
        form = OrderForm(data=data)
        self.assertFalse(form.is_valid())

    def test_empty_email(self):
        data = self.correct_data.copy()
        data['email'] = ''
        form = OrderForm(data=data)
        self.assertFalse(form.is_valid())

    def test_uncorrect_email(self):
        data = self.correct_data.copy()
        data['email'] = 'uncorrect@asd,ee!'
        form = OrderForm(data=data)
        self.assertFalse(form.is_valid())

    def test_empty_phone(self):
        data = self.correct_data.copy()
        data['phone'] = ''
        form = OrderForm(data=data)
        self.assertFalse(form.is_valid())

    def test_empty_comment(self):
        data = self.correct_data.copy()
        data['comment'] = ''
        form = OrderForm(data=data)
        self.assertTrue(form.is_valid())

