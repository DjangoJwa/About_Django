from django.contrib.auth.signals import user_logged_in
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework_jwt.utils import jwt_payload_handler
from rest_framework_jwt.utils import jwt
from users.serializers import UserSerializer
from users.models import User
from auth import settings

# Create your views here.
class CreateUserAPIView(APIView):
    # 모든 유저의 url 접근 허용
    permission_classes = (AllowAny, )

    def post(self, request):
        user = request.data
        serializer = UserSerializer(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([AllowAny, ])
def authenticate_user(request):
    try:
        username = request.data['username']
        password = request.data['password']

        user = User.objects.get(username=username, password=password)
        if user:
            try:
                payload = jwt_payload_handler(user)
                token = jwt.encode(payload, settings.SECRET_KEY)
                user_details = {}
                user_details['name'] = "%s" % (user.name)
                user_details['token'] = token
                user_logged_in.send(sender=user.__class__, request=request, user=user)
                return Response(user_details, status=status.HTTP_200_OK)
            except Exception as e:
                raise e
        else:
            res = {'error': 'Cant authenticate with the given credentials or the account has been deactivated'}
            return Response(res, status=status.HTTP_403_FORBIDDEN)
    except KeyError:
        res = {'error': 'plz provide a email and a password'}
        return Response(res)