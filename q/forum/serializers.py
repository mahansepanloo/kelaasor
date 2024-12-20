from rest_framework import serializers
from .models import Question, Answer

class QuestionSerializer(serializers.ModelSerializer):
    # answers = serializers.SerializerMethodField()
    class Meta:
        model = Question
        fields = '__all__'
        extra_kwargs = {
            "user": {"required": False},
            'classs': {"required": False},
            "title": {"required": False}
        }
    # def get_answers(self,obj):
    #         a = obj.qanswer.all()
    #         return AnswerSerializer(instance=a, many=True).data

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'
        extra_kwargs = {
            "user": {"required": False, "read_only": True},
            'question': {"required": False, "read_only": True},

        }

class CreatERateSerializer(serializers.Serializer):
    rate = serializers.IntegerField()






