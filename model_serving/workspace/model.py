from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC

processor          = Wav2Vec2Processor.from_pretrained("nguyenvulebinh/wav2vec2-base-vietnamese-250h")
model              = Wav2Vec2ForCTC.from_pretrained("nguyenvulebinh/wav2vec2-base-vietnamese-250h")

processor.save_pretrained('./my_tokenizer/')
model.save_pretrained('./my_model/')