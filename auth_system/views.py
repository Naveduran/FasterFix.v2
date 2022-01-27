from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer
from rest_framework.permissions import AllowAny

class UserSignUp(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        user = request.data
        serializer = UserSerializer(data=user)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, 201)

        return Response(serializer.errors, 400)