from django.db import models

class FileUpload(models.Model):
    file_name = models.CharField(max_length=255)
    s3_url = models.URLField()
    upload_date = models.DateTimeField(auto_now_add=True)
