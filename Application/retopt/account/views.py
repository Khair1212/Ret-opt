
from django.shortcuts import render
from django.shortcuts import redirect
from .models import Customer, Analyst,User
from django.views.generic import CreateView
from .forms import CustomerSignUpForm, AnalystSignUpForm
# Create your views here.
def index(request):
    return render(request,'index.html')
class CustomerSignUpView(CreateView):
    model = User
    form_class = CustomerSignUpForm
    template_name = 'signup.html'
    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'customer'
        return super().get_context_data(**kwargs)
    def form_valid(self, form):
        user = form.save()
        #login(self.request, user)
        return redirect('index')
    
class AnalystSignUpView(CreateView):
    model = User
    form_class = AnalystSignUpForm
    template_name = 'signup.html'
    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'manager'
        return super().get_context_data(**kwargs)
    def form_valid(self, form):
        user = form.save()
        #login(self.request, user)
        return redirect('index')
    

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CustomerSignUpForm, AnalystSignUpForm, CustomerUpdateForm, AnalystUpdateForm, ProfileUpdateForm
# Create your views here.


def customer_register(request):
    if request.method == 'POST':
        form = CustomerSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in!')
            return redirect('login')
    else:
        form = CustomerSignUpForm()
    return render(request, 'account/customer_register.html', {'form': form})

def analyst_register(request):
    if request.method == 'POST':
        form = AnalystSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in!')
            return redirect('login')
    else:
        form = AnalystSignUpForm()
    return render(request, 'account/analyst_register.html', {'form': form})

# @login_required
# def profile(request):
#     if request.method == 'POST':
        
#         u_form = UserUpdateForm(request.POST, instance=request.user)
#         p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

#         if u_form.is_valid() and p_form.is_valid():
#             u_form.save()
#             p_form.save()
#             messages.success(request, f'Your account has been updated!')
#             return redirect('profile')
#     else:
#         u_form = UserUpdateForm(instance=request.user)
#         p_form = ProfileUpdateForm(instance=request.user.profile)
#     context = {
#         'u_form':u_form,
#         'p_form': p_form
#     }

#     return  render(request, 'account/profile.html', context)


@login_required
def profile(request):
    if request.method == 'POST':
        if request.user.is_analyst:
            u_form = AnalystUpdateForm(request.POST, instance=request.user)
            p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.customer)
        else: 
            u_form = CustomerUpdateForm(request.POST, instance=request.user)
            p_form = ProfileUpdateForm(request.POST, instance=request.user.analyst)
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    else:
        if request.user.is_analyst:
            u_form = AnalystUpdateForm(instance=request.user)
            p_form = ProfileUpdateForm(instance=request.user.customer)
        else:
            u_form = CustomerUpdateForm(instance=request.user)
            p_form = ProfileUpdateForm(instance=request.user.analyst)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'account/profile.html', context)
