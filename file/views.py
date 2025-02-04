import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from .models import UploadFile

def home(request):
    file_url = None
    message = None

    if request.method == 'POST':
        if 'create_directory' in request.POST:
            directory_name = request.POST.get('directory_name', '').strip()
            if directory_name:
                target_dir = os.path.join(settings.MEDIA_ROOT, directory_name)
                os.makedirs(target_dir, exist_ok=True)
                message = f"Directory '{directory_name}' created successfully."
            else:
                message = "Please enter a valid directory name."

        elif request.FILES.get('file'):
            uploaded_file = request.FILES['file']
            upload_directory = request.POST.get('upload_directory', '').strip()

            fs = FileSystemStorage()
            if upload_directory:
                target_dir = os.path.join(settings.MEDIA_ROOT, upload_directory)
                os.makedirs(target_dir, exist_ok=True)
                relative_path = os.path.join(upload_directory, uploaded_file.name)
                filename = fs.save(relative_path, uploaded_file)
            else:
                filename = fs.save(uploaded_file.name, uploaded_file)
            file_url = fs.url(filename)

            new_upload = UploadFile(file=filename)
            new_upload.save()
            message = f"File uploaded successfully: {file_url}"

    files = UploadFile.objects.all()
    directories = [d for d in os.listdir(settings.MEDIA_ROOT) if os.path.isdir(os.path.join(settings.MEDIA_ROOT, d))]

    return render(request, 'home.html', {'files': files, 'file_url': file_url, 'message': message, 'directories': directories})


def folder_view(request, folder_name):
    folder_path = os.path.join(settings.MEDIA_ROOT, folder_name)

    if not os.path.exists(folder_path) or not os.path.isdir(folder_path):
        return render(request, '404.html', {'message': f"Folder '{folder_name}' does not exist."})

    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        
        # Save the file inside the correct folder
        fs = FileSystemStorage(location=folder_path)
        filename = fs.save(uploaded_file.name, uploaded_file)
        file_url = f"/media/{folder_name}/{filename}"

        # Save file entry to database
        new_upload = UploadFile(file=os.path.join(folder_name, filename))
        new_upload.save()

        return redirect(f'/{folder_name}/')  # Refresh the page after upload

    # Get files in the folder
    files = UploadFile.objects.filter(file__startswith=folder_name + "/")

    return render(request, 'folder.html', {'folder_name': folder_name, 'files': files})
