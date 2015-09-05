from django.conf import settings
from django.contrib.auth import BACKEND_SESSION_KEY, SESSION_KEY, get_user_model
from django.contrib.sessions.backends.db import SessionStore

from .base import FunctionalTest


"""
The intent of this test is set up a pre-authenticated session, using cookies.
(TDD with Python, page 304)

We create a session object in the database. (The session key is the PK of the
user object.)

We then add a cookie to the browser that matches the session on the server, so
on our next visit to the site, the server should recognize us as a logged-in
user.

Note tat, as it is, this will only work because FunctionalTest inherits from
LiveServerTestCase, so the User and Session objects we create will end up in
the same database as the test server.

Later we'll need to modify it so that it works against the datbase of the
staging server too.

"""

User = get_user_model()
class MyListsTest(FunctionalTest):
  
    def create_pre_authenticated_session(self, email):
        user = User.objects.create(email=email)
        session = SessionStore()
        session[SESSION_KEY] = user.pk
        session[BACKEND_SESSION_KEY] =  settings.AUTHENTICATION_BACKENDS[0]
        session.save()
        ## to set a cookie we need to first visit the domain.
        ## 404 pages load the quickest!
        self.browser.get(self.server_url + "/404_no_such_url")
        self.browser.add_cookie(dict(
            name=settings.SESSION_COOKIE_NAME,
            value=session.session_key,
            path='/',
        ))

    def test_logged_in_users_lists_are_saved_as_my_lists(self):
        email = 'edith@example.com'

        self.browser.get(self.server_url)
        self.wait_to_be_logged_out(email)

        # Edith is a logged-in user
        self.create_pre_authenticated_session(email)

        self.browser.get(self.server_url)
        self.wait_to_be_logged_in(email)
