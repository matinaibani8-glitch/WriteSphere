from django import forms
from .models import usersign,story,BlogComment

class userform(forms.ModelForm):
    class Meta:
        model = usersign
        fields = "__all__"

class storyform(forms.ModelForm):
    class Meta:
        model = story
        fields = "__all__"

class BlogCommentForm(forms.ModelForm):
    class Meta:
        model = BlogComment
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={
                'placeholder': 'Write your comment...',
                'rows': 3,
                'class': 'form-control'
            })
        }
        
class updateform(forms.ModelForm):
    class Meta:
        model = story
        fields = ["title","category","content"]

class updatesign(forms.ModelForm):
    class Meta:
        model = usersign
        fields = ["firstname","lastname","gmail","password"]