from django import forms
from .models import Course,Material,Aiprompt

class CourseForm(forms.ModelForm):
    class Meta:
        model=Course
        fields=['name','description','duration']


class MaterialForm(forms.ModelForm):
    class Meta:
        model=Material
        fields=['course','title','description','file']

# class AipromptForm(forms.ModelForm):
#     class Meta:
#         model=Aiprompt
#         fields=['course','title','personality','prompt_type','custom_prompt']