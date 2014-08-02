from calendar import timegm
import datetime
import hashlib
import jwt
import os
import unittest

def timestamp(from_datetime):
  return timegm(from_datetime.utctimetuple())

def random_bytes():
  return hashlib.sha1(os.urandom(128)).digest()


class JOATTestCase(unittest.TestCase):

  test_iat_datetime = datetime.datetime.utcnow()
  test_iat_timestamp = timestamp(test_iat_datetime)
  test_exp_timedelta = datetime.timedelta(minutes=90)
  test_exp_timestamp = timestamp(test_iat_datetime+test_exp_timedelta)

  def generate_salt(cls, claims):
    """Use a constant salt for testing"""
    return '\xdaFw\xfb8\x9f\x9a\xb0\x87\xd3X2J!\x90\x1f\x05\xd6\xa5W'

  def generate_wrong_salt(cls, claims):
    """Return the wrong salt for testing"""
    return '\xbb4;\xc7\xb2Vn\xa5\xb7\xb0^\xc6J%\x1d\x90\xb8Ik:'

  def setUp(self):
    self.jwt_header = {
      'typ': 'JWT',
      'alg': 'HS256'
    }
    self.jwt_claims = {
      'iss': 'My OAuth2 Provider',
      'aud': 'abc123DEF', # The application's client_id
      'sub': '12345', # The resource owner's user_id
      'scope': ['email', 'profile'],
      'iat': self.test_iat_timestamp,
      'exp': self.test_exp_timestamp
    }

    self.jwt_token = jwt.encode(self.jwt_claims, self.generate_salt(self.jwt_claims))

    self.joat_payload = {
      'client': {
        'id': 'abc123DEF',
        'name': 'My OAuth2 Provider'
      },
      'user_id': '12345',
      'authorized_scope': ['email', 'profile']
    }