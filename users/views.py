from django.shortcuts import render, redirect, reverse
from django.conf import settings
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib import messages
from django.utils import timezone
from kavenegar import KavenegarAPI, APIException, HTTPException
from random import randint

from .forms import SignUpForm
from .models import UserVerifyToken
from .decorators import projects_panel

User = get_user_model()


def kave_negar_token_send(receptor, token, template='verify'):
    try:
        api = KavenegarAPI(settings.SMS_API_KEY)
        params = {
            # 'sender':   '1000596446',
            'receptor': receptor,
            'message':  '.وب سرویس پیام کوتاه کاوه نگار',
            'template': template,
            'token':    token,
            'type':     'sms',
        }
        response = api.verify_lookup(params)
        print('kave_negar_token_send:', response)
    except APIException as e:
        print(e)
    except HTTPException as e:
        print(e)


def sign_up(request):

    if request.user.is_authenticated:
        print(request.user.pk)
        return redirect('/dashboard/')
    else:
        form = SignUpForm(request.POST or None)
        if request.method == 'POST':
            print('in sign_up | POST')
            if form.is_valid():
                print('form valid')
                template = 'verify'
                print(form.cleaned_data.get('username'))
                user = form.save(commit=False)
                # user.refresh_from_db()
                # load the profile instance created by the signal
                user.is_active = False
                token = randint(100000, 999999)
                print(f'token: {token}')
                # token = 123456
                user.save()
                new_phone = form.cleaned_data.get('username')
                # profile = Profile.objects.create(user=user, phone=new_phone, verify_code=code)
                # user.save()
                raw_password = form.cleaned_data.get('password1')
                # kave_negar_token_send(new_phone, token, template)
                verify_obj = UserVerifyToken.objects.create(phone_number=new_phone, verify_token=token)
                verify_obj.save()
                request.session['phone_number'] = new_phone
                return redirect('users:verify')

        return render(request, 'users/register.html', {'form': form})


def verify(request):
    print('in verify')
    print(request.session['phone_number'])
    if request.method == 'POST':
        phone_number = request.session.get('phone_number')
        verify_code = request.POST.get(f'verify_code', None)
        print(f'verify_code: {verify_code}')
        print(f'phone_number: {phone_number}')
        verify_obj = None
        try:
            # this objects.get() may get multiple result if the token is not unique and the number is repeated
            verify_obj = UserVerifyToken.objects.get(phone_number=phone_number, verify_token=verify_code)
        except UserVerifyToken.DoesNotExist:
            messages.add_message(request, messages.ERROR, 'کد وارد شده نامعتبر است')
            start_time = request.POST.get('remaining_time', None)
            print(f'start_time: {start_time}')
            return render(request, 'users/verify.html', {'start_time': start_time})
        if verify_obj:
            created_at = verify_obj.created_at.timestamp()
            now = timezone.now().timestamp()
            if now - created_at > 120:
                messages.add_message(request, messages.ERROR, 'مدت اعتبار سنجی به پایان رسیده است')
                return render(request, 'users/verify.html', {'start_time': '00:00'})
            print(now)
            print(verify_obj)
            user_obj = User.objects.get(username=phone_number)
            user_obj.is_active = True
            user_obj.save()
            request.session.pop('phone_number')
            return render(request, 'users/verify_success.html')
    return render(request, 'users/verify.html')


# http://127.0.0.1:8000/users/sign_up/
def verify_success(request):
    return render(request, 'users/verify_success.html', {})

# def register(request):
#     if request.method == 'POST':
#         form = CustomUserCreationForm(request.POST)
#         if form.is_valid():
#             print('form is valid')
#             form.save()
#             username = form.cleaned_data.get('username')
#             messages.success(request, f'Your account has been created: {username} .You are now able to log in')
#             return redirect('users:user-login')
#     else:
#         form = CustomUserCreationForm()
#     return render(request, 'users/register.html', {'form': form})


# def signup(request):
#     context = dict()
#     if request.method == 'POST':
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password1')
#             new_user = authenticate(username=username, password=password)
#             login(request, new_user)
#             return redirect('team')
#     else:
#         form = SignUpForm()
#     context['form'] = form
#     return render(request, 'signup.html', context=context)
