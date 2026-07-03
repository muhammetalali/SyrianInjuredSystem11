from .models import AuditLog

class AuditLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.user.is_authenticated and request.method in ["POST", "PUT", "PATCH", "DELETE"]:
            AuditLog.objects.create(
                user=request.user,
                action=f"{request.method} request",
                path=request.path,
                method=request.method,
                ip_address=request.META.get("REMOTE_ADDR"),
            )

        return response