from django import forms

from .models import Post, Comment

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text',)

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('author', 'text',)
        

class ContactForm(forms.Form):
    #contact_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'form-group col-xs-12 floating-label-form-group controls'}))
    contact_name = forms.CharField(required=True)
    contact_email = forms.EmailField(required=True)
    #contact_number = forms.CharField(widget=forms.TextInput(attrs={'type':'number'}))
    contact_number = forms.CharField(required=True)
    contact_message = forms.CharField(required=True,widget=forms.Textarea)
