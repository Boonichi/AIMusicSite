import numpy as np


Gro=[
            {
                "d": "Gió",
                "s": 88,
                "e": 537
            },
            {
                "d": "mùa",
                "s": 547,
                "e": 897
            },
            {
                "d": "đông",
                "s": 897,
                "e": 1187
            },
            {
                "d": "bắc",
                "s": 1187,
                "e": 1588
            },
            {
                "d": "se",
                "s": 1597,
                "e": 2367
            },
            {
                "d": "lạnh.",
                "s": 2358,
                "e": 2390
            }  
]

Pre=[
            {
                "d": "Gió",
                "s": 0,
                "e": 86
            },
            {
                "d": "mùa",
                "s": 547,
                "e": 1500
            },
            {
                "d": "đông",
                "s": 897,
                "e": 1187
            },
            {
                "d": "bắc",
                "s": 1187,
                "e": 1588
            },
            {
                "d": "se",
                "s": 1597,
                "e": 2367
            },
            {
                "d": "lạnh.",
                "s": 2358,
                "e": 2358
            }  
]



def take_infor(jsondata_arr):
    s=[]
    e=[]
    for dict in jsondata_arr:
        s.append(dict['s'])
        e.append(dict['e'])
    s=np.array(s)
    e=np.array(e)
    
    return np.concatenate((np.expand_dims(s,0),np.expand_dims(e,0)),0)

def calculate_IOU(Gro,Pre):
    max_s=np.max((np.concatenate((np.expand_dims(Gro[0],0),np.expand_dims(Pre[0],0)))),0)
    
    min_e=np.min((np.concatenate((np.expand_dims(Gro[1],0),np.expand_dims(Pre[1],0)))),0)
    
    IOU=min_e-max_s
    IOU=np.where(IOU==0,1,IOU)
    IOU=np.where(IOU<0,0,IOU)
    
    return IOU

    
def Accuracy(Groundtruth,Prediction):
    Pre_s_e= np.empty((2,len(Prediction))) # 2,l
    Gro_s_e= np.empty((2,len(Groundtruth)))

    Pre_s_e=take_infor(Prediction)
    Gro_s_e=take_infor(Groundtruth)
    
    IOU=calculate_IOU(Gro_s_e,Pre_s_e)
    UNION=(Pre_s_e[1]-Pre_s_e[0]) + (Gro_s_e[1]-Gro_s_e[0]) -IOU
    UNION=np.where(UNION<0,1,UNION)
    print(IOU)
    print(UNION)
    
    acc=IOU/UNION
    
    return   (np.sum(acc)/(len(IOU)))*100


print(Accuracy(Gro,Pre))
    
      
    
    