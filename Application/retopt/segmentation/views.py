from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from account.models import Analyst

# Create your views here.
def segmentation():
    print("HI")


#@user_passes_test(lambda u: u.groups.filter(name='analyst').exists())
@user_passes_test(lambda u: u.is_authenticated and not u.is_customer)
def segmentation_view(request):
    if request.user.is_authenticated:
        analyst = Analyst.objects.get(user=request.user)
        print(analyst)
        return render(request, 'segmentation/analysis.html',)
