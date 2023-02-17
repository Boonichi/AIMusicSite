from .libs import*


def get_denoiser(device="cuda"):
    # Use a pre-trained model
    separator = pretrained.get_model(name="mdx").models[3]
    separator.to(device)
    separator.eval()
    return separator




def run_denoiser(separator, vocal,sample_rate=None,get_vocal_function=None):
    global mix,sr
    
    if(get_vocal_function!=None):
        mix,sr=get_vocal_function(vocal)
    else:
        mix=vocal
        sr=sample_rate
            
    if((type(mix)==numpy.ndarray or type(mix)==torch.Tensor)):
        if(type(mix)==numpy.ndarray):
            mix=torch.from_numpy(mix)
    else:
        if(get_vocal_function == None):
            raise TypeError('get_vocal_function must return numpy.ndarry or torch.Tensor')
        else:
            raise TypeError('vocal must be in numpy.ndarray or torch Tensor type')    
    
    src_rate = separator.samplerate  # 44100
    mix = mix.to(device)  # instead of cuda because some computer can't use cuda
    ref = mix.mean(dim=0)  # mono mixture
    mix = (mix - ref.mean()) / ref.std()
    mix = convert_audio(mix, src_rate, separator.samplerate, separator.audio_channels)

    # Separate
    with torch.no_grad():
        estimates = apply_model(separator, mix[None], overlap=0.25)[0]  # defalut 0.25

    estimates = estimates * ref.std() + ref.mean()  # estimates * std + mean
    return estimates[3].cpu().numpy()[0, ...],sr