from datetime import datetime, timedelta

from django.contrib.sessions.models import Session


class OneSessionPerUserMiddleware:
    # Called only once when the web server starts
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user

        # Code to be executed for each request before
        # the view (and later middleware) are called.
        if user.is_authenticated and hasattr(user, 'logged_in_user'):
            stored_session_key = user.logged_in_user.session_key

            # if there is a stored_session_key  in our database and it is
            # different from the current session, delete the stored_session_key
            # session_key with from the Session table
            if stored_session_key and stored_session_key != request.session.session_key:
                try:
                    Session.objects.get(session_key=stored_session_key).delete()
                except Session.DoesNotExist:
                    pass

            user.logged_in_user.session_key = request.session.session_key
            user.logged_in_user.save()

        response = self.get_response(request)

        # This is where you add any extra code to be executed for each request/response after
        # the view is called.
        # For this tutorial, we're not adding any code so we just return the response

        return response


class AutoLogout:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            # If the user is not authenticated, no need to check for inactivity.
            return self.get_response(request)

        # Check if 'last_touch' is in the session.
        if 'last_touch' in request.session:
            last_touch = datetime.strptime(request.session['last_touch'], '%Y-%m-%d %H:%M:%S')
            if datetime.now() - last_touch > timedelta(minutes=5):
                # If it's been more than 5 minutes, delete the current session.
                Session.objects.get(session_key=request.session.session_key).delete()
                request.session.flush()  # Delete current session cookie.
        else:
            # Otherwise, set 'last_touch' to the current time.
            request.session['last_touch'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        response = self.get_response(request)
        return response
