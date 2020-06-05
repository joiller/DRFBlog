from django.shortcuts import render
from rest_framework.settings import api_settings

from .serializers import *
from rest_framework import views, generics, viewsets
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth import get_user_model
from django.http import HttpResponseForbidden
import jwt
from utils import get_md5
from rest_framework.authtoken.models import Token
from django.contrib.auth import logout, login
from rest_framework.authtoken.views import ObtainAuthToken


# Create your views here.


class BlogUserViewSet(viewsets.ModelViewSet):
    queryset = BlogUser.objects.all()
    serializer_class = BlogUserSerializer


class BlogUserRegisterView(generics.CreateAPIView):
    print('viewing')
    queryset = BlogUser.objects.all()
    serializer_class = BlogUserRegisterSerializer

    def create(self, request, *args, **kwargs):
        print('creating')
        serializer = self.get_serializer(data=request.data)
        print(serializer.is_valid())
        # print(serializer.data)
        print(serializer.validated_data)
        if serializer.is_valid():
            print('yesyes')
            # del serializer.validated_data['password2']
            # user = BlogUser(**serializer.data)
            # user.is_active = False
            # user.source = 'Register'
            # print(user)
            # user.save()
            # s = self.get_serializer(user)
            if serializer.validated_data['password'] == serializer.validated_data['password2']:
                user = serializer.save()
            else:
                raise serializer.ValidationError({"password": 'password must match'})

            sign = get_md5(str(user.id)+user.password)
            # sign = jwt.encode({"validation": (str(user.id)+user.email)},'validation', algorithm='HS256')
            root = 'http://127.0.0.1:8000'
            url = '{root}/result/?type={type}&id={id}&sign={sign}'.format(root=root,
                                              type='validation',
                                              id=user.id,
                                                     sign=sign)
            subject = '验证邮件'
            message = """
            <p>你好呀，<p/>
            <p>这是一份验证邮件<p/>
            点击下方链接<br />
            <a href='{url}' rel='bookmark'>{url}</a>
            """.format(url=url)

            send_mail(subject, 'message', from_email='781225147@qq.com',
                      recipient_list=['xiaoxiaobaer@gmail.com'],
                      html_message=message)

            to_url = '{root}/result/?type={type}&id={id}'.format(root=root,
                                                 type='register',
                                                 id=user.id)

            return redirect(to_url)

        else:
            return Response(serializer.errors)

    # def post(self, request, *args, **kwargs):
    #     print('????????????')
    #     return self.create(request,*args, **kwargs)


def register_result(request):
    type = request.GET.get('type')
    id = request.GET.get('id')

    user = get_object_or_404(get_user_model(), id=id)
    if user.is_active:
        return redirect('/')
    if type and type in ['register', 'validation']:
        token = Token.objects.get(user=user).key

        if type=='register':
            content = '''
            注册成功，邮件发到你的{email}邮箱中，请去邮箱验证后登录
            '''.format(email=user.email)
            title = '注册成功'
        else:
            correct_sign = get_md5(str(user.id)+user.password)
            # correct_sign = str(jwt.encode({"validation": (str(user.id)+user.email)},'validation', algorithm='HS256'))
            sign = request.GET.get('sign')
            if sign!=correct_sign:
                return HttpResponseForbidden()
            user.is_active = True
            user.save(update_fields=['is_active'])
            content = '验证成功，可以登录了'
            title = '验证成功'

        return render(request, 'Account/result.html', {
            'title': title,
            'content': content,
            'token': token
        })
    else:
        return redirect('/')


class LoginView(ObtainAuthToken):
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        login(request, user)
        return Response({'token': token.key})


def logout_view(request):
    user = request.user
    token = Token.objects.get(user=user)
    token.delete()
    logout(request)
    print(user)
    Token.objects.create(user=user)
    # Token.objects.create(user=request.user)
    return redirect('Account:base')


# def base_view(request):
#     return render(request, 'Account/base.html')


class BaseView(generics.ListAPIView):
    # authentication_classes = [ObtainAuthToken]
    queryset = BlogUser.objects.all()
    serializer_class = BlogUserSerializer

    def list(self, request, *args, **kwargs):
        return render(request, 'Account/base.html')
