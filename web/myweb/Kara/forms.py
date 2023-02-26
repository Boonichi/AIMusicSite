from django import forms
from django.core.exceptions import ValidationError
ALLOWED_TYPES_VOCAL = ['mp3', 'wav']
ALLOWED_TYPES_LYRIC = ['txt']
class Uploadfile(forms.Form):
    lyric_file=forms.FileField()
    vocal_file=forms.FileField()
    
    
    def clean(self):
        cleaned_data=super().clean()
        vocal=str(cleaned_data['vocal_file'])
        _,type_vocal=vocal.split('.')
        if(type_vocal not in ALLOWED_TYPES_VOCAL):
            raise ValidationError('Vocal file is not in correct form must be in mp3 or wav')
        lyric=str(cleaned_data['lyric_file'])
        _,type_lyric=lyric.split('.')
        if(type_lyric not in ALLOWED_TYPES_LYRIC):
            raise ValidationError('Lyric file is not in correct form must be in txt')
        return cleaned_data
    
    