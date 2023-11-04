from rest_framework import serializers
from .models import Tender, TenderApplication

class TenderSerializer(serializers.ModelSerializer):
    lots = serializers.SerializerMethodField()

    class Meta:
        model = Tender
        fields = '__all__'
        read_only_fields = ('customer', 'contractors')
    

    def get_lots(self, obj):
        customer = obj.customer  # Получаем кастомера текущего тендера
        if customer:
            return [tender.tender_name for tender in Tender.objects.filter(customer=customer).exclude(id=obj.id)]
        return []
    
    def create(self, validated_data):
        user = self.context.get('user')
        if user:
            validated_data['customer'] = user
        return super().create(validated_data)
    


class TenderApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TenderApplication
        fields = '__all__'
        read_only_fields = ('is_accepted', 'applicant', 'customer')

    def create(self, validated_data):
        user = self.context.get('user')
        tender = validated_data.get('tender')
        if user and tender:
            customer = tender.customer
            application = TenderApplication.objects.create(applicant=user, customer=customer, **validated_data)
            return application
        return None
