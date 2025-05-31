from django import forms
from .models import GameComment

class GameCommentForm(forms.ModelForm):
    parent = forms.ModelChoiceField(
        queryset=GameComment.objects.all(), 
        required=False, 
        widget=forms.HiddenInput(attrs={'id': 'id_parent'})
    )

    class Meta:
        model = GameComment
        fields = ['content', 'parent']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Yorumunuzu yazın...',
                'id': 'id_content'
            }),
        }
