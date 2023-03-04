from django.db import models

# Create your models here.
class file(models.Model):
    lyric_file=models.FileField(upload_to='lyric')
    vocal_file=models.FileField(upload_to='vocal')