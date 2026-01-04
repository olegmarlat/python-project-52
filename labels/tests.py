from . import LabelCreationForm
from . import Label
from . import LabelTestCase


class TestLabelCreationForm(LabelTestCase):
    def test_valid_data(self):
        """Test that form is valid with correct data and label is created."""
        form = LabelCreationForm(data=self.valid_label_data)
        self.assertTrue(form.is_valid())
        label = form.save()
        self.assertEqual(label.name, self.valid_label_data['name'])
        self.assertEqual(Label.objects.count(), self.label_count + 1)

    def test_missing_fields(self):
        form = LabelCreationForm(data={
            'name': ''
        })
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)

    def test_duplicate_name(self):
        form = LabelCreationForm(data={
            'name': self.label1.name
        })
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)


class TestLabelModel(LabelTestCase):
    def create_test_label(self, **overrides):
        """Helper method to create a Label with optional overrides."""
        label_data = {
            'name': self.valid_label_data['name']
        }
        label_data.update(overrides)
        return Label.objects.create(**label_data)

    def test_label_creation(self):
        initial_count = Label.objects.count()
        label = self.create_test_label()
        self.assertEqual(Label.objects.count(), initial_count + 1)
        self.assertEqual(label.name, self.valid_label_data['name'])
        self.assertEqual(str(label), self.valid_label_data['name'])

    def test_duplicate_label_name(self):
        with self.assertRaises(Exception):
            self.create_test_label(name=self.label1.name)

    def test_blank_label_name(self):
        label = Label(name='')
        with self.assertRaises(Exception):
            label.full_clean()
