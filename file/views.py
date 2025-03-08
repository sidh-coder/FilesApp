import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from .models import UploadFile
from django.contrib.auth.decorators import login_required
from accounts.forms import CustomUserCreationForm
from django.contrib.auth import login

@login_required
def home(request):
    # (existing code)
    # We'll modify file paths to use the logged-in user’s folder.
    file_url = None
    message = None
    user_folder = request.user.username  # Use username to name the directory

    if request.method == 'POST':
        if 'create_directory' in request.POST:
            directory_name = request.POST.get('directory_name', '').strip()
            if directory_name:
                # Create the directory inside the user's folder.
                target_dir = os.path.join(settings.MEDIA_ROOT, user_folder, directory_name)
                os.makedirs(target_dir, exist_ok=True)
                message = f"Directory '{directory_name}' created successfully."
            else:
                message = "Please enter a valid directory name."

        elif request.FILES.get('file'):
            uploaded_file = request.FILES['file']
            upload_directory = request.POST.get('upload_directory', '').strip()
            fs = FileSystemStorage()
            if upload_directory:
                target_dir = os.path.join(settings.MEDIA_ROOT, user_folder, upload_directory)
                os.makedirs(target_dir, exist_ok=True)
                relative_path = os.path.join(user_folder, upload_directory, uploaded_file.name)
                filename = fs.save(relative_path, uploaded_file)
            else:
                target_dir = os.path.join(settings.MEDIA_ROOT, user_folder)
                os.makedirs(target_dir, exist_ok=True)
                relative_path = os.path.join(user_folder, uploaded_file.name)
                filename = fs.save(relative_path, uploaded_file)
            file_url = fs.url(filename)
            new_upload = UploadFile(file=filename)
            new_upload.save()
            message = f"File uploaded successfully: {file_url}"

    # Filter files for the current user only.
    files = UploadFile.objects.filter(file__startswith=user_folder + "/")
    # List directories under the user's folder.
    user_media_root = os.path.join(settings.MEDIA_ROOT, user_folder)
    directories = []
    if os.path.exists(user_media_root):
        directories = [d for d in os.listdir(user_media_root) if os.path.isdir(os.path.join(user_media_root, d))]
    
    return render(request, 'home.html', {
        'files': files,
        'file_url': file_url,
        'message': message,
        'directories': directories
    })


@login_required
@login_required
def folder_view(request, folder_path):
    user_folder = request.user.username
    # Build the full filesystem path for the folder
    full_folder_path = os.path.join(settings.MEDIA_ROOT, user_folder, folder_path)

    if not os.path.exists(full_folder_path) or not os.path.isdir(full_folder_path):
        return render(request, '404.html', {'message': f"Folder '{folder_path}' does not exist."})

    message = None

    # Check if the user is trying to create a new directory
    if request.method == 'POST':
        if 'create_directory' in request.POST:
            directory_name = request.POST.get('directory_name', '').strip()
            if directory_name:
                new_folder_path = os.path.join(full_folder_path, directory_name)
                os.makedirs(new_folder_path, exist_ok=True)
                message = f"Directory '{directory_name}' created successfully."
            else:
                message = "Please provide a valid folder name."
        elif request.FILES.get('file'):
            # Handle file upload as before
            uploaded_file = request.FILES['file']
            fs = FileSystemStorage(location=full_folder_path)
            filename = fs.save(uploaded_file.name, uploaded_file)
            new_upload = UploadFile(file=os.path.join(user_folder, folder_path, filename))
            new_upload.save()
            message = f"File '{uploaded_file.name}' uploaded successfully."
            return redirect(f'/{folder_path}/')

    # Filter files that are stored in this nested folder
    files = UploadFile.objects.filter(file__startswith=f'{user_folder}/{folder_path}/')

    # List subfolders inside this folder
    subfolders = []
    for item in os.listdir(full_folder_path):
        item_full_path = os.path.join(full_folder_path, item)
        if os.path.isdir(item_full_path):
            subfolders.append(item)

    return render(request, 'folder.html', {
        'folder_path': folder_path,
        'files': files,
        'subfolders': subfolders,
        'message': message
    })
