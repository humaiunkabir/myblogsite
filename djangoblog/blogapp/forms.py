from django import forms
from .models import article, author, comment


class createForm(forms.ModelForm):
    class Meta:
        model = article
        fields = [
            'title',
            'body',
            'image',
            'category'
        ]


class createAuthor(forms.ModelForm):
    class Meta:
        model = author
        fields = [
            'profile_picture',
            'detals'
        ]


class commentForm(forms.ModelForm):
    class Meta:
        model = comment
        fields = [
            'name',
            'email',
            'post_comment',
        ]
