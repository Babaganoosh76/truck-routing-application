from app import app
from werkzeug.security import check_password_hash

class User():

  def __init__(self, username):
    self.username = username
    self.email = None

  def is_authenticated(self):
    return True

  def is_active(self):
    return True

  def is_anonymous(self):
    return False

  def get_id(self):
    return self.username

# def get_DBEntry(self):
#     return app.config['USERS_COLLECTION'].find_one({"_id": self.username})

# def get_posts(self):
#     DB = self.get_DBEntry()
#     return DB["data"]["posts"]

# def write_post(self, post):
#     app.config['USERS_COLLECTION'].update_one({"_id":self.username},{"$push" : {"data.posts" : post }},upsert=False)

# def deleteAllPosts(self):
#     app.config['USERS_COLLECTION'].update_one({"_id":self.username},{"$set" : {"data.posts" : [] }},upsert=False)

  @staticmethod
  def validate_login(password_hash, password):
    return check_password_hash(password_hash, password)