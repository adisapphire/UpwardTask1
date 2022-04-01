from os import stat
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from .serializers import LoginSerializer, RegisterSerializer,MailSerializer
from rest_framework.permissions import IsAuthenticated
from .models import Mail
import time
from .mail import create_message, gmail_authenticate, Sync_mail, get_mails, send_message
MyMail = "puneet.bindal787@gmail.com"

class LoginViewSet(ModelViewSet, TokenObtainPairView):
    serializer_class = LoginSerializer
    permission_classes = (AllowAny,)
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class RegistrationViewSet(ModelViewSet, TokenObtainPairView):
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        res = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

        return Response({
            "user": serializer.data,
            "refresh": res["refresh"],
            "token": res["access"]
        }, status=status.HTTP_201_CREATED)

#refresh token view set
class RefreshViewSet(viewsets.ViewSet, TokenRefreshView):
    permission_classes = (AllowAny,)
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)

class SyncViewset(viewsets.ModelViewSet):
    serializer_class = MailSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get']

    def get_queryset(self):
        try:
            historyId = Mail.objects.order_by('-internalDate').first().historyid
        except:
            historyId= None
        try:
            service = gmail_authenticate()
            ids = Sync_mail(service,historyId)
            mails = get_mails(service,ids)
            for mail in mails:
                if not Mail.objects.filter(mail_id=mail['mail_id']).exists():
                    m = Mail(**mail)
                    m.save()
        except Exception as e:
            print(e,'hello')
        return Mail.objects.all()

class SendViewset(viewsets.ModelViewSet):
    serializer_class = MailSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
            data=request.data
            mails = Mail.objects.filter(sender_mail__icontains=data['sender'],subject__icontains=data['text'])
            threads = []

            for m  in mails:
                threads.append(m.thread_id)
            threads = set(threads)
            for t in threads:
                mail = Mail.objects.filter(thread_id=t).order_by('-internalDate').first()
                sender = mail.sender_mail
                import re
                x = re.search(r'<(.*?)>',sender)

                if not MyMail == x.group(1):
                    msg_id = mail.mail_id
                    thread_id = mail.thread_id
                    subject = mail.subject
                    reply_msg = create_message(MyMail, sender, msg_id, thread_id, subject, data['msg'])
                    service = gmail_authenticate()
                    res = send_message(service, "me", reply_msg)
                    txt = service.users().messages().get(userId='me', id=res['id'],format='full').execute()
                    mail = {}
                    mail['historyid'] = txt['historyId']
                    mail['internalDate'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(int(txt['internalDate'])/1000.0)) 
                    mail['mail_id'] = txt['id']
                    mail['subject'] = subject
                    mail['sender_mail'] = "Puneet Bindal <puneet.bindal787@gmail.com>"
                    mail['thread_id'] = txt['threadId']
                    m = Mail(**mail)
                    m.save()
                    
                    return Response(res, status=status.HTTP_200_OK)
            return Response("No message sent", status=status.HTTP_200_OK)



