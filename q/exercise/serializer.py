from rest_framework import serializers
from .models import *

class InboxExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model =InboxExerciseModel
        fields = '__all__'


class CreateExerciseSerializers(serializers.ModelSerializer):
    class Meta:
        model = ExerciseModel
        exclude = ['classs']
        extra_kwargs = {
            "nsocre": {"required": False}
        }

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

class AnswersSerializer(serializers.Serializer):
    answer_format = serializers.IntegerField()
    text = serializers.CharField(required=False)
    file = serializers.FileField(required=False)
class ShowSubSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCriteria
        fields = "__all__"

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
        fields = ['score_received',"bazkhord"]
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
    sub = serializers.CharField(source='sub.name')
    class Meta:
        model = RezScore
        fields = "__all__"


class Taskserlazers(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = "__all__"
        extra_kwargs = {
            'user': {'required': False},
            'exercise':{'required': False}
        }

class ShowGroupsSerializers(serializers.ModelSerializer):  
    user = serializers.SerializerMethodField()  
    class Meta:  
        model = Group  
        fields = "__all__" 

    def get_user(self, obj):  
        return [user.username for user in obj.user.all()]