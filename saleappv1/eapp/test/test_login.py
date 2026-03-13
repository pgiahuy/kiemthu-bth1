import hashlib

from eapp.dao import add_user
from eapp.models import User
import pytest
from eapp.test.test_base import test_session, test_app, create_app