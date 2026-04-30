from transactions.models import Customer, Transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum
from core.authentication import CookieJWTAuthentication
from core import permissions


class CustomerDueListAPIView(APIView):

    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):

        customers = Customer.objects.filter(user=request.user)

        result = []

        for customer in customers:

            transactions = Transaction.objects.filter(
                customer=customer,
                user=request.user
            )

            income = transactions.filter(
                transaction_type='INCOME'
            ).aggregate(total=Sum('amount'))['total'] or 0

            expense = transactions.filter(
                transaction_type='EXPENSE'
            ).aggregate(total=Sum('amount'))['total'] or 0

            due = income - expense

            result.append({
                "customer_id": customer.reference_id,
                "customer_name": customer.name,
                "due_balance": due
            })

        return Response(result)
