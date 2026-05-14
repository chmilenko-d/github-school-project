# myapp/views.py
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.translation import activate
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
from .models import Post, TranslationKey

LANGUAGE_SESSION_KEY = '_language'


@csrf_exempt
@require_POST
def set_language_api(request):
    try:
        data = json.loads(request.body)
        lang_code = data.get('language')
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)

    from django.conf import settings
    if lang_code and lang_code in dict(settings.LANGUAGES):
        request.session[LANGUAGE_SESSION_KEY] = lang_code
        activate(lang_code)
        response = JsonResponse({'status': 'ok', 'language': lang_code})
        response.set_cookie(
            key='django_language',
            value=lang_code,
            max_age=365 * 24 * 60 * 60,  # 1 год
            path='/',
            httponly=False
        )
        return response

    return JsonResponse({'status': 'error', 'message': 'Unsupported language'}, status=400)


@csrf_exempt
@require_POST
def increment_view(request, slug):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    post = get_object_or_404(Post, slug=slug)
    post.views += 1
    post.save(update_fields=['views'])

    return JsonResponse({'views': post.views})