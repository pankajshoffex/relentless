from rest_framework.authentication import SessionAuthentication, BasicAuthentication


class CsrfExemptSessionAuthentication(SessionAuthentication):
    """
     Disable CSRF Token from the session authentication
    """

    def enforce_csrf(self, request):
        return # To not perform the csrf check previously happening
