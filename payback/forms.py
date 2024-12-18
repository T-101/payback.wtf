from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms

from payback.models import PaybackUser


class PaybackUserForm(forms.ModelForm):
    class Meta:
        model = PaybackUser
        fields = ['handle', 'group', 'email']

    def __init__(self, *args, **kwargs):
        payback_user = kwargs.get('instance')
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        if payback_user.created_seven_days_ago:
            self.fields['handle'].disabled = True
            self.fields['email'].disabled = True
            self.fields['group'].disabled = True
            self.helper.form_tag = False
            self.helper.disable_csrf = True
        if not payback_user.created_seven_days_ago:
            self.helper.add_input(Submit('submit', 'Submit'))
