import librosa 
import numpy
import numpy as np


class Processing():
    
    def __init__(self,signal,sr=22050):
        self.signal=signal
        self.sr=sr # sampling rate
    
    def FFT(self,rato_frequen_bin=0.5):# DFT FT 
        FT=np.fft.fft(self.signal)
        magnitude=np.absolute(FT)
        
        return magnitude[:self.sr*rato_frequen_bin] #(#frequency bin = sampling rate)DB
    
    def STFT(self,N_fft=2048,HOP_SIZE=512,window='hann'):
        STFT = librosa.stft(self.signal, n_fft=N_fft, hop_length=HOP_SIZE,window=window)
        
        STFT=np.abs(STFT)** 2
        
        STFT_log_scale = librosa.power_to_db(STFT)
        
        return STFT_log_scale  # (#frequency bin=(sr-framesize)/hopsize +1,#frames=(frame size)/2 +1)
    
    def Mel_spectograms(self,number_mel=10,N_fft=2048,HOP_SIZE=512,window='hann'):
        mel_spectrogram = librosa.feature.melspectrogram(self.signal, sr=self.sr, n_fft=N_fft, hop_length=HOP_SIZE, n_mels=number_mel)
        
        log_mel_spectrogram = librosa.power_to_db(mel_spectrogram)
        
        return log_mel_spectrogram #(#n_mel,#frames=(frame size)/2 +1)
    
    
    def MFCCs(self,n_mfcc=20):
        mfccs = librosa.feature.mfcc(y=self.signal, n_mfcc=n_mfcc, sr=self.sr)
        
        return mfccs #(#n_mfcc,#frame)
    

    def CQT(self,hop_length=512, fmin=None, n_bins=84):
        cqt=librosa.cqt(y=self.signal,sr=self.sr,hop_length=hop_length,fmin=fmin,n_bins=n_bins)
        
        return cqt #…, n_bins, t
        
