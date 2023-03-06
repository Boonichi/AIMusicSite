from django.shortcuts import render,redirect
from django.views.generic import View 
from django.urls import reverse
from django.http import JsonResponse
from .models import file
import os
import json
from .forms import Uploadfile
from .get_lyric_song import take_lyric_song
import requests


# Create your views here.

class seaching_view(View):
    
    def get(self,request,*args, **kwargs):
        
        return render(request,'Kara/searching.html',{'err':""})
     
    def post(self,request,*args, **kwargs):
        data={
            'err':''
        }
        global song_search
        if('song_name' in request.POST.keys()):
            song_search=request.POST['song_name']
            return redirect(reverse('Kara:waiting'))
        else:
            song_search=''
            form=Uploadfile(request.POST,request.FILES)
            if(form.is_valid()):
                file.objects.create(vocal_file = request.FILES['vocal_file'],lyric_file=request.FILES['lyric_file'])
                return redirect(reverse('Kara:waiting'))
            else:
                data['err']=form.non_field_errors().as_text().replace("*",'')
                return render(request,'Kara/searching.html',data)

class waiting_view(View):
    def get(self,request,*args, **kwargs):
        return render(request,'Kara/waiting.html',{})
    
    def post(self,request,*args, **kwargs):
        info={}
        global song_path,song_name,author_name,lyric_path
        if(song_search!=''):
            lyric,number,song_path,song_name,author_name=take_lyric_song(song_search)
            
            lyric_path=os.path.join(os.getcwd(),'media','lyric','searching.txt')
            
            with open(lyric_path,'w',encoding='utf-8') as output:
                current_sentence=0
                num=0
                for word in lyric:
                    output.write(word)
                    num += 1
                    if(num<number[current_sentence]['count']):
                        output.write(" ")
                    else:
                        output.write("\n")
                        current_sentence+=1
                        num=0
        else:
            song_path     =os.path.join(os.getcwd(),'media',str(file.objects.all().order_by('-id')[0].vocal_file))
            lyric_path         =os.path.join(os.getcwd(),'media',str(file.objects.all().order_by('-id')[0].lyric_file))
            song_name     ="NULL"
            author_name   ="NULL"
            
        
        lyric_timestamps = request_serving(song_path, lyric_path)
        
        folder=os.path.join(os.getcwd(),'static/info')
        path=os.path.join(os.getcwd(),'static/info','result.json')
        
        if(not os.path.exists(folder)):
            os.makedirs(folder)
            
        with open(path, "w",encoding='utf-8') as outfile:
            json.dump(lyric_timestamps, outfile,ensure_ascii=False)
        
        info['lyrics']=path
        info['author_name']=author_name
        info['song_name']=song_name
        with open(os.path.join(os.getcwd(),'static/info/info_file.json'), "w",encoding='utf-8') as outfile:
            json.dump(info, outfile,ensure_ascii=False)
                            
        return redirect(reverse('Kara:result'))
    
class result_view(View):
    def get(self,request,*args, **kwargs):
        global path

        if(song_search!=''):
            path   =song_path.split(os.path.sep)
            path   =os.path.join(path[-2],path[-1])
            path   =path
        else:
            path   =str(file.objects.all().order_by('-id')[0].vocal_file)
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
    

def request_serving(song_path, lyric_path):
        url = "http://localhost:8080/predictions/lyric_align"

        files = {
            'data' : open(song_path, "rb"),
            'script' : open(lyric_path)
        }

        response = requests.post(url, files = files)
        
        return response.json()