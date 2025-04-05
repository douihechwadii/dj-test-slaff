import os
from django.http import JsonResponse
from django.conf import settings
from dinar.scripts.flous import *

def run(request):
    file_path = os.path.join(settings.BASE_DIR, "dinar", "logs", "test.txt")
    
    
    if not os.path.exists(file_path):
        return JsonResponse({"error": "Log file not found", "status": "failure"})
    
    result = convert_logs_to_json(file_path)
    return JsonResponse(result, safe=False)