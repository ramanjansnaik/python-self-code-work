from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import BlockType, Project
from .serializers import BlockTypeSerializer, ProjectSerializer

@api_view(['GET'])
def get_block_types(request):
    blocks = BlockType.objects.all()
    serializer = BlockTypeSerializer(blocks, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def save_project(request):
    data = request.data.copy()
    data['created_by'] = request.user.id
    serializer = ProjectSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Project saved', 'project_id': serializer.data['id']})
    return Response(serializer.errors, status=400)
