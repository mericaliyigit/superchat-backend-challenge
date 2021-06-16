from rest_framework import serializers

from an_app.models import Chat,Message,Contact

class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ['owner','participants','created']

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields =['id','owner','created','name','email']

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id','sender','receiver','created','chat','content']


