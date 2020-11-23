from webview.models import books
#from django.contrib.auth.models import User, Group
from rest_framework import serializers
from django.contrib.auth.models import User, Group

class booksSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = books
        fields = ('url', 'title','author','isbn','publisher','publication_year','last_modified_date','created_date','created_at','update_at')
   #fields = ('url','title','author','isbn','publisher','publication_year','last_modified_date','created_date','created_at','update_at')

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']