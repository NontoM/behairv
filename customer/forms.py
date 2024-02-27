# forms.py
from django import forms

class UserProfileForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    username = forms.CharField(max_length=150)
    date_of_birth = forms.DateField(required=False)
    gender = forms.ChoiceField(choices=[(0, 'Male'), (1, 'Female')], required=False)
    number = forms.CharField(max_length=200, required=False)
    profile_picture = forms.ImageField(required=False)
    bio = forms.CharField(widget=forms.Textarea, required=False)
    address = forms.CharField(max_length=200, required=False)
    location_number = forms.IntegerField(required=False)
    city = forms.CharField(max_length=200, required=False)
    country = forms.CharField(max_length=200, required=False)
    zip_code = forms.CharField(max_length=10, required=False)


    # Optionally, you can add custom validation or widgets for specific fields
    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data.get('date_of_birth')
        # Your custom validation logic for date_of_birth
        return date_of_birth
