from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Tender(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=100)
    created_date = models.DateTimeField()
    start_date = models.DateTimeField()
    warranty_type = models.CharField(max_length=100)
    bill_doc = models.CharField(max_length=100)
    tender_name = models.CharField(max_length=100)
    tender_format = models.CharField(max_length=100)
    amount_price = models.DecimalField(max_digits=10, decimal_places=2)
    contractors = models.ManyToManyField(User, related_name='tenders', null=True, blank=True)
    closed_date = models.DateTimeField()
    quality = models.CharField(max_length=100)
    warranty_coverage = models.IntegerField()
    packaging = models.CharField(max_length=100)
    insurance = models.BooleanField(default=False)
    related_service = models.BooleanField(default=False)
    banking_support = models.BooleanField(default=False)
    inspection = models.CharField(max_length=100)
    warranty = models.CharField(max_length=100)
    needed_docs = models.CharField(max_length=100)
    dispute_resolution = models.CharField(max_length=100)
    protocol = models.BigIntegerField()
    advance_payment = models.IntegerField()
    after_shipment = models.IntegerField()
    receive = models.IntegerField()
    payment_date = models.DateTimeField()
    forfeitures_day = models.FloatField()
    forfeitures_max = models.FloatField()

    def __str__(self):
        return self.tender_name



class TenderApplication(models.Model):
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applicationser')
    tender = models.ForeignKey(Tender, on_delete=models.CASCADE, related_name='applications')
    is_accepted = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ['applicant', 'tender']