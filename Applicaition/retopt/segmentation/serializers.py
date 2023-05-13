from rest_framework import serializers
from rest_framework import Transactions

class approvalTransactions(serializers.ModelSerializer):
    class Meta:
        model = Transactions
        fields = '__all__'