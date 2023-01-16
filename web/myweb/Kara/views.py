from django.shortcuts import render,redirect
from django.views.generic import View 
from django.urls import reverse


from LYRIC_ALIGN import Lyrics_to_alignment
from get_lyric_song import take_lyric_song
# Create your views here.

class seaching_view(View):
    def get(self,request,*args, **kwargs):
        return render(request,'Kara/searching.html',{})
     
    def post(self,request,*args, **kwargs):
        global song_name
        song_name=request.POST['song_name']
        return redirect(reverse('Kara:waiting'))


class waiting_view(View):
    def get(self,request,*args, **kwargs):
       
        return render(request,'Kara/waiting.html',{})
    def post(self,request,*args, **kwargs):
        global word,treils_length,vocal
        
        lyric,path_song=take_lyric_song(song_name)
        
        word,treils_length,vocal=Lyrics_to_alignment(path_song,lyric).run()

        return redirect(reverse('Kara:result'))
    
    
class result_view(View):
    def get(self,request,*args, **kwargs):
        return render(request,'Kara/result.html')