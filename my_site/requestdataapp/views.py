from django.core.files.storage import FileSystemStorage
from django.http import HttpRequest
from django.shortcuts import render
from django.views import View

from .forms import UserBioForm, UploadFileForm




def process_get_view(request: HttpRequest):
    a = request.GET.get('a', '')
    b = request.GET.get('b', '')
    result = a + b
    context = {
        'a': a,
        'b': b,
        'RESULT': result,
    }
    return render(request, 'requestdataapp/request-qwerty.html', context=context)


def user_form(request: HttpRequest):
    context = {
        'form': UserBioForm(),
    }
    return render(request, 'requestdataapp/user_boi_form.html', context=context)

def handle_file_upload(request: HttpRequest):

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            myfile = form.cleaned_data['file']

            fs = FileSystemStorage()
            if myfile.size > (1024 * 1024):
                print('Файл превышает 1Мб. Загрузка невозможна')
                return render(request, 'requestdataapp/error_file.html')
            filename = fs.save(myfile.name, myfile)
            print('Фаил сохранен', filename)
    else:
        form = UploadFileForm()
    context = {
        'form': form,
    }

    return render(request, 'requestdataapp/file-upload.html', context=context)



