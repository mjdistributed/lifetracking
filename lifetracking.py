import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.api import mail

import jinja2
import webapp2


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

DEFAULT_DB_NAME = 'db'


# We set a parent key on the 'Data' to ensure that they are all in the same
# entity group. Queries across the single entity group will be consistent.
# However, the write rate should be limited to ~1/second.

def data_key(db_name=DEFAULT_DB_NAME):
    """Constructs a Datastore key for a data entity with db_name."""
    return ndb.Key('Data', db_name)


class Data(ndb.Model):
    """Models an individual Data entry with author, content, and date."""
    author = ndb.UserProperty()
    steps = ndb.IntegerProperty(indexed=False)
    milesRun = ndb.FloatProperty(indexed=False)
    cupsCoffee = ndb.IntegerProperty(indexed=False)
    cupsWater = ndb.IntegerProperty(indexed=False)
    foodHealthiness = ndb.IntegerProperty(indexed=False)
    dollarsSpent = ndb.FloatProperty(indexed=False)
    mood = ndb.IntegerProperty(indexed=False)
    productivity = ndb.IntegerProperty(indexed=False)
    energy = ndb.IntegerProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)


class MainPage(webapp2.RequestHandler):

    def get(self):
        db_name = self.request.get('db_name',DEFAULT_DB_NAME)
        data_query = Data.query(ancestor=data_key(db_name)).order(-Data.date)
        data = data_query.fetch(10)

        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        template_values = {
            'data': data,
            'db_name': urllib.quote_plus(db_name),
            'url': url,
            'url_linktext': url_linktext,
        }

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))


class LifeTracking(webapp2.RequestHandler):

    def post(self):
        # We set the same parent key on the 'Data' to ensure each Data
        # is in the same entity group. Queries across the single entity group
        # will be consistent. However, the write rate to a single entity group
        # should be limited to ~1/second.
        data_name = self.request.get('data_name', DEFAULT_DB_NAME)
        data = Data(parent=data_key(data_name))

        if users.get_current_user():
            data.author = users.get_current_user()

        content = self.request.get('content').split()
        data.steps = int(self.request.get('steps'))
        data.milesRun = float(self.request.get('milesRun'))
        data.cupsCoffee = int(self.request.get('cupsCoffee'))
        data.cupsWater = int(self.request.get('cupsWater'))
        data.foodHealthiness = int(self.request.get('foodHealthiness'))
        data.dollarsSpent = float(self.request.get('dollarsSpent'))
        data.mood = int(self.request.get('mood'))
        data.productivity = int(self.request.get('productivity'))
        data.energy = int(self.request.get('energy'))
        data.put()

        query_params = {'data_name': data_name}
        self.redirect('/?' + urllib.urlencode(query_params))

class EmailReminder(webapp2.RequestHandler):

    def get(self):
        mail.send_mail(sender="me <mmjbot@gmail.com>",
              to="Matt Johnson <mmjbot@gmail.com>",
              subject="Test Email",
              body="omg yay this is working! Next email coming in 5 minutes")


application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/sign', LifeTracking),
    ('/tasks/email_reminder', EmailReminder)
], debug=True)