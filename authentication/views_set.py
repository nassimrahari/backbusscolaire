
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from transport_scolaire.serializers import UserSerializer


class TokenCheckView(APIView):
    # permission_classes = [IsAuthenticated]
    user_serializer = UserSerializer  # Remplacez UserSerializer par votre propre sérialiseur d'utilisateur

    def get(self, request):
        serialized_user = self.user_serializer(request.user).data
        return Response({'token': 'Token is valid', 'user': serialized_user})