from django.db import models

class UploadFile(models.Model):
    file = models.FileField()
    uploaded_at = models.DateTimeField(auto_now_add=True)