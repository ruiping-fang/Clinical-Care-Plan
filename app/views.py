from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
import os

from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


DATA_STORE = {}

def index(request):
    return render(request, "index.html")


@csrf_exempt
def generate_careplan(request):
    if request.method == "POST":
        body = json.loads(request.body)

        patient_name = body.get("name")
        diagnosis = body.get("diagnosis")
        medication = body.get("medication")
        history = body.get("history")

        prompt = f"""
You are a clinical pharmacist.
Generate a care plan for:

Patient: {patient_name}
Diagnosis: {diagnosis}
Medication: {medication}
History: {history}

Output must include:
- Problem list
- Goals
- Pharmacist interventions
- Monitoring plan
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a clinical pharmacist assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )

        careplan = response.choices[0].message.content


        DATA_STORE[patient_name] = {
            "diagnosis": diagnosis,
            "medication": medication,
            "careplan": careplan
        }

        return JsonResponse({"careplan": careplan})

    return JsonResponse({"error": "Invalid request"})