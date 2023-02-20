from django import forms

class Uploadfile(forms.Form):
    lyric_file=forms.FileField()
    vocal_file=forms.FileField()
        