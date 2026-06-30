#!/usr/bin/env python3
"""
Herramienta reutilizable de ElevenLabs para el portafolio.

NO contiene ninguna clave. Lee la API key desde la variable de entorno
ELEVENLABS_API_KEY (o desde un archivo .env local, que está en .gitignore).

Uso:
  export ELEVENLABS_API_KEY=...        # o crea tools/elevenlabs/.env
  python3 tools/elevenlabs/tts.py voices
  python3 tools/elevenlabs/tts.py say "Texto a leer" salida.mp3 [voice_id]

Voz por defecto: Desmond (la usada en /motivacion).
"""
import sys, os, json, base64, urllib.request, urllib.error

DEFAULT_VOICE = "jAW0IMxOTz75sgLAYWp6"  # Desmond — gravelly
MODEL = "eleven_multilingual_v2"
API = "https://api.elevenlabs.io/v1"


def load_key():
    key = os.environ.get("ELEVENLABS_API_KEY")
    if not key:
        # fallback: archivo .env junto a este script (gitignored)
        envp = os.path.join(os.path.dirname(__file__), ".env")
        if os.path.exists(envp):
            for line in open(envp):
                line = line.strip()
                if line.startswith("ELEVENLABS_API_KEY="):
                    key = line.split("=", 1)[1].strip().strip('"').strip("'")
    if not key:
        sys.exit("ERROR: define ELEVENLABS_API_KEY (variable de entorno o tools/elevenlabs/.env)")
    return key


def req(path, key, data=None, raw=False):
    headers = {"xi-api-key": key, "Content-Type": "application/json"}
    body = json.dumps(data).encode() if data is not None else None
    r = urllib.request.Request(API + path, data=body, headers=headers)
    resp = urllib.request.urlopen(r, timeout=300)
    return resp.read() if raw else json.load(resp)


def cmd_voices(key):
    d = req("/voices", key)
    for v in d.get("voices", []):
        print(f'{v["voice_id"]}  {v.get("name")}')


def cmd_say(key, text, out, voice):
    payload = {
        "text": text,
        "model_id": MODEL,
        "language_code": "es",
        "voice_settings": {"stability": 0.55, "similarity_boost": 0.85,
                           "style": 0.25, "use_speaker_boost": True},
    }
    audio = req(f"/text-to-speech/{voice}", key, payload, raw=True)
    open(out, "wb").write(audio)
    print(f"OK -> {out} ({len(audio)} bytes, voz {voice})")


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    key = load_key()
    if sys.argv[1] == "voices":
        cmd_voices(key)
    elif sys.argv[1] == "say":
        if len(sys.argv) < 4:
            sys.exit("uso: say \"texto\" salida.mp3 [voice_id]")
        text, out = sys.argv[2], sys.argv[3]
        voice = sys.argv[4] if len(sys.argv) > 4 else DEFAULT_VOICE
        cmd_say(key, text, out, voice)
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
