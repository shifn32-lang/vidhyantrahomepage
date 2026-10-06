from django.contrib.auth import authenticate, login, logout
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from myapp.models import ContactInquiry, NewsletterSubscriber

SERVICES = {
    'ai-subscription': 'AI Model Subscription',
    'meta-ads': 'Meta Advertising',
    'google-ads': 'Google Advertising',
    'youtube-ads': 'YouTube Advertising',
    'seo': 'Search Engine Optimization',
    'smo': 'Social Media Optimization',
    'website': 'Custom Web Development',
    'school-erp': 'School ERP System',
    'lms': 'Learning Management System',
    'edu-website': 'Educational Portal',
}

MAX_LOGIN_FAILURES = 5
LOGIN_LOCK_SECONDS = 600


def home(request):
    return render(request, 'index.html')


def _client_ip(request):
    return request.META.get('REMOTE_ADDR', 'unknown')


def _valid_email(value):
    try:
        validate_email(value)
    except ValidationError:
        return False
    return True


@require_POST
def contact_submit(request):
    name = request.POST.get('name', '').strip()[:150]
    email = request.POST.get('email', '').strip()
    phone = request.POST.get('phone', '').strip()[:30]
    service = request.POST.get('service', '').strip()
    message = request.POST.get('message', '').strip()

    if not (name and message and service) or not _valid_email(email):
        return JsonResponse({'ok': False, 'error': 'Please fill in all required fields with a valid email.'}, status=400)

    ContactInquiry.objects.create(
        name=name, email=email, phone=phone,
        service=SERVICES.get(service, service[:100]), message=message,
    )
    return JsonResponse({'ok': True})


@require_POST
def newsletter_submit(request):
    email = request.POST.get('email', '').strip()
    if not _valid_email(email):
        return JsonResponse({'ok': False, 'error': 'Please enter a valid email address.'}, status=400)
    NewsletterSubscriber.objects.get_or_create(email=email.lower())
    return JsonResponse({'ok': True})


@require_POST
def login_submit(request):
    key = f'login-fail-{_client_ip(request)}'
    if cache.get(key, 0) >= MAX_LOGIN_FAILURES:
        return JsonResponse({'ok': False, 'error': 'Too many attempts. Please try again in a few minutes.'}, status=429)

    email = request.POST.get('email', '').strip().lower()
    user = authenticate(request, username=email, password=request.POST.get('password', ''))
    if user is None or not user.is_staff:
        cache.set(key, cache.get(key, 0) + 1, LOGIN_LOCK_SECONDS)
        return JsonResponse({'ok': False, 'error': 'Incorrect email or password.'}, status=401)

    cache.delete(key)
    login(request, user)
    return JsonResponse({'ok': True, 'redirect': '/admin/'})


def logout_view(request):
    logout(request)
    return redirect('home')
