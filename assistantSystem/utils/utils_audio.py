from django.conf import settings
from django.core.files.storage.filesystem import FileSystemStorage
from django.shortcuts import render
from django.http import JsonResponse
from google.cloud import speech
from google.cloud import texttospeech
from googleapiclient.discovery import build
import os
from env_apis import custom_search

def voice_search(request):
    if request.method == 'POST':
        # Recibir el audio del cliente
        audio_file = request.FILES.get('audio')
        
        if not audio_file:
            return JsonResponse({'error': 'No se recibió archivo de audio'}, status=400)

        # Convertir audio a texto
        client = speech.SpeechClient()
        audio = speech.RecognitionAudio(content=audio_file.read())
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code="es-ES",
        )
        response = client.recognize(config=config, audio=audio)
        
        if not response.results:
            return JsonResponse({'error': 'No se pudo reconocer el audio'}, status=400)

        text = response.results[0].alternatives[0].transcript

        # Realizar búsqueda en Google
        service = build("customsearch", "v1", developerKey=custom_search)
        res = service.cse().list(q=text, cx='TU_SEARCH_ENGINE_ID').execute()
        
        if 'items' not in res:
            return JsonResponse({'error': 'No se encontraron resultados'}, status=400)

        search_result = res['items'][0]['snippet']

        # Convertir resultado a audio
        client = texttospeech.TextToSpeechClient()
        synthesis_input = texttospeech.SynthesisInput(text=search_result)
        voice = texttospeech.VoiceSelectionParams(
            language_code="es-ES", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
        )
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )
        response = client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )

        # Guardar el audio resultante
        audio_file_name = "search_result.mp3"
        audio_file_path = os.path.join(settings.MEDIA_ROOT, audio_file_name)
        with open(audio_file_path, "wb") as out:
            out.write(response.audio_content)

        audio_url = FileSystemStorage().url(audio_file_name)

        return JsonResponse({'audio_url': audio_url})

    return render(request, 'voice_search.html')