from rest_framework.decorators import api_view,permission_classes,authentication_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import PhotoSerializer,RepoSerializer
from .models import Photo, Repo
from .workings.middleMan import MiddleMan
from rest_framework.response import Response
from django.http import HttpResponse


thumbnails_store={}
originals_store={}


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def getPhotos(request):
    user=request.user
    photos=Photo.objects.filter(user=user)
    serializer=PhotoSerializer(photos,many=True)
    return Response(serializer.data)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def upload(request):
    user=request.user
    m=MiddleMan(user.username)
    files = request.FILES.getlist('files')
    result=[]
    for file in files:
        try:
            uname,repo,fileContent=m.upload_file(file) # this filecontent is un important for logic
            if repo:
                photoSerializer=PhotoSerializer(data={'oname':file.name,'uname':uname,'size':file.size})
                if photoSerializer.is_valid():
                    photo=photoSerializer.save(user=user)
                    result.append(photoSerializer.data)
                    repoSerializer=RepoSerializer(data={'photo':photo.id,'repo':repo})
                    if repoSerializer.is_valid():
                        repoSerializer.save()
                        originals_store[photo.id]=fileContent   # this line is un important for logic
                    else:
                        return Response(repoSerializer.errors)
                else:
                    return Response(photoSerializer.errors)
        except Exception as e:
            print(e)
    return Response(result)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def download(request,id):
    user=request.user
    photo=Photo.objects.get(id=id,user=user)
    if photo and id in originals_store: # this is un important for logic
        content=originals_store[id]   # this is un important for logic
        print('present in temp variable')
    else:
        print('downloading from git')
        repo=Repo.objects.get(photo=photo)
        m=MiddleMan(user.username)
        content=m.download_file(photo.uname,repo.repo)
        originals_store[id]=content      # this is un important for logic
    response = HttpResponse(content, content_type='application/octet-stream')
    return response


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def getAThumbnail(request,uname):
    global thumbnails_store
    user=request.user
    if uname in thumbnails_store:# this is un important for logic
        print('thumbnails present in temp variable')
    else:
        print('fetching all thumbnails from git')
        m=MiddleMan(user.username)
        m.thumbnails(thumbnails_store)
    response = HttpResponse(thumbnails_store[uname], content_type='application/octet-stream')
    return response 



@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def getThumbnailsReady(request):
    global thumbnails_store
    user=request.user
    m=MiddleMan(user.username)
    m.thumbnails(thumbnails_store)
    return Response('im ready') 