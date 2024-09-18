from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms

from payback.models import PaybackUser


class PaybackUserForm(forms.ModelForm):
    class Meta:
        model = PaybackUser
        fields = ['handle', 'group', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Submit'))
