from django import forms

class PostForm(forms.Form):
    title = forms.CharField(max_length=100)
    body = forms.CharField(widget=forms.Textarea(attrs={"rows":5, "cols":20}))
    id = forms.HiddenInput()