from rest_framework import serializers
from .models import Classs,SubCriteriaClass

class CreateClassSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = Classs
        exclude = [
            "teacher", "ta", "user"
        ]
        extra_kwargs = {
            "description": {"required": True},
            "finish": {"required": False},
            "start": {"required": False}
        }

class AdduserPrivetSerializer(serializers.Serializer):
    user = serializers.ListField()


class CodserSerializer(serializers.Serializer):
    password = serializers.CharField()



class Editeclass(serializers.Serializer):
    teacher = serializers.ListField(required=False)
    ta = serializers.ListField(required=False)
    user = serializers.IntegerField(required=False)

class EditeinfoClass(serializers.ModelSerializer):
    class Meta():
        model = Classs
        fields = "__all__"


class ShowInfoClass(serializers.ModelSerializer):
    class Meta:
        model = Classs
        fields = "__all__"






class SubClass(serializers.Serializer):
    item = serializers.ListField()

class SubEdite(serializers.ModelSerializer):
    class Meta:
        model = SubCriteriaClass
        exclude = ["clas"]
        extra_kwargs={
            'name':{'required': True},

        }

