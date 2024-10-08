from rest_framework import serializers
from .models import *




class CreateExerciseSerializers(serializers.ModelSerializer):
    class Meta:
        model = ExerciseModel
        exclude = ['classs']

class InboxSerializer(serializers.Serializer):
    add = serializers.BooleanField()



class Create_group(serializers.Serializer):
    list_id = serializers.ListField()

class AnswerTextSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswersModel
        fields = ['']

class SubCriteriaserializers(serializers.Serializer):
    a = serializers.DictField()

class AnswerTextSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswersModel
        fields = ['user', "id"]

class AnswerTextSerializer1(serializers.ModelSerializer):
    class Meta:
        model = AnswersModel
        fields = "__all__"
class AnswerTextSerializer2(serializers.ModelSerializer):
    class Meta:
        model = SubCriteria
        fields = "__all__"
class AnswerTextSerializer3(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"
class AnswerSerilazers(serializers.ModelSerializer):
    class Meta:
        model = AnswersModel
        fields = ['score_received']
        extra_kwargs = {'score_received': {'required': True}}

class InputTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = '__all__'


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswersModel
        fields = '__all__'




class SubCriteriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswersModel
        fields = "__all__"

class RankSerilazers(serializers.ModelSerializer):
    class Meta:
        model = Socer
        fields = "__all__"

class Rezserilazers(serializers.ModelSerializer):
    class Meta:
        model = RezScore
        fields = "__all__"