from django.core.exceptions import PermissionDenied
from django.utils import timezone
from django.contrib.auth.models import User
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from volunteerapi.models import JobPosts, VolunteerUsers, CauseAreas


class JobPostUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPosts
        fields = ('id', 'user', 'cause_area', 'title', 'publication_date', 'image_url', 'content', 'approved', 'interested_volunteers', 'address',)

class UserSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField()

    def get_author_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    class Meta:
        model = User
        fields = ('author_name', 'email')

class VolunteerUserSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)  

    class Meta:
        model = VolunteerUsers
        fields = ('id', 'user',)

class CauseAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CauseAreas
        fields = ('id', 'label',)

class PostSerializer(serializers.ModelSerializer):
    user = VolunteerUserSerializer(many=False)
    cause_area = CauseAreaSerializer(many=True)
    interested_volunteers = VolunteerUserSerializer(many=True)
        # Declare that an ad-hoc property should be included in JSON
    is_owner = serializers.SerializerMethodField()

    # Function containing instructions for ad-hoc property
    def get_is_owner(self, obj,):
        # Check if the authenticated user is the owner
        return self.context['request'].user.id == obj.user.user_id

    class Meta:
        model = JobPosts
        fields = ('id', 'user', 'cause_area', 'title', 'publication_date', 'image_url', 'content', 'approved', 'interested_volunteers', 'address', 'is_owner',)


class JobPostsView(ViewSet):
    def list(self, request):
        posts = JobPosts.objects.filter(publication_date__lte=timezone.now()).order_by('-publication_date')
        serialized = PostSerializer(posts, many=True, context={'request': request})
        return Response(serialized.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        try:
            single_post = JobPosts.objects.get(pk=pk)
            post_serialized = PostSerializer(single_post, context={'request': request})
            return Response(post_serialized.data)
        except JobPosts.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        title = request.data.get('title')
        address = request.data.get('address')
        image_url = request.data.get('image_url')
        content = request.data.get('content')

        post = JobPosts.objects.create(
            user=request.user.volunteerusers,
            title=title,
            address = address,
            image_url=image_url,
            content=content,
            )

        cause_ids = request.data.get('cause_area', [])
        post.cause_area.set(cause_ids)

        volunteer_ids = request.data.get('interested_volunteers', [])
        post.interested_volunteers.set(volunteer_ids)

        serializer = PostSerializer(post, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        try:
            post = JobPosts.objects.get(pk=pk)
            serializer = JobPostUpdateSerializer(post, data=request.data, context={'request': request})
            if serializer.is_valid():
                post.title = serializer.validated_data['title']
                post.image_url = serializer.validated_data['image_url']
                post.category_id = serializer.validated_data['address']
                post.content = serializer.validated_data['content']
                post.approved = serializer.validated_data['approved']
                post.save()

                cause_ids = request.data.get('cause_area', [])
                post.cause_area.set(cause_ids)

                volunteer_ids = request.data.get('interested_volunteers', [])
                post.interested_volunteers.set(volunteer_ids)

                serializer = JobPostUpdateSerializer(post, context={'request': request})
                return Response(None, status.HTTP_204_NO_CONTENT)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except JobPosts.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        try:
            post = JobPosts.objects.get(pk=pk)
            if request.user.volunteerusers.id != post.user_id:
                raise PermissionDenied("You do not have permission to delete this post.")
            post.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except JobPosts.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
