from django.conf import settings

def google_analytics(request):
    return {'GOOGLE_ANALYTICS': settings.GOOGLE_ANALYTICS }


def debug(request):
    return {'DEBUG': settings.DEBUG }
