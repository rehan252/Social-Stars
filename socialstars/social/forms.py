from django import forms
from social.models import Post


class PostForm(forms.ModelForm):
    post = forms.CharField(widget=forms.Textarea(
        attrs={
            'label': "What's new....",
            'rows': 6,
            'class': 'form-control new-post',
            'placeholder': 'Write new post...'
        }
    ))

    post_image = forms.ImageField(required=False)

    class Meta:
        model = Post
        fields = ('post', 'post_image',)



