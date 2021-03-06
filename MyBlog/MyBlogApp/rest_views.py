from datetime import datetime
from rest_framework.renderers import JSONRenderer
from models import Blog

__author__ = 'stephaneki'

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from serializers import BlogSerializer


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


@csrf_exempt
def blog_create(request):
    """
    Create a blog.
    """
    if request.method == 'PUT':
        data = JSONParser().parse(request)
        blog = Blog(time=datetime.now())
        blog.save()
        serializer = BlogSerializer(blog, data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data)
        else:
            return JSONResponse(serializer.errors, status=400)

    else:
        return HttpResponse(status=400)  # Bad request