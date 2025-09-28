from django import forms
from django_select2.forms import Select2Widget

from blog.models import Post, Category


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields=['title', 'content','author']
        widgets={
            'title': forms.TextInput(attrs={'class':'form-control',"placeholder":"Title","autofocus":"true"}),
            'content':forms.Textarea(attrs={'class':'form-control','rows':8,"placeholder":"Content"}),
            'author':forms.TextInput(attrs={'class':'form-control',"placeholder":"Author"}),
        }

    def clean_title(self):
        title=(self.cleaned_data.get('title') or "").strip()
        if len(title) < 3:
            raise forms.ValidationError("Title must be at least 3 characters long")
        return title

    def clean_content(self):
        content=(self.cleaned_data.get('content') or "").strip()
        if len(content) < 10:
            raise forms.ValidationError("Content must be at least 10 characters long")
        return content

class CategoryForm(forms.Form):
    category=forms.ModelChoiceField(
        queryset=Category.objects.all(),
        label="Choose a Category",
        widget=Select2Widget(attrs={'class': 'select2'})
    )

class CategoryCreateForm(forms.ModelForm):
    class Meta:
        model = Category
        fields=['title']
        widgets={
            'title': forms.TextInput(attrs={'class':'form-control',"placeholder":"Category","autofocus":"true"}),
        }
    def clean_title(self):
        category=(self.cleaned_data.get('title') or "").strip()
        if len(category) < 3:
            raise forms.ValidationError("Title must be at least 3 characters long")
        return category

