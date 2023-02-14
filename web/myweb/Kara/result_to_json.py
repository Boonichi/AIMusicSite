from .libs import*

def check_special_sign(word):
    if("’" in word or '$' in word or '%' in word):
        return True
    return False

def converto_time(position,trellis_len,len_signal,sr,target_sr=1000):
    return int((position/trellis_len)*(len_signal/sr)*(target_sr))


def convert_to_json_form(word_segments,original_lyrics,number_sentence_word_per_sentence,convert_time,trellis_len,len_signal,output_folder='static/info',output_file='result.json'):
    result=[]
    index=0
    for order,sentence in enumerate(number_sentence_word_per_sentence):
        result.append({})
        result[order]['sentence']=' '.join(original_lyrics[index:index+sentence['count']])
        result[order]['s']=0
        result[order]['e']=0
        result[order]['w']=[]
        index+=sentence['count']
    
    index=0
    index_sentence=0
    count_word=0
    for w in original_lyrics:
        result[index_sentence]['w'].append({})
        if(not check_special_sign(w)): 
            result[index_sentence]['w'][count_word]['s']=convert_time(word_segments[index].start,trellis_len,len_signal,16000)
            result[index_sentence]['w'][count_word]['d']=w
            result[index_sentence]['w'][count_word]['e']=convert_time(word_segments[index].end,trellis_len,len_signal,16000)
            index +=1
        else: #some special situation
            result[index_sentence]['w'][count_word]['s']=convert_time(word_segments[index].start,trellis_len,len_signal,16000)
            result[index_sentence]['w'][count_word]['d']=w
            result[index_sentence]['w'][count_word]['e']=convert_time(word_segments[index+1].end,trellis_len,len_signal,16000)
            index +=2
        count_word+=1
        if(count_word==number_sentence_word_per_sentence[index_sentence]['count']):
            result[index_sentence]['s']=result[index_sentence]['w'][0]['s']
            result[index_sentence]['e']=result[index_sentence]['w'][-1]['e']
            index_sentence +=1
            count_word=0
            
    folder=os.path.join(os.getcwd(),output_folder)
    path=os.path.join(os.getcwd(),output_folder,output_file)
    if(not os.path.exists(folder)):
        os.makedirs(folder)
    
    with open(path, "w",encoding='utf-8') as outfile:
        json.dump(result, outfile,ensure_ascii=False)
        
    return path