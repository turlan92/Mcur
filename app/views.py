import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_datetime
from django.shortcuts import render

from .models import PiImage


def view_images(request):
    # Получаем GET-параметры
    sort_order = request.GET.get('sort', 'desc')   # asc или desc
    date_from = request.GET.get('from')
    date_to = request.GET.get('to')

    images = PiImage.objects.all()

    # Фильтруем по дате/времени
    if date_from:
        dt_from = parse_datetime(date_from)
        if dt_from:
            images = images.filter(received__gte=dt_from)
    if date_to:
        dt_to = parse_datetime(date_to)
        if dt_to:
            images = images.filter(received__lte=dt_to)

    # Сортировка
    if sort_order == 'asc':
        images = images.order_by('received')
    else:
        images = images.order_by('-received')

    return render(request, 'app/view_images.html', {
        'images': images,
        'sort_order': sort_order,
        'date_from': date_from or '',
        'date_to': date_to or ''
    })

API_KEY = os.environ.get('API_KEY_FOR_PI', 'SECRET_KEY_HERE')

@csrf_exempt
def upload_image(request):
    key = request.META.get('HTTP_X_API_KEY')
    if key != API_KEY:
        return JsonResponse({'detail': 'Unauthorized'}, status=401)

    if request.method != 'POST':
        return JsonResponse({'detail': 'Method not allowed'}, status=405)

    if 'image' not in request.FILES:
        return JsonResponse({'detail': 'No image file'}, status=400)

    f = request.FILES['image']
    camera = request.POST.get('camera', 'pi_cam')
    timestamp = request.POST.get('timestamp')

    parsed_ts = parse_datetime(timestamp) if timestamp else None

    pi_img = PiImage.objects.create(
        camera=camera,
        image=f,
        timestamp=parsed_ts
    )

    return JsonResponse({
        'id': pi_img.id,
        'camera': pi_img.camera,
        'timestamp': pi_img.timestamp,
        'received': pi_img.received,
        'image_url': pi_img.image.url,
    }, status=201)


from django.shortcuts import render
from .models import PiImage


