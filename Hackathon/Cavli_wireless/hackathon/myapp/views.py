from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.core.files.storage import default_storage
from django.conf import settings

from .models import FileUpload
import boto3
import json

@csrf_exempt
@require_POST
def upload_file(request):
    if request.method == 'POST' and request.FILES['file']:
        uploaded_file = request.FILES['file']
        file_name = uploaded_file.name

        # Upload the file to AWS S3
        s3 = boto3.client('s3', 
                          aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                          region_name=settings.AWS_S3_REGION_NAME)

        s3.upload_fileobj(uploaded_file, settings.AWS_STORAGE_BUCKET_NAME, file_name)

        # Get the S3 URL
        s3_url = f'https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/{file_name}'

        # Save file information to MongoDB
        file_info = FileUpload(file_name=file_name, s3_url=s3_url)
        file_info.save()

        response_data = {
            'file_name': file_name,
            's3_url': s3_url,
            'upload_date': file_info.upload_date.strftime('%Y-%m-%d %H:%M:%S')
        }

        return JsonResponse(response_data)
    else:
        return JsonResponse({'error': 'Invalid request'})

def get_file_info(request, file_id):
    try:
        file_info = FileUpload.objects.get(pk=file_id)
        response_data = {
            'file_name': file_info.file_name,
            's3_url': file_info.s3_url,
            'upload_date': file_info.upload_date.strftime('%Y-%m-%d %H:%M:%S')
        }
        return JsonResponse(response_data)
    except FileUpload.DoesNotExist:
        return JsonResponse({'error': 'File not found'})
