import datetime
import jwt

from .helper import JOATTestCase, random_bytes, timestamp
from joat import JOAT

class TestTokenValidation(JOATTestCase):

  def setUp(self):
    super(TestTokenValidation, self).setUp()
    self.joat = JOAT("My OAuth2 Provider")
    self.joat.salt_generator = self.generate_salt

  def test_validate_token(self):
    valid_token = jwt.encode(self.jwt_claims, self.generate_salt(self.jwt_claims))

    token_data = self.joat.parse_token(valid_token)
    self.assertDictEqual(token_data, self.joat_payload)

  def test_validate_with_incorrect_salt(self):
    invalid_token = jwt.encode(self.jwt_claims, self.generate_wrong_salt(None))

    token_data = self.joat.parse_token(invalid_token)
    self.assertIsNone(token_data)