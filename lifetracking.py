import os
import urllib
import cgi

from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.api import mail

# from google.appengine.ext import blobstore
# from google.appengine.ext.webapp import blobstore_handlers

import jinja2
import webapp2


MAIN_PAGE_FOOTER_TEMPLATE = """\
    <form action = "%s" method="post" enctype="multipart/form-data">
            Upload File: <input type="file" name="file"><br> 
            <input type="submit" name="submit" value="Submit">
    </form>
    <hr>
    <a href="%s">%s</a>
  </body>
</html>
"""

DEFAULT_GUESTBOOK_NAME = 'default_guestbook'

# We set a parent key on the 'Greetings' to ensure that they are all in the same
# entity group. Queries across the single entity group will be consistent.
# However, the write rate should be limited to ~1/second.

def guestbook_key(guestbook_name=DEFAULT_GUESTBOOK_NAME):
    """Constructs a Datastore key for a Guestbook entity with guestbook_name."""
    return ndb.Key('Guestbook', guestbook_name)

# [START greeting]
class Greeting(ndb.Model):
    """Models an individual Guestbook entry."""
    author = ndb.UserProperty()
    content = ndb.StringProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)
# [END greeting]

# [START main_page]
class MainPage(webapp2.RequestHandler):
    def get(self):
        upload_url = "hello"
        # upload_url = blobstore.create_upload_url('/upload')
        self.response.write('<html><body>')
        # Checks for active Google account session
        user = users.get_current_user()
        if user:
            self.response.write('Hello, ' + user.nickname())
        else:
            self.redirect(users.create_login_url(self.request.uri))
        url = users.create_logout_url(self.request.uri)
        url_linktext = 'Logout'

        # Write the submission form and the footer of the page
        self.response.write(MAIN_PAGE_FOOTER_TEMPLATE % (upload_url, url, url_linktext))

# [END main_page]

# [START UploadHandler]
# class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
#     def post(self):
        # upload_files = self.get_uploads('file')
        # blob_info = upload_files[0]
        # blob_reader = blobstore.BlobReader(blob_info.key())
        # json_data = blob_reader.read()
        # reporter_file = ReporterFile()
        # reporter_file.filename = blob_info.all().get().filename
        # reporter_file.author = users.get_current_user()
        # reporter_file.uploaded_file = json_data
        # reporter_file.put()
        # self.redirect("/get_my_data")
# [END UPloadHandler]


class GetMyData(webapp2.RequestHandler):
    def get(self):
        self.response.write('<html><body>')
        user = users.get_current_user()
        if user:
            self.response.write('My Uploaded Data: </br>')
            data_query = ReporterFile.query().order(-ReporterFile.upload_date)
            data = data_query.fetch()
            for data_file in data:
                self.response.write(str(data_file.filename) + " Uploaded on " + str(data_file.upload_date) + "</br>")
                self.response.write(data_file.uploaded_file)
                self.response.write("</br>")
        else:
            self.redirect(users.create_login_url(self.request.uri))

class ReporterFile(ndb.Model):
    """Models an uploaded reporter file."""
    author = ndb.UserProperty()
    filename = ndb.StringProperty()
    # uploaded_file = ndb.BlobProperty()
    upload_date = ndb.DateTimeProperty(auto_now_add=True)
        
# [END UploadData]

application = webapp2.WSGIApplication([
    ('/', MainPage),
    # ('/upload', UploadHandler),
    ('/get_my_data', GetMyData)
], debug=True)




# JINJA_ENVIRONMENT = jinja2.Environment(
#     loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
#     extensions=['jinja2.ext.autoescape'],
#     autoescape=True)

# DEFAULT_DB_NAME = 'db'


# class MainPage(webapp2.RequestHandler):

#     def get(self):
#         # Checks for active Google account session
#         if users.get_current_user():
#             url = users.create_logout_url(self.request.uri)
#             url_linktext = 'Logout'
#         else:
#             url = users.create_login_url(self.request.uri)
#             url_linktext = 'Login'
#         # if user:
#         #     self.response.headers['Content-Type'] = 'text/plain'
#         #     self.response.write('Hello, ' + user.nickname())
#         # else:
#         #     self.redirect(users.create_login_url(self.request.uri))


# class EmailReminder(webapp2.RequestHandler):

#     def get(self):
#         """email reminders to each user to log their daily data"""
#         db_name = self.request.get('db_name',DEFAULT_DB_NAME)
#         data_query = Data.query(ancestor=data_key(db_name)).order(-Data.date)
#         user_set = set()
#         for row in data_query:
#             user_set.add(row.author)
#         for curr_user in user_set:
#             mail.send_mail(sender="me <mmjbot@gmail.com>",
#                   to=curr_user.nickname() + " " + curr_user.email(),
#                   subject="Track Your Life!",
#                   body="""
#                   This is your daily reminder to track your life! Fill out the survey at http://matt-ravi-lifetracking.appspot.com/
#                   """)


# application = webapp2.WSGIApplication([
#     ('/', MainPage),
#     ('/tasks/email_reminder', EmailReminder)
# ], debug=True)