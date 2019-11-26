
from django.shortcuts import render
from django.views.generic import View

# qudong/manage
class QudongManageView(View):
    '''驱动管理'''
    def get(self, request):

        return render(request, 'qudong/Library_Main.html' )

# qudong/manage/drive
class QudongDriveView(View):
    '''驱动列表'''
    def get(self, request):

        return render(request, 'qudong/Driver_Library.html')
        # return render(request, 'qudong/Template_Library.html')


# qudong/manage/template
class QudongTemplateView(View):
    '''驱动列表'''
    def get(self, request):

        # return render(request, 'qudong/Driver_Library.html')
        return render(request, 'qudong/Template_Library.html')
