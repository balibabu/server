from rest_framework.decorators import api_view,permission_classes,authentication_classes
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
from django.contrib.auth import logout
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication


############# clipboard syncronization #################
clips={}
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def sync_clip(request):
    user = request.user
    latest_clip=request.data.get('clip','')
    old_clip=''
    if user.id in clips:
        old_clip=clips[user.id]
    clips[user.id]=latest_clip
    return Response(old_clip)


import random
from django.http import HttpResponse
in_memory_files = {}

@api_view(['POST', 'GET'])
def file_share(request):
    if request.method == 'POST':
        file = request.FILES.get('file')
        if file:
            key = str(random.randint(1,9))+str(len(in_memory_files))+str(random.randint(1,9))
            in_memory_files[key] = (file.name, file.read())
            return Response(key)
        else:
            return Response('No file received')
    elif request.method == 'GET':
        key = request.query_params.get('key', '')
        if key in in_memory_files:
            filename, file_content = in_memory_files[key]
            response = HttpResponse(file_content,content_type='application/octet-stream')
            response['Content-Disposition'] = filename
            response['Access-Control-Expose-Headers'] = 'Content-Disposition'
            return response
        return Response('No file found')



# import os
# from pathlib import Path
# from datetime import datetime
# from django.http import HttpResponseNotFound
# BASE_DIR = Path(__file__).resolve().parent.parent

# @api_view(['GET'])
# def db_backup(request):
#     db_path = os.path.join(BASE_DIR, 'db.sqlite3')
#     if not os.path.exists(db_path):
#         return HttpResponseNotFound("Database file not found.")
#     with open(db_path, 'rb') as db_file:
#         response = HttpResponse(db_file,content_type='application/octet-stream')
#         response['Content-Disposition'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")+'.sqlite3'
#         response['Access-Control-Expose-Headers'] = 'Content-Disposition'
#         return response
