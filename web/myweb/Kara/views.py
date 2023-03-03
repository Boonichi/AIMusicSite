from django.shortcuts import render,redirect
from django.views.generic import View 
from django.urls import reverse
from django.http import JsonResponse

from .lyric_align import Lyrics_to_alignment
from .get_lyric_song import take_lyric_song
from .result_to_json import convert_to_json_form,converto_time
from .libs import os,json


# Create your views here.

class seaching_view(View):
    def get(self,request,*args, **kwargs):
        return render(request,'Kara/searching.html',{})
     
    def post(self,request,*args, **kwargs):
        global song_search
        song_search=request.POST['song_name']
        return redirect(reverse('Kara:waiting'))


class waiting_view(View):
    def get(self,request,*args, **kwargs):
       
        return render(request,'Kara/waiting.html',{})

    def post(self,request,*args, **kwargs):
        info={}
        lyric,lyric_number,path_song,song_name,author_name=take_lyric_song(song_search)
        word,treils_length,vocal=Lyrics_to_alignment(path_song,lyric).run()

        output_file=convert_to_json_form(word,lyric,lyric_number,converto_time,treils_length,len(vocal),'static/info','result.json')
        #output_file=convert_to_json_form(0,lyric,number,converto_time,0,0)
        info['lyrics']=output_file
        info['author_name']=author_name
        info['song_name']=song_name
        info['audio']=path_song
        
        with open(os.path.join(os.getcwd(),'static/info/info_file.json'), "w",encoding='utf-8') as outfile:
            json.dump(info, outfile,ensure_ascii=False)
                            
        return redirect(reverse('Kara:result'))
    
    
class result_view(View):
    def get(self,request,*args, **kwargs):
        json_data = open(os.path.join(os.getcwd(),'static/info/info_file.json'),'rb')
        data1=json.load(json_data)
        json_data.close()
        path=data1['audio'].split(os.path.sep)
        path=os.path.join(path[-2],path[-1])
        return render(request,'Kara/result.html',{'path':path})
    
class API_JSON(View):
    def get(self,request):
       json_data = open(os.path.join(os.getcwd(),'static/info/info_file.json'),'rb')
       data1=json.load(json_data)
       json_data.close()
       with open(data1['lyrics'],'rb') as file:
           data1['lyrics']=json.load(file)
       data1=json.dumps(data1) #encode json 
       return JsonResponse({'data':data1})   