from django.utils.timezone import datetime
from transactions.models import Customer, Transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum
from core.authentication import CookieJWTAuthentication
from core import permissions
from globalparameters import globalparameters


class MonthlyReportAPIView(APIView):

    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):

        month = request.GET.get('month')
        year = request.GET.get('year')

        transactions = Transaction.objects.filter(
            user=request.user,
            date__month=month,
            date__year=year
        )

        income = transactions.filter(
            transaction_type='INCOME'
        ).aggregate(total=Sum('amount'))['total'] or 0

        expense = transactions.filter(
            transaction_type='EXPENSE'
        ).aggregate(total=Sum('amount'))['total'] or 0

        profit = income - expense

        json_response = {
            "month": month,
            "year": year,
            "income": income,
            "expense": expense,
            "profit": profit
        }

        return Response(
            {
                globalparameters.RESULT_CODE: globalparameters.RESULT_SUCCESS_CODE,
                globalparameters.RESULT_DESCRIPTION: globalparameters.RESULT_SUCCESS_DESCRIPTION,
                globalparameters.RESULT_MESSAGE: "Monthly report fetched successfully",
                globalparameters.RESULT_DATA: json_response
            },
            status=200
        )
