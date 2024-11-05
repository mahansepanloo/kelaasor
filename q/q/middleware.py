from django.contrib.auth.models import AnonymousUser


class LoggerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.activate = {}

    def __call__(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')

        user = "Anonymoususer" if isinstance(request.user, AnonymousUser) else str(request.user)

        response = self.get_response(request)

        self.activate.update({
            'ip': ip,
            'user': user,
            "view": self._get_view_name(request),
            "host": request.get_host(),
        })

        try:
            with open('loggers.log', "a") as f:
                f.write(f"{self.activate}\n")
        except Exception as e:
            print(f"Error writing to log file: {e}")

        return response

    def _get_view_name(self, request):
        view_name = getattr(request, 'resolver_match', None)
        if view_name:
            return f"{view_name.view_name} ({view_name.url_name})"
        return "No view associated"
    








    
from django.http import HttpResponseForbidden  
from datetime import datetime,timedelta

list_ban = {}

class BlockIpMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    def __call__(self, request):
        self._remove_expired_bans(request)
        if self.get_ip(request) in list_ban:
             return HttpResponseForbidden("You are banned")
        response = self.get_response(request)
        return response
    
    def get_ip(self,request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    def _remove_expired_bans(self,requset):
        now = datetime.now()
        for ip in list_ban:
            if now - list_ban[ip] > timedelta(minutes=1):
                del list_ban[ip]
           
    


class Manager_ban:
    now = datetime.now()
    def add(self,request):
          list_ban[self._get_ip(request)] = self.now

    def remove(self,request):
            del list_ban[self._get_ip(request)]  
    def _get_ip(self,request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
              ip = x_forwarded_for.split(',')[0]
        else:
              ip = request.META.get('REMOTE_ADDR')
        return ip
           
    

    