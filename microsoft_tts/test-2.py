from transformers import SpeechT5Processor, SpeechT5ForTextToSpeech, SpeechT5HifiGan
from datasets import load_dataset
import torch
import soundfile as sf
from datasets import load_dataset

processor = SpeechT5Processor.from_pretrained("microsoft/speecht5_tts")
model = SpeechT5ForTextToSpeech.from_pretrained("microsoft/speecht5_tts")
vocoder = SpeechT5HifiGan.from_pretrained("microsoft/speecht5_hifigan")

inputs = processor(text="Hello, my name is Deepak, and I'm here to assist you as a Customer Service Executive at ICICI Bank. With a strong background in banking and financial services, I am dedicated to helping you navigate through your banking needs, whether it's about managing your accounts, understanding loan options, exploring investment opportunities, or utilizing our banking facilities. I am committed to ensuring that your experience with ICICI Bank is smooth, efficient, and satisfying. Your financial well-being is my top priority.", return_tensors="pt")

# load xvector containing speaker's voice characteristics from a dataset
embeddings_dataset = load_dataset("Matthijs/cmu-arctic-xvectors", split="validation")
speaker_embeddings = torch.tensor(embeddings_dataset[7306]["xvector"]).unsqueeze(0)

speech = model.generate_speech(inputs["input_ids"], speaker_embeddings, vocoder=vocoder)

sf.write("speech-2.wav", speech.numpy(), samplerate=16000)
