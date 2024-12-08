import os
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from .utils.utils_files import (
    process_text_file,
    process_docx_file,
    convert_text_to_audio,
    process_excel_file,
    generate_graph,
)

def upload_file(request):
    if request.method == 'POST' and request.FILES.get('document'):
        uploaded_file = request.FILES['document']
        file_extension = os.path.splitext(uploaded_file.name)[1].lower()

        # Validar formatos permitidos
        if file_extension not in ['.txt', '.docx', '.xls', '.xlsx']:
            return render(request, 'upload_form.html', {'error': 'Formato no soportado.'})

        # Guardar archivo temporalmente
        fs = FileSystemStorage()
        file_path = fs.save(uploaded_file.name, uploaded_file)
        file_absolute_path = fs.path(file_path)

        try:
            if file_extension == '.txt':
                content = process_text_file(file_absolute_path)
                audio_file_name = os.path.splitext(uploaded_file.name)[0] + ".mp3"
                audio_file_path = os.path.join(settings.MEDIA_ROOT, audio_file_name)
                convert_text_to_audio(content, audio_file_path)
                audio_url = fs.url(audio_file_name)
                return render(request, 'result.html', {'audio_url': audio_url})

            elif file_extension == '.docx':
                content = process_docx_file(file_absolute_path)
                audio_file_name = os.path.splitext(uploaded_file.name)[0] + ".mp3"
                audio_file_path = os.path.join(settings.MEDIA_ROOT, audio_file_name)
                convert_text_to_audio(content, audio_file_path)
                audio_url = fs.url(audio_file_name)
                return render(request, 'result.html', {'audio_url': audio_url})

            elif file_extension in ['.xls', '.xlsx']:
                df = process_excel_file(file_absolute_path)
                graph_file_name = os.path.splitext(uploaded_file.name)[0] + "_graph.png"
                graph_path = os.path.join(settings.MEDIA_ROOT, graph_file_name)
                generate_graph(df, graph_path)
                graph_url = fs.url(graph_file_name)
                return render(request, 'result.html', {'graph_url': graph_url})

        except Exception as e:
            return render(request, 'upload_form.html', {'error': str(e)})

        finally:
            if os.path.exists(file_absolute_path):
                os.remove(file_absolute_path)

    return render(request, 'upload_form.html')
