from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from datetime import timedelta

client = None

SYSTEM_PROMPT = "شما یک دستیار پزشکی هستید که به صورت خلاصه و غیر قطعی پاسخ می‌دهید."

RATE_LIMIT = 10
PERIOD = timedelta(hours=1)


def _check_rate_limit(session):
    start = session.get('chat_ts')
    count = session.get('chat_count', 0)
    now = timezone.now()
    if not start or now - timezone.datetime.fromisoformat(start) >= PERIOD:
        session['chat_ts'] = now.isoformat()
        session['chat_count'] = 0
        return 0
    return count


def chat_page(request):
    request.session.setdefault('chat_history', [])
    return render(request, 'chat.html')


def chat_send(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'invalid method'}, status=400)

    message = request.POST.get('message', '').strip()
    if not message:
        return JsonResponse({'error': 'empty'}, status=400)

    count = _check_rate_limit(request.session)
    if count >= RATE_LIMIT:
        return JsonResponse({'error': 'limit'}, status=429)

    history = request.session.get('chat_history', [])
    history.append({'role': 'user', 'content': message})
    messages = [{'role': 'system', 'content': SYSTEM_PROMPT}] + history

    if settings.OPENAI_API_KEY:
        try:
            import openai
            client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
            completion = client.chat.completions.create(model='gpt-4o', messages=messages)
            reply = completion.choices[0].message.content.strip()
        except Exception:
            reply = 'خطایی رخ داد.'
    else:
        reply = 'مدل در دسترس نیست.'

    history.append({'role': 'assistant', 'content': reply})
    request.session['chat_history'] = history
    request.session['chat_count'] = count + 1

    html = f"<div class='mb-2'><strong>شما:</strong> {message}</div><div class='mb-3 text-end'><strong>دستیار:</strong> {reply}</div>"
    return HttpResponse(html)
