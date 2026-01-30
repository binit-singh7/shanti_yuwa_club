from django.contrib.sessions.middleware import SessionMiddleware
from django.conf import settings

class AdminSessionMiddleware(SessionMiddleware):
    """
    Middleware that uses a different session cookie for the admin site.
    This prevents the admin session from logging in the user on the main site,
    and vice-versa.
    """
    ADMIN_SESSION_COOKIE_NAME = 'admin_sessionid'

    def process_request(self, request):
        # Determine which cookie to use
        if request.path.startswith('/admin/'):
            # Use admin cookie
            session_key = request.COOKIES.get(self.ADMIN_SESSION_COOKIE_NAME)
            request.session = self.SessionStore(session_key)
        else:
            # Use default mechanism
            super().process_request(request)

    def process_response(self, request, response):
        # Let the standard middleware handle saving the session
        # logic and setting the default cookie.
        response = super().process_response(request, response)
        
        # If we are in the admin path, we need to intercept the cookie
        if request.path.startswith('/admin/'):
            cookie_name = settings.SESSION_COOKIE_NAME
            
            # Check if the standard middleware set the session cookie
            if cookie_name in response.cookies:
                # Rename the cookie in the response to our admin cookie name
                # SimpleCookie stores Morsel objects. We can move the morsel to a new key.
                morsel = response.cookies[cookie_name]
                
                # Create a new cookie with the admin name
                response.cookies[self.ADMIN_SESSION_COOKIE_NAME] = morsel.value
                new_morsel = response.cookies[self.ADMIN_SESSION_COOKIE_NAME]
                
                # Copy all attributes (path, domain, secure, httponly, etc.)
                for key in morsel.keys():
                    if morsel[key]:
                        new_morsel[key] = morsel[key]
                
                # Remove the original cookie so it doesn't overwrite the main site session
                del response.cookies[cookie_name]
                
        return response
