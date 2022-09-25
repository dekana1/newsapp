from django import forms
from .models import Comments


class CommentForm(forms.ModelForm):
    text = forms.CharField(max_length=250, widget=forms.Textarea(attrs={
        "class":"form-control", "id": "comment_text", "placeholder": "Great content..."
    }))
    
    class Meta:
        model = Comments
        fields = ['text']