import os
from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def myself(request):
    blog_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    resume_path = blog_path + '/static/resume/lvbiaobiao-python.pdf'
    with open(resume_path, 'rb') as pdf:
        response = HttpResponse(pdf.read(), content_type='application/pdf')
    response['Content-Disposition'] = 'filename=lvbiaobiao-python.pdf'
    # response = FileResponse(open(resume_path, 'rb'))
    return response
