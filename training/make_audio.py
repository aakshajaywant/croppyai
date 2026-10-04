"""Pre-record the advisories as MP3 so the phone plays them offline, even with no TTS voice installed.
Run in Colab:  !pip -q install transformers torch scipy pydub && apt -qq install ffmpeg
Uses Meta MMS-TTS (facebook/mms-tts-swh for Swahili, facebook/mms-tts-eng for English).
Have a native speaker listen to every clip before the demo."""
import re, torch, scipy.io.wavfile as wav
from pathlib import Path
from pydub import AudioSegment
from transformers import VitsModel, AutoTokenizer

html = Path("../app/index.html").read_text(encoding="utf-8")
block = html[html.index("const ADVICE"):html.index("/* ---------- Helpers")]
MODELS = {"sw": "facebook/mms-tts-swh", "en": "facebook/mms-tts-eng"}
for lang, name in MODELS.items():
    tok, mdl = AutoTokenizer.from_pretrained(name), VitsModel.from_pretrained(name)
    out = Path(f"../app/audio/{lang}"); out.mkdir(parents=True, exist_ok=True)
    for key in ["rust", "miner", "cercospora", "phoma", "healthy", "unsure", "bean_als", "bean_rust", "bean_healthy"]:
        seg = block[re.search(r"(?<![\w])" + key + r":\{", block).start():]
        m = re.search(lang + r':\{t:"(.*?)",a:"(.*?)"\}', seg)
        text = f"{m.group(1)}. {m.group(2)}"
        with torch.no_grad():
            w = mdl(**tok(text, return_tensors="pt")).waveform[0].numpy()
        wav.write("/tmp/x.wav", mdl.config.sampling_rate, w)
        AudioSegment.from_wav("/tmp/x.wav").export(out / f"{key}.mp3", format="mp3", bitrate="32k")
        print(lang, key, "ok")
