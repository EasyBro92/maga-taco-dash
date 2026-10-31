# Pasa un audio o un vídeo (webm, mp3, ogg...) a WAV con Blender, que trae
# FFmpeg dentro (en este PC no hay otro programa para eso). 31/10/2026.
#
#   blender -b -P herramientas/a_wav.py -- entrada salida.wav [hz] [canales]
#
# Para whisper: 16000 Hz y un canal. Para los recortes del juego: 22050 Hz.

import sys
import aud

args = sys.argv[sys.argv.index('--') + 1:]
entrada, salida = args[0], args[1]
hz = int(args[2]) if len(args) > 2 else 16000
canales = aud.CHANNELS_MONO if (len(args) < 4 or args[3] == '1') else aud.CHANNELS_STEREO
s = aud.Sound(entrada).resample(hz, True).rechannel(1 if canales == aud.CHANNELS_MONO else 2)
s.write(salida, rate=hz, channels=canales, format=aud.FORMAT_S16, container=aud.CONTAINER_WAV, codec=aud.CODEC_PCM)
print('WAV', salida, flush=True)
