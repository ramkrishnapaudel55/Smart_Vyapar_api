from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Sum
from transactions.models import Transaction
from core.authentication import CookieJWTAuthentication
from transactions.models.models_transaction import Customer
from globalparameters import globalparameters


class DashboardSummaryAPIView(APIView):

    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):

        transactions = Transaction.objects.filter(user=request.user)

        total_income = transactions.filter(
            transaction_type='INCOME'
        ).aggregate(total=Sum('amount'))['total'] or 0

        total_expense = transactions.filter(
            transaction_type='EXPENSE'
        ).aggregate(total=Sum('amount'))['total'] or 0

        profit = total_income - total_expense
        customer_count = Customer.objects.filter(user=request.user).count()

        json_response = {
            "total_income": total_income,
            "total_expense": total_expense,
            "profit": profit,
            "customer_count": customer_count,
        }

        return Response({
            globalparameters.RESULT_CODE: globalparameters.RESULT_SUCCESS_CODE,
            globalparameters.RESULT_DESCRIPTION: globalparameters.RESULT_SUCCESS_DESCRIPTION,
            globalparameters.RESULT_MESSAGE: "Dashboard summary fetched successfully",
            globalparameters.RESULT_DATA: json_response
        }, status=200)
