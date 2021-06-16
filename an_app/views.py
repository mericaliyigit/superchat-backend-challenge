import json
import time
from json import JSONDecodeError

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import serializers
from django.core.serializers.json import Serializer
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime

import requests
from ipaddress import ip_address,ip_network

from django.views.decorators.http import require_POST
from rest_framework.views import APIView

from an_app.models import Contact, Chat, Message
from django.forms.models import model_to_dict

from an_app.apps import SuperChatConfig


class MainView(View):

    def get(self,request):

        if request.user.is_authenticated:
            print('Yee')
            return HttpResponse("Welcome to superchat",status=200)
        else:
            print('Noo')
            return HttpResponse("Unathorized",status=200)


class CreateContact(APIView):

    def post(self, request):

        if not request.user.is_authenticated:
            return HttpResponse("Unauthorized",status=401)

        print(request.user, request.user.id)
        print(request.body)
        try:
            data = json.loads(request.body)
        except JSONDecodeError as e:
            print('Bad request')
            return HttpResponse(status=400)
        required_fields = ('name','surname','email')
        for req in required_fields:
            if req not in data:
                #print('Missing content')
                return HttpResponse(f'Missing content')
        else:
            record=Contact.objects.filter(email=data['email'])
            if record:
                return HttpResponse(f"Contact with {data['email']} already exists")
            else:
                a_contact = Contact.objects.create(owner_id=request.user.id , **data)
                a_contact.owner_id = request.user
                a_contact.save()
                return HttpResponse(f"Successfully created new contact", status=200)

    def get(self,request):
        print("Post only")
        return HttpResponse(status=400)


class Contacts(APIView):

    def get(self,request):

        if not request.user.is_authenticated:
            return HttpResponse("Unauthorized",status=401)

        queryset = Contact.objects.all()
        print(queryset)
        jsoned=json.loads(serializers.serialize("json", queryset, fields =('name','surname','email')))
        jstring = ""
        for d in jsoned:
            jstring +='\n'
            jstring += json.dumps(d['fields'])
            print(d)

        return HttpResponse(jstring, content_type='application/json')


class SendMessage(APIView):

    def post(self,request):

        if not request.user.is_authenticated:
            return HttpResponse("Unauthorized",status=401)

        try:
            data = json.loads(request.body)
        except JSONDecodeError as e:
            return HttpResponse(f'Wrong format json {e}')

        required_fields = ('receiver','content')
        for req in required_fields:
            if req not in data:
                return HttpResponse(f'Missing content')
        else:
            print('Checking if valid receiver exists')
            target=Contact.objects.filter(email= data['receiver'])[0]
            if target:
                print('receiver mail is valid ')
                q = Chat.objects.filter(owner_id=request.user.id,target__id=target.id)
                old_chat = None
                if len(q) > 0:
                    old_chat = q[0]

                if old_chat:

                    print('old chat exists appending to it')
                    the_message = SuperChatConfig.plugin.message_fix(data['content'], target.name)
                    new_message = Message.objects.create(sender_id=request.user.id, receiver_id=target.id,
                                                         chat_id=old_chat.id,content=the_message)
                    new_message.save()
                    return HttpResponse(f'Message sent to {data["receiver"]}')
                else:
                    print('No previous chat will create one')
                    print(request.user.id)
                    new_chat=Chat.objects.create(owner_id=request.user.id,target_id=target.id)
                    new_chat.save()
                    print('Created a new chat now I will append this message to it')

                    the_message = SuperChatConfig.plugin.message_fix(data['content'],target.name)
                    new_message = Message.objects.create(sender_id=request.user.id, receiver_id=target.id,
                                                         chat_id=new_chat.id,content=the_message)

                    new_message.save()
                    return HttpResponse(f"Message sent to {data['receiver']}")

            else:
                return HttpResponse('NO SUCH USER')


        return HttpResponse(content="All is good", status=200)

    def get(self,request):
        print("Post only")
        return HttpResponse(status=400)


class Conversations(APIView):
    def get(self,request):

        if not request.user.is_authenticated:
            return HttpResponse("Unauthorized",status=401)

        chats = Chat.objects.filter(owner_id=request.user.id)
        all_chats = []
        for chat in chats:
            print(chat, chat.id, chat.owner_id)
            messages = Message.objects.filter(chat=chat.id).order_by('created')
            jsoned = json.loads(serializers.serialize("json", messages))
            #print(jsoned)
            chat_o = dict()
            chat_o['receiver'] = chat.target.email
            chat_o['messages'] = list()
            for jj in jsoned:
                chat_o['messages'].append({'datetime': jj['fields']['created'],
                                          'message' : jj['fields']['content']})

            all_chats.append(chat_o)

        print(all_chats)

        return HttpResponse(content=all_chats,status=200)

    def post(self,request):
        print("Get only")
        return HttpResponse(status=400)



def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    return ip_address(ip)


@require_POST
@csrf_exempt
def githubhook(request):
    client_ip = get_client_ip(request)
    print(type(client_ip))
    # ask github for valid hook ips this could be static list as well
    whitelist = requests.get('https://api.github.com/meta')
    hooks = whitelist.json()['hooks']
    print(f'Accepted hooks {hooks}')
    print(f'Clinet ip {client_ip}')
    # If in our trusted list return today if not return forbidden
    for accepted_ip in hooks:
        if client_ip in ip_network(accepted_ip):
            break
    else:
        return HttpResponse('Forbidden',status=403)

    # it passed our requirements we can respond to this hook
    return HttpResponse(f'Git-hook response {datetime.now()}')