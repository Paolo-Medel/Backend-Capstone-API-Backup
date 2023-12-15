from rest_framework import viewsets, serializers, status
from rest_framework.response import Response
from volunteerapi.models import CauseAreas

class CauseAreaSerializer(serializers.ModelSerializer):

    class Meta:
        model = CauseAreas
        fields = ('id', 'label',)

class CauseAreaView(viewsets.ViewSet):

    def list(self, request):
        cause_areas = CauseAreas.objects.all().order_by('label')
        serialized = CauseAreaSerializer(cause_areas, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk=None):
        try:
            cause_areas = CauseAreas.objects.get(pk=pk)
            serialized = CauseAreaSerializer(cause_areas)
            return Response(serialized.data, status=status.HTTP_200_OK)
        except CauseAreas.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
