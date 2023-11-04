from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Tender, TenderApplication
from .serializers import TenderSerializer, TenderApplicationSerializer

class TenderViewSet(viewsets.ModelViewSet):
    queryset = Tender.objects.all()
    serializer_class = TenderSerializer

    def get_serializer_context(self):
        context = super(TenderViewSet, self).get_serializer_context()
        context['user'] = self.request.user
        return context


class TenderApplicationViewSet(viewsets.ModelViewSet):
    queryset = TenderApplication.objects.all()
    serializer_class = TenderApplicationSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user
        return context
    
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        queryset = self.queryset.filter(customer=self.request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def partial_update(self, request, pk=None):
        instance = self.queryset.get(pk=pk)
        if instance.tender.customer == request.user:
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                # Принимаем заявку и добавляем контрактора в поле contractors
                if not instance.is_accepted:
                    tender = instance.tender
                    tender.contractors.add(instance.applicant)
                    instance.is_accepted = True
                    instance.save()
                else:
                    return Response('Заявка уже была принята')
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response("You don't have permission to update this application.", status=status.HTTP_403_FORBIDDEN)