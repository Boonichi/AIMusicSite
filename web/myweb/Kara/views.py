from django.shortcuts import render,redirect
from django.views.generic import View 
from django.urls import reverse
from django.http import JsonResponse,HttpResponse
from .models import file
from .forms import Uploadfile
from .LYRIC_ALIGN import Lyrics_to_alignment
from .get_lyric_song import take_lyric_song,get_vocal,get_lyric
from .result_to_json import convert_to_json_form,converto_time
from .libs import os,json
import librosa
# Create your views here.

class seaching_view(View):
    def get(self,request,*args, **kwargs):
        form=Uploadfile()
        return render(request,'Kara/searching.html',{'form':form})
     
    def post(self,request,*args, **kwargs):
        global song_search
        if('song_name' in request.POST.keys()):
            song_search=request.POST['song_name']
        else:
            song_search=''
            form=Uploadfile(request.POST,request.FILES)
            if(form.is_valid()):
                file.objects.create(vocal_file = request.FILES['vocal_file'],lyric_file=request.FILES['lyric_file'])
        return redirect(reverse('Kara:waiting'))


class waiting_view(View):
    def get(self,request,*args, **kwargs):
        return render(request,'Kara/waiting.html',{})
    def post(self,request,*args, **kwargs):
        info={}
        global path_song,lyric,song_name,author_name,function_lyric,number
        if(song_search!=''):
            lyric,number,path_song,song_name,author_name=take_lyric_song(song_search)
            function_lyric=None
        else:
            path_song     =os.path.join(os.getcwd(),'media',str(file.objects.all().order_by('-id')[0].vocal_file))
            lyric         =os.path.join(os.getcwd(),'media',str(file.objects.all().order_by('-id')[0].lyric_file))
            song_name     ="NULL"
            author_name   ="NULL"
            function_lyric=get_lyric
            number        =None
            
            
        word,treils_length,vocal,number,ori_lyric=Lyrics_to_alignment(path_song,lyric,number,get_lyric_function=function_lyric,get_vocal_function=get_vocal).run()
        output_file=convert_to_json_form(word,ori_lyric,number,converto_time,treils_length,len(vocal),'static/info','result.json')
        
        # output_file=convert_to_json_form(0,lyric,number,converto_time,0,0)
        
        info['lyrics']=output_file
        info['author_name']=author_name
        info['song_name']=song_name
        with open(os.path.join(os.getcwd(),'static/info/info_file.json'), "w",encoding='utf-8') as outfile:
            json.dump(info, outfile,ensure_ascii=False)
                            
        return redirect(reverse('Kara:result'))
    
class result_view(View):
    def get(self,request,*args, **kwargs):
        # json_data = open(os.path.join(os.getcwd(),'static/info/info_file.json'),'rb')
        # data1=json.load(json_data)
        # json_data.close()
        # path=data1['audio'].split(os.path.sep)
        # path=os.path.join(path[-2],path[-1])
        global path

        if(song_search!=''):
            path   =path_song.split(os.path.sep)
            path   =os.path.join(path[-2],path[-1])
            path   =os.path.join('http://127.0.0.1:8000/','media',path)
        else:
            path   =os.path.join('http://127.0.0.1:8000/','media',str(file.objects.all().order_by('-id')[0].vocal_file))
        return render(request,'Kara/result.html',{'file':path})
    
class API_JSON(View):
    def get(self,request):
       json_data = open(os.path.join(os.getcwd(),'static/info/info_file.json'),'rb')
       data1=json.load(json_data)
       json_data.close()
       with open(data1['lyrics'],'rb') as file:
           data1['lyrics']=json.load(file)
       data1=json.dumps(data1) #encode json 
       return JsonResponse({'data':data1})   