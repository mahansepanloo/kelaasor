from rest_framework.permissions import BasePermission
from rest_framework.exceptions import NotFound, PermissionDenied
from .models import Classs


class IsJoinable(BasePermission):
    def has_permission(self, request, view):
        class_id = view.kwargs.get('id_class')
        if class_id is None:
            return False
        try:
            item = Classs.objects.get(id=class_id)
        except Classs.DoesNotExist:
            raise NotFound("Class not found.")
        if (request.user in item.user.all() or
                request.user in item.ta.all() or
                request.user in item.teacher.all()):
            return True
        raise PermissionDenied("Access denied to see class.")