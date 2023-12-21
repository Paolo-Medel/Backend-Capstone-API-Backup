from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from volunteerapi.models import VolunteerUsers

@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    '''Handles the authentication of a user

    Method arguments:
      request -- The full HTTP request object
    '''
    email = request.data['email']
    password = request.data['password']

    # Use the built-in authenticate method to verify
    # authenticate returns the user object or None if no user is found
    authenticated_user = authenticate(username=email, password=password)

    # If authentication was successful, respond with their token
    if authenticated_user is not None:
        token = Token.objects.get(user=authenticated_user)
        data = {
            'valid': True,
            'token': token.key,
            'is_business': authenticated_user.volunteerusers.is_business,
            'volunteer_user_id': authenticated_user.volunteerusers.id,
            'user_id': authenticated_user.id
        }
        return Response(data)
    else:
        # Bad login details were provided. So we can't log the user in.
        data = { 'valid': False }
        return Response(data)

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    '''Handles the creation of a new gamer for authentication

    Method arguments:
      request -- The full HTTP request object
    '''

    # Create a new user by invoking the `create_user` helper method
    # on Django's built-in User model
    new_user = User.objects.create_user(
        username=request.data['email'],
        password=request.data['password'],
        first_name=request.data['first_name'],
        last_name=request.data['last_name'],
        email=request.data['email']
    )

    volunteer_user = VolunteerUsers()
    volunteer_user.user_id = new_user.id
    volunteer_user.bio = request.data.get('bio')
    volunteer_user.profile_image_url = request.data.get('profile_image_url')
    volunteer_user.is_business = request.data.get("is_business")
   # Save the VolunteerUsers object first to generate an id
    volunteer_user.save()

    # Use set() to set the many-to-many field cause_area
    cause_area_data = request.data.get("cause_area", [])
    volunteer_user.cause_area.set(cause_area_data)

    # Save the VolunteerUsers object again after setting the many-to-many field
    volunteer_user.save()
    # Use the REST Framework's token generator on the new user account
    token = Token.objects.create(user=new_user)
    # Return the token to the client
    data = {
        'valid': True,
        'token': token.key,
        'is_business': new_user.volunteerusers.is_business,
        'volunteer_user_id': new_user.volunteerusers.id, 
        'user_id': new_user.id, 
    }
    return Response(data)
