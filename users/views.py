from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from djoser.views import UserViewSet as DjoserViewSet
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from .models import User  
from .serializers import SetRatingSerializer



class CustomUserViewSet(DjoserViewSet):
    def get_permissions(self):
        if self.action == 'create_contractor':
            return [AllowAny()]
        return super().get_permissions()
    
    @swagger_auto_schema(operation_summary='Регистрация контракторов', operation_description='This endpoint is used for creating a new contractor user')
    @action(detail=False, methods=["POST"])
    def create_contractor(self, request):
        data = request.data.copy()
        data["is_contractor"] = True
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save()
    


class SetUserRating(APIView):

    @swagger_auto_schema(
        operation_summary="Обновление рейтинга пользователя",
        operation_description="Установите рейтинг для пользователя",
        request_body=SetRatingSerializer,
        responses={
            201: openapi.Response(description="Рейтинг успешно установлен", schema=SetRatingSerializer),
            404: "Пользователь не найден",
            400: "Неверный запрос"
        },
    )
    def post(self, request, user_id):
        """
        Установите рейтинг для пользователя. 
        """
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = SetRatingSerializer(data=request.data)

        if serializer.is_valid():
            new_rating = serializer.validated_data["rating"]

            user.total_rating += new_rating
            user.rating_votes += 1
            user.rating = round(user.total_rating / user.rating_votes, 1)  

            user.save()

            return Response({"rating": user.rating}, status=status.HTTP_201_CREATED)