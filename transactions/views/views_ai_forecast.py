
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from core.authentication import CookieJWTAuthentication
from core.permissions import IsAuthenticated
from ollama import chat
from transactions.models import Transaction
from datetime import timedelta
from django.utils.timezone import now
from globalparameters import globalparameters

def calculate_accuracy(predicted, actual):
    errors = []
    for key in ["predicted_income", "predicted_expense", "predicted_profit"]:
        if actual[key] != 0:
            errors.append(abs(predicted[key] - actual[key]) / actual[key])
        else:
            errors.append(0)

    accuracy = 100 - (sum(errors) / len(errors) * 100)
    return max(0, round(accuracy, 2))


def get_forecast_from_model(model_name, prompt_text):
    try:
        response = chat(
            model=model_name,
            messages=[{"role": "user", "content": prompt_text}],
            options={"think": False}
        )
        ai_content = response["message"]["content"]

        clean_content = ai_content.strip()
        if clean_content.startswith("```"):
            clean_content = clean_content.replace("```json", "").replace("```", "").strip()
        return json.loads(clean_content)

    except Exception:
        return {
            "predicted_income": 0,
            "predicted_expense": 0,
            "predicted_profit": 0,
            "trend": "stable",
            "growth_percentage": 0,
            "confidence": "low",
            "advice": f"{model_name} response parsing failed."
        }


class AIForecastAPIView(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # Get last 6 months transactionss
        six_months_ago = now().date() - timedelta(days=180)

        qs = Transaction.objects.filter(
            user=user,
            date__gte=six_months_ago
        ).order_by("date")

        print(qs.count())

        # Monthly summary
        data_summary = {}

        for t in qs:
            month_key = t.date.strftime("%Y-%m")

            if month_key not in data_summary:
                data_summary[month_key] = {
                    "income": 0,
                    "expense": 0
                }

            if t.transaction_type == "INCOME":
                data_summary[month_key]["income"] += float(t.amount)
            else:
                data_summary[month_key]["expense"] += float(t.amount)

        # If no data found
        if not data_summary:
            return Response({
                "forecast": {
                    "predicted_income": 0,
                    "predicted_expense": 0,
                    "predicted_profit": 0,
                    "trend": "stable",
                    "growth_percentage": 0,
                    "confidence": "low",
                    "advice": "Not enough transaction data available for forecasting."
                }
            })

        # Sort months
        months_sorted = sorted(data_summary.keys())
        if len(months_sorted) < 2:
            return Response({
                "forecast": {
                    "predicted_income": 0,
                    "predicted_expense": 0,
                    "predicted_profit": 0,
                    "trend": "stable",
                    "growth_percentage": 0,
                    "confidence": "low",
                    "advice": "Not enough data for backtesting."
                }
            })

        # Prepare historical data for backtesting (all months except last)
        historical_summary = {m: data_summary[m] for m in months_sorted[:-1]}
        actual_next_month = {
            "predicted_income": data_summary[months_sorted[-1]]["income"],
            "predicted_expense": data_summary[months_sorted[-1]]["expense"],
            "predicted_profit": data_summary[months_sorted[-1]]["income"] - data_summary[months_sorted[-1]]["expense"]
        }


        prompt_lines = [
            "You are a financial business analytics AI.",
            "Analyze the monthly business data and predict next month's performance.",
            "Return ONLY valid JSON in the following format:",
            "{",
            "  \"predicted_income\": number,",
            "  \"predicted_expense\": number,",
            "  \"predicted_profit\": number,",
            "  \"trend\": \"up\" | \"down\" | \"stable\",",
            "  \"growth_percentage\": number,",
            "  \"confidence\": \"low\" | \"medium\" | \"high\",",
            "  \"advice\": string",
            "}",
            "",
            "Business Data:"
        ]

        for month, values in sorted(data_summary.items()):
            prompt_lines.append(
                f"{month}: income {values['income']} expense {values['expense']}"
            )

        prompt_text = "\n".join(prompt_lines)

        print("AI Prompt:", prompt_text)


        try:
            models = {
                "llama_forecast": "llama3.2:3b",
                "deepseek_forecast": "deepseek-r1:1.5b",
                "vicuna_forecast": "vicuna:13b",
                "gpt4all_forecast": "gpt4all"
            }   

            forecast_data = {}
            model_accuracies = {}

            for key, model_name in models.items():
                # forecast_data[key] = get_forecast_from_model(model_name, prompt_text)
                forecast = get_forecast_from_model(model_name, prompt_text)
                forecast_data[key] = forecast
                model_accuracies[key] = calculate_accuracy(forecast, actual_next_month)

            best_model_name = max(model_accuracies, key=model_accuracies.get)
            best_forecast = forecast_data[best_model_name]

            print("AI Raw Response: ", forecast_data)

        except Exception as e:
            json_response = {
                "error": "AI service error",
                "details": str(e)
            }
            return Response({
                globalparameters.RESULT_CODE: globalparameters.RESULT_ERROR_CODE,
                globalparameters.RESULT_DESCRIPTION: globalparameters.RESULT_ERROR_DESCRIPTION,
                globalparameters.RESULT_MESSAGE: "Failed to get forecast from AI service",
                globalparameters.RESULT_DATA: json_response
            }, status=500)
        
        json_response = {
            "best_model": best_model_name,
            "forecast": best_forecast,
            "accuracy_percent": model_accuracies[best_model_name],
            "all_models_forecast": forecast_data,
            "input_summary": data_summary
        }

        return Response({
            globalparameters.RESULT_CODE: globalparameters.RESULT_SUCCESS_CODE,
            globalparameters.RESULT_DESCRIPTION: globalparameters.RESULT_SUCCESS_DESCRIPTION,
            globalparameters.RESULT_MESSAGE: "Forecast generated successfully",
            globalparameters.RESULT_DATA: json_response
        }, status=200)
           
