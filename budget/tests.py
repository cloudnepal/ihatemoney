import os
import tempfile
import unittest

from flask import g

import web
import models

class BudgetTestCase(unittest.TestCase):

    def test_notifications(self):
        """Test that the notifications are sent, and that email adresses
        are checked properly.
        """
        # create a project
        self.create_project("raclette")

        with web.app.test_client() as c:
            self.login("raclette", test_client=c)
            result = c.post("/raclette/invite", 
                    data={"emails": 'test@test.com'})
            # check here that the mails are sent.


    def login(self, project, password=None, test_client=None):
        password = password or project
        test_client = test_client or self.app

        return test_client.post('/authenticate', data=dict(
            id=project, password=password), follow_redirects=True)

    def create_project(self, name):
        """Create a fake project"""
        # create the project
        project = models.Project(id=name, name=unicode(name), password=name, 
                contact_email="%s@notmyidea.org" % name)
        models.db.session.add(project)
        models.db.session.commit()

        return project

    def setUp(self):
        web.app.config['TESTING'] = True

        self.fd, self.fp = tempfile.mkstemp()
        web.app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///%s" % self.fp
        web.app.config['CSRF_ENABLED'] = False # simplify the tests
        self.app = web.app.test_client()

        models.db.init_app(web.app)
        web.mail.init_app(web.app)

        models.db.app = web.app
        models.db.create_all()

    def tearDown(self):
        # clean after testing
        os.close(self.fd)
        os.unlink(self.fp)


if __name__ == "__main__":
    unittest.main()