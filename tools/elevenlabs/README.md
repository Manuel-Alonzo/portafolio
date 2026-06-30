# ElevenLabs — tooling de voz

Integración reutilizable para generar audio con ElevenLabs (la voz **Desmond**
usada en `/motivacion`). El script **no contiene la API key**: la lee del entorno.

## Configurar la clave (una sola vez)

### Opción A — Para que esté SIEMPRE disponible (recomendado)
Añade la variable de entorno en la configuración de tu entorno de **Claude Code on the web**:

- Nombre: `ELEVENLABS_API_KEY`
- Valor: tu clave (`sk_...`)

Así cada sesión nueva ya tendrá ElevenLabs conectado automáticamente, sin pegar
la clave de nuevo. Docs: https://code.claude.com/docs/en/claude-code-on-the-web

### Opción B — Local (solo esta máquina/sesión)
Crea `tools/elevenlabs/.env` (ya está en `.gitignore`, nunca se sube):

```
ELEVENLABS_API_KEY=sk_tu_clave_aqui
```

## Uso

```bash
# Listar tus voces guardadas
python3 tools/elevenlabs/tts.py voices

# Generar audio (voz Desmond por defecto)
python3 tools/elevenlabs/tts.py say "El fracaso no existe." salida.mp3

# Con otra voz
python3 tools/elevenlabs/tts.py say "Hola" salida.mp3 <voice_id>
```

## Notas
- Voz por defecto: **Desmond** (`jAW0IMxOTz75sgLAYWp6`).
- Modelo: `eleven_multilingual_v2` (buen español).
- La clave nunca debe commitearse. Si alguna vez se expone, **revócala** en el
  panel de ElevenLabs y genera una nueva.
