from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import MultiPartParser

from .serializer import *

def home(request):
    return render(request, 'brainshare/home.html', {})

def download(request, uid):
    context = {
        'uid':uid
    }
    return render(request, 'brainshare/download.html', context)

class HandleFileUpload(APIView):
    parser_classes = [MultiPartParser]

    def post(self , request):
        try:
            data = request.data

            serializer = FileListSerializer(data = data)
        
            if serializer.is_valid():
                result = serializer.save()
                return Response({
                    'status' : 200,
                    'message' : 'files uploaded successfully',
                    'data': {
                        'files': result['files'],
                        'folder': result['folder']
                    }
                })
            
            return Response({
                'status' : 400,
                'message' : 'somethign went wrong',
                'data'  : serializer.errors
            })
        except Exception as e:
            print(e)
