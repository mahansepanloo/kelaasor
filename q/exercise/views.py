import datetime
from rest_framework.permissions import IsAuthenticated
from .models import *
from rest_framework.views import APIView
from .serializer import *
from rest_framework.response import Response
from rest_framework import status, viewsets
from django.db import transaction
from accounts.models import User
from classs.models import Classs
from rest_framework import generics
from forum.permissions import IsJoinable
from rest_framework.parsers import FileUploadParser,MultiPartParser
import os
import requests
import subprocess
from django.db.models import Sum


class Inboxew(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        item = InboxExerciseModel.objects.filter(user=request.user)
        if item.exists():
            serilazers = InboxExerciseSerializer(instance=item, many=True)
            return Response(serilazers.data, status=status.HTTP_200_OK)
        return Response("not found inbox exercise", status=status.HTTP_404_NOT_FOUND)
    def post(self,request):
        try:
            item = InboxExerciseModel.objects.get(id=request.data['ide'])
        except  InboxExerciseModel.DoesNotExist:
            return Response("not found", status=status.HTTP_404_NOT_FOUND)
        q = ExerciseModel.objects.create(classs_id=request.data['class'],name=item.exercise.name,
                                         description=item.exercise.description,score=item.exercise.score,
                                         answer_format=item.exercise.answer_format)
        serilazers = CreateExerciseSerializers(instance=q)
        return Response(serilazers.data, status=status.HTTP_201_CREATED)









class CreateExerciseView(APIView):
    permission_classes = [IsAuthenticated, IsJoinable]
    def get(self, request,id_class):
        try:
            item = Classs.objects.get(id=id_class)
        except Classs.DoesNotExist:
            return Response('class not found', status=status.HTTP_404_NOT_FOUND)
        e = ExerciseModel.objects.filter(classs_id=item)
        serializer = CreateExerciseSerializers(instance=e, many=True)
        return Response(serializer.data)


    def post(self, request, id_class):
        try:
            item = Classs.objects.get(id=id_class)
        except Classs.DoesNotExist:
            return Response('class not found',status=status.HTTP_404_NOT_FOUND)
        if request.user in item.teacher.all() or request.user in item.ta.all():
            serializer = CreateExerciseSerializers(data=request.data)
            inbox = InboxSerializer(data=request.data)
            if serializer.is_valid():
                q = serializer.save(classs=item)
                if inbox.is_valid():
                    if inbox.validated_data['add'] == True:
                        InboxExerciseModel.objects.create(exercise=q,user=request.user)
                        return Response('created exercise add inbox', status=status.HTTP_201_CREATED)
                    return Response('created exercise', status=status.HTTP_201_CREATED)
                return Response(inbox.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response('not access',status=status.HTTP_403_FORBIDDEN)

class SubCriteriaCreate(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id_q):
        item = SubCriteria.objects.filter(exercise__id=id_q)
        if item.exists():
            q=item.first()
            if request.user in q.exercise.classs.teacher.all() or request.user in q.exercise.classs.ta.all():
                    serializer = ShowSubSerializer(instance=item,many=True)
                    return Response(serializer.data,status=status.HTTP_200_OK)
            return Response('not access',status=status.HTTP_403_FORBIDDEN)
        return Response(status=status.HTTP_404_NOT_FOUND)



    def post(self, request,id_q):
        try:
            q = ExerciseModel.objects.get(id=id_q)
        except ExerciseModel.DoesNotExist:
            return Response("exercise not found", status=status.HTTP_404_NOT_FOUND)
        if request.user in q.classs.teacher.all() or request.user in q.classs.ta.all():
            serilazers = SubCriteriaserializers(data=request.data)
            if serilazers.is_valid():
                validated_data = serilazers.validated_data
                for key, value in validated_data['a'].items():
                    SubCriteria.objects.create(exercise=q, name=key, score=value)
                return Response('add', status=status.HTTP_201_CREATED)
            return Response(serilazers.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response("not access", status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id_q):
        try:
            q = SubCriteria.objects.get(id=id_q)
        except ExerciseModel.DoesNotExist:
            return Response("exercise not found", status=status.HTTP_404_NOT_FOUND)
        if request.user in q.exercise.classs.teacher.all() or request.user in q.exercise.classs.ta.all():
            serializer = ShowSubSerializer(instance=q,data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response('not access',status=status.HTTP_403_FORBIDDEN)





class EditExerciseView(APIView):
    permission_classes = [IsAuthenticated]
    def put(self, request, id_exercise):
        try:
            item = ExerciseModel.objects.get(id=id_exercise)
        except ExerciseModel.DoesNotExist:
            return Response('not exist',status=status.HTTP_404_NOT_FOUND)
        if request.user in item.classs.teacher.all() or request.user in item.classs.ta.all():
            serializer = CreateExerciseSerializers(instance=item, data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response('not access',status=status.HTTP_403_FORBIDDEN)



class Create_Group_Manual(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, id_e):
        try:
            exercise = ExerciseModel.objects.get(id=id_e)
        except ExerciseModel.DoesNotExist:
            return Response('exercise does not exist',status=status.HTTP_404_NOT_FOUND)
        if request.user in exercise.classs.teacher.all() or request.user in exercise.classs.ta.all():
            serializer = Create_group(data=request.data)
            if serializer.is_valid():
               g = Group.objects.create(exercise=exercise)
               for i in serializer.validated_data['list_id']:
                   g.user.add(i)
               g.save()
               return Response("success",status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response('not access',status=status.HTTP_403_FORBIDDEN)


class SubmitAnswer(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, id_q):
        try:
            exercise = ExerciseModel.objects.get(id=id_q)
        except ExerciseModel.DoesNotExist:
            return Response('Exercise does not exist', status=status.HTTP_404_NOT_FOUND)
        if exercise.limit_send:
            if exercise.is_group:
                try:
                    group = Group.objects.get(exercise=exercise, user=request.user)
                    submission_count = AnswersModel.objects.filter(group=group, exercise=exercise).count()
                except Group.DoesNotExist:
                    return Response('Group not found', status=status.HTTP_404_NOT_FOUND)
            else:
                submission_count = AnswersModel.objects.filter(user=request.user, exercise=exercise).count()
            if submission_count > exercise.limit_send:
                return Response('Cannot send answer', status=status.HTTP_400_BAD_REQUEST)
        if str(exercise.answer_format) == str(request.data['answer_format']):
            if not exercise.is_group:
                    if request.data['answer_format'] == "1":
                        AnswersModel.objects.create(exercise=exercise, text=request.data['text'], user=request.user)
                        return Response('created', status=status.HTTP_201_CREATED)
                    elif request.data['answer_format'] == "2":
                        AnswersModel.objects.create(exercise=exercise, file=request.FILES['file'], user=request.user)
                        return Response('created', status=status.HTTP_201_CREATED)
                    return Response("bad requset", status=status.HTTP_400_BAD_REQUEST)
            if exercise.is_group:
                try:
                    g = Group.objects.filter(exercise=exercise, user=request.user).first()
                except Group.DoesNotExist:
                    return Response("Group does not exist", status=status.HTTP_404_NOT_FOUND)
                if request.data['answer_format'] == '1':
                    AnswersModel.objects.create(exercise=exercise, text=request.FILES['file'], group=g)
                    return Response('created', status=status.HTTP_201_CREATED)
                elif request.data['answer_format'] == '2':
                    AnswersModel.objects.create(exercise=exercise, file=request.data.get('file'), group=g)
                    return Response('created', status=status.HTTP_201_CREATED)
        return Response({'error': 'Invalid answer format'}, status=status.HTTP_400_BAD_REQUEST)





class AnswerCreateJuge(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id_a):
        code = request.data.get('code')
        language = request.data.get('language')

        if not code or not language:
            return Response({"error": "Code and language are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            question = ExerciseModel.objects.get(id=id_a)
        except ExerciseModel.DoesNotExist:
            return Response({"error": "Question not found."}, status=status.HTTP_404_NOT_FOUND)

        tests = Test.objects.filter(exercise=question)
        if not tests.exists():
            return Response({"error": "No tests found for this question."}, status=status.HTTP_404_NOT_FOUND)

        score = question.score
        points_per_test = score // len(tests)

        for test in tests:
            result = self.run_code(language, code, test)
            if result.get("score") != True:
                score -= points_per_test

        answer_data = {
            'exercise': question,
            'juge': code,
            'user': request.user,
            'score_received': score,
        }
        answer = AnswersModel.objects.create(**answer_data)
        serializer = AnswerSerializer(answer)
        socer, created = Socer.objects.get_or_create(exercises=question, user=request.user)
        if socer.score_received:
            if socer.score_received < score:
                socer.score_received = score
                socer.save()
        else:
            socer.score_received = score
            socer.save()

        serializer = AnswerSerializer(answer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    def run_code(self, language, code, tests):
        url = "https://api.jdoodle.com/v1/execute"
        headers = {'content-type': 'application/json'}

        body = {
            "clientId": "cc9ffef2535c84159a74fbd525fcbc23",
            "clientSecret": "19777fae74c242e307f72df03e6e8a7a2a2bffccb35cee69076378ef6edab07f",
            "script": code,
            "language": language,
            "versionIndex": "0",
            "stdin": tests.inputs
        }

        response = requests.post(url, headers=headers, json=body)
        if response.status_code == 200:
            response_json = response.json()
            output = response_json.get('output', '')
            score = self.evaluate_code(output, tests)
            return {'output': output, 'score': score}
        else:
            return {'output': 'error', 'score': 0}

    def evaluate_code(self, output, test):
        print(output.strip() == test.outputs.strip())
        return output.strip() == test.outputs.strip()



from django.http import HttpResponse
class Download(APIView):
    def get(self, request, file):
        document = AnswersModel.objects.get(id=file)
        file_path = document.file.path
        file = open(file_path, 'r', encoding='utf-8')
        file_content = file.read()
        response = HttpResponse(file_content, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename=document'
        return response



class all_Answer(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,id_q):
        q = AnswersModel.objects.filter(exercise=id_q)
        if q.exists():
            serializer = AnswerTextSerializer(q,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response("not founds", status=status.HTTP_404_NOT_FOUND)





class SocerTextAnswer(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,reqeust,id_a):
        try:
            q = AnswersModel.objects.get(id=id_a)
        except AnswersModel.DoesNotExist:
            return Response("not found", status=status.HTTP_404_NOT_FOUND)
        if reqeust.user in q.exercise.classs.ta.all() or reqeust.user in q.exercise.classs.teacher.all():
            if q.exercise.is_group == False:
                serializeranswer = AnswerTextSerializer1(instance=q,many=False)
                rez = SubCriteria.objects.filter(exercise=q.exercise)
                if rez.exists():
                    serializerrez = AnswerTextSerializer2(instance=rez,many=True)
                    return Response(data=(serializeranswer.data,serializerrez.data), status=status.HTTP_200_OK)
                return Response(data=serializeranswer.data, status=status.HTTP_200_OK)
            elif q.exercise.is_group == True:
                try:
                    g =Group.objects.get(user=q.user)
                except Group.DoesNotExist:
                    return Response("not found", status=status.HTTP_404_NOT_FOUND)
                serializergroup = AnswerTextSerializer3(instance=g)
                serializeranswer = AnswerTextSerializer1(instance=q, many=False)
                rez = SubCriteria.objects.filter(exercise=q.exercise)
                if rez.exists():
                    serializerrez = AnswerTextSerializer2(instance=rez, many=True)
                    return Response(data=(serializeranswer.data, serializerrez.data,serializergroup.data), status=status.HTTP_200_OK)
                return Response(data=serializeranswer.data, status=status.HTTP_200_OK)
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response("not access",status=status.HTTP_403_FORBIDDEN)

    def put(self, request, id_a):
        try:
            q = AnswersModel.objects.get(id=id_a)
        except AnswersModel.DoesNotExist:
            return Response("not found", status=status.HTTP_404_NOT_FOUND)
        if request.user in q.exercise.classs.teacher.all() or request.user in q.exercise.classs.ta.all():
            a = AnswerSerilazers(instance=q,data=request.data,partial=True)
            if a.is_valid():
                    b = a.validated_data.get("bazkhord",None)
                    if a.validated_data["score_received"] > q.exercise.score:
                        return Response("score not valid", status=status.HTTP_400_BAD_REQUEST)
                    if  q.exercise.is_group == False:
                        q.score_received = int(a.validated_data["score_received"])
                        q.bazkhord = b
                        q.save()
                        socer, created = Socer.objects.get_or_create(exercises=q.exercise, user=q.user)
                        if socer.score_received:
                            if socer.score_received < a.validated_data["score_received"]:
                                socer.score_received = a.validated_data["score_received"]
                                socer.save()
                        else:
                            socer.score_received = a.validated_data["score_received"]
                            socer.save()

                        return Response('save score', status=status.HTTP_201_CREATED)
                    if q.exercise.is_group == True:
                        q.score_received = int(a.validated_data["score_received"])
                        q.bazkhord = b
                        q.save()
                        if q.group:
                                g = q.group.user.all()
                                for i in g:
                                    GroupAssignment.objects.create(group=q.group,user=i,score_received=a.validated_data["score_received"])
                                    socer, created = Socer.objects.get_or_create(exercises=q.exercise, user=i)
                                    if socer.score_received :
                                        if socer.score_received < a.validated_data["score_received"]:
                                            socer.score_received = a.validated_data["score_received"]
                                            socer.save()
                                    socer.score_received = a.validated_data["score_received"]
                                    socer.save()
                                return Response(data=a.data, status=status.HTTP_201_CREATED)
                    return Response("Group not found", status=status.HTTP_404_NOT_FOUND)

            return Response(data=a.errors, status=status.HTTP_404_NOT_FOUND)
        return Response("not allowed", status=status.HTTP_404_NOT_FOUND)
class EditSocerUserGroupView(APIView):
    def put(self, request, id_a):
        try:
            qq = AnswersModel.objects.get(id=id_a)
        except AnswersModel.DoesNotExist:
            return Response("Answer not found", status=status.HTTP_404_NOT_FOUND)

        name = request.data.get('name')
        score = request.data.get('score')
        if not name or score is None:
            return Response("Both 'name' and 'score' must be provided", status=status.HTTP_400_BAD_REQUEST)
        q = GroupAssignment.objects.filter(group=qq.group)
        try:
            n = q.get(user=name)
        except GroupAssignment.DoesNotExist:
            return Response("User not found in group", status=status.HTTP_404_NOT_FOUND)
        n.score_received = score
        n.save()
        s = Socer.objects.get(exercises=qq.exercise,user=name)
        s.score_received = score
        s.save()
        return Response(status=status.HTTP_200_OK)





def groupauto(input_list: list, num: int):
    ln = [[] for _ in range(num)]
    sums = [-(len(input_list))] * num
    l = len(input_list)
    for item in input_list:
        a = sums.index(min(sums))
        ln[a].append(item)
        sums[a] += l
        l -= 1
    return(ln)
class RankingView(APIView):
        permission_classes = [IsAuthenticated,IsJoinable]
        def get(self, request, id_class):
            try:
                some_class = Classs.objects.get(id=id_class)

                socer_list = (
                    Socer.objects
                    .filter(exercises__classs=some_class)
                    .values('user__username')
                    .annotate(total_score=Sum('score_received'))
                    .order_by('-total_score')
                )

                ranked_scores_with_ranks = [
                    {'username': socer['user__username'], 'total_score': socer['total_score']}
                    for  socer in socer_list]

                return Response(ranked_scores_with_ranks, status=status.HTTP_200_OK)
            except Classs.DoesNotExist:
                return Response({'error': 'Class not found'}, status=status.HTTP_404_NOT_FOUND)

        def post(self, request, id_class):

                some_class = Classs.objects.get(id=id_class)
                socer_list = (
                    Socer.objects
                    .filter(exercises__classs=some_class)
                    .values('user__username', 'user')
                    .annotate(total_score=Sum('score_received'))
                    .order_by('-total_score')
                )


                l = list(socer_list.values_list('user', flat=True))
                num_groups = request.data['num']
                if int(num_groups)*2 > len(l):
                    return Response("cant",status=status.HTTP_400_BAD_REQUEST)
                a = groupauto(l,int(num_groups))
                for group in a:
                    new_group = Group.objects.create(exercise_id=request.data['id_e'])
                    for user_id in group:
                        user = User.objects.get(id=user_id)
                        new_group.user.add(user)
                return Response(status=status.HTTP_201_CREATED)



class RezscoreUser(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, e_id):
        sub = SubCriteria.objects.filter(exercise_id=e_id)
        if sub.exists():
            s = AnswerTextSerializer2(instance=sub,many=True)
            return Response(s.data,status=status.HTTP_200_OK)
        return Response({'error': 'Sub does not exist'}, status=status)


    def post(self, request, e_id):
        sub = SubCriteria.objects.filter(exercise_id=e_id)
        a = AnswersModel.objects.get(id=request.data['answer_id'])
        if sub.exists():
            RezScore.objects.create(user=a.user, score=request.data['score'],sub_id=request.data['sub'])
            return Response(status=status.HTTP_201_CREATED)
        return Response({'error': 'Sub does not exist'}, status=status)


class AddTask(APIView):
    def get(self, request, e_id):
        try:
            sub = ExerciseModel.objects.get(id=e_id)
            tasks = Test.objects.filter(exercise = sub)
        except ExerciseModel.DoesNotExist:
            return Response({'error': 'Exercise not found'}, status=status.HTTP_404_NOT_FOUND)
        if request.user in sub.classs.ta.all() or request.user in sub.classs.teacher.all():
            serializer = Taskserlazers(instance=tasks,many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response("not accsess",status=status.HTTP_403_FORBIDDEN)
    def post(self,request,e_id):
        try:
            sub = ExerciseModel.objects.get(id=e_id)
        except ExerciseModel.DoesNotExist:
            return Response({'error': 'Exercise not found'}, status=status.HTTP_404_NOT_FOUND)
        if request.user in sub.classs.ta.all() or request.user in sub.classs.teacher.all():
            serializer = Taskserlazers(data=request.data)
            if serializer.is_valid():
                a = serializer.validated_data.get('inputs')
                z = a.replace(" ","\r\n")
                serializer.save(exercise = sub,user=request.user,inputs=z)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response("not accsess",status=status.HTTP_403_FORBIDDEN)
class AllAnswers(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,id_q):
        q = AnswersModel.objects.filter(exercise=id_q,user = request.user)
        if q.exists():
            serializer = AnswerTextSerializer(q,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response("not founds", status=status.HTTP_404_NOT_FOUND)


class Show_Groups(APIView):
    permission_classes = [IsAuthenticated,IsJoinable]
    def get(self,reqeust,id_e,id_class):
        group = Group.objects.filter(exercise_id=id_e)
        data = ShowGroupsSerializers(instance=group,many=True)
        return Response(data.data,status = status.HTTP_200_OK)
    
    