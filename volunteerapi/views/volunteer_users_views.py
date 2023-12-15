from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from django.contrib.auth.models import User
from volunteerapi.models import VolunteerUsers, CauseAreas, JobPosts


class VolunteerUsersView(ViewSet):
    """View set for volunteer_users"""

    def retrieve(self, request, pk=None):
        """Handle GET requests for single game

        Returns:
            Response -- JSON serialized game instance
        """
        try:
            volunteer_user = VolunteerUsers.objects.get(pk=pk)
            serialized = VolunteerUsersSerializer(volunteer_user)
            return Response(serialized.data)
        except VolunteerUsers.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


    def list(self, request):
        """Handle GET requests to volunteer_users resource

        Returns:
            Response -- JSON serialized list of volunteer_users
        """
        try:
            volunteer_users = VolunteerUsers.objects.all()
            serialized = VolunteerUsersSerializer(volunteer_users, many=True)
            return Response(serialized.data)
        except VolunteerUsers.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


    def update(self, request, pk=None):
        try:
            volunteer = VolunteerUsers.objects.get(pk=pk)
            serializer = UpdateVolunteerUsersSerializer(volunteer, data=request.data, context={'request': request})
            if serializer.is_valid():
                volunteer.user = serializer.validated_data['user']
                volunteer.bio = serializer.validated_data['bio']
                volunteer.profile_image_url = serializer.validated_data['profile_image_url']
                volunteer.save()
                cause_area_data = request.data.get('cause_area', [])
                volunteer.cause_area.set(cause_area_data)
                favorite_data = request.data.get('favorite', [])
                volunteer.favorite.set(favorite_data)
                serializer = UpdateVolunteerUsersSerializer(volunteer, context={'request': request})
                return Response(None, status.HTTP_204_NO_CONTENT)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except VolunteerUsers.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)



class UserVolunteerUsersSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()

    def get_email(self, obj):
        return f'{obj.username}'

    def get_full_name(self, obj):
        return f'{obj.first_name} {obj.last_name}'

    class Meta:
        model = User
        fields = ('id', 'full_name', 'email', 'username')

class FavoritesVolunteerUsersSerializer(serializers.ModelSerializer):

    class Meta:
        model = JobPosts
        fields = ('id', 'title', 'content', 'address', 'publication_date')

class CauseAreaVolunteerUsersSerializers(serializers.ModelSerializer):

    class Meta:
        model = CauseAreas
        fields = ('id', 'label')

class VolunteerUsersSerializer(serializers.ModelSerializer):
    user = UserVolunteerUsersSerializer(many=False)
    cause_area = CauseAreaVolunteerUsersSerializers(many=True)
    favorite = FavoritesVolunteerUsersSerializer(many=True)

    class Meta:
        model = VolunteerUsers
        fields = ('id', 'bio', 'profile_image_url', 'created_on', 'user', 'is_business', 'cause_area', 'favorite')

class UpdateVolunteerUsersSerializer(serializers.ModelSerializer):

    class Meta:
        model = VolunteerUsers
        fields = ('id', 'bio', 'profile_image_url', 'created_on', 'user', 'is_business', 'cause_area', 'favorite')
