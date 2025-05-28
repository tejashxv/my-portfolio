from django.shortcuts import render
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .models import ContactQuery  
from django.contrib import messages

# Create your views here.

def index(request):
    if request.method == 'POST':
        name = request.POST.get('NAME', '').strip()
        email = request.POST.get('EMAIL', '').strip()
        subject = request.POST.get('SUBJECT', 'No Subject').strip()
        message = request.POST.get('MESSAGE', '').strip()

        if not name or not email or not message:
            messages.error(request, "Name, email, and message are required.")
            return render(request, 'home/index.html')

        try:
        
            ContactQuery.objects.create(
                name=name,
                email=email,
                subject=subject,
                message=message
            )

            full_message = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
            send_mail(
                subject,
                full_message,
                settings.EMAIL_HOST_USER,
                [settings.EMAIL_HOST_USER],
                fail_silently=False,
            )
            messages.success(request, "Email sent successfully!")

        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")

    return render(request, 'home/index.html')


