import sys

sys.path.append('./src')
sys.path.append('./test')

from strong_config_core.base_plugin import BasePlugin
from strong_config_core.main import load_config
import pytest
import os
from schematics.models import Model
from schematics.types import StringType, ModelType
from schematics.exceptions import DataError


class PersonSchema(Model):
  name = StringType(required=True)


class Schema(Model):
  person = ModelType(PersonSchema)


class TestPlugin(BasePlugin):

  def protocol(self):
    return 'test'

  def get_value(self, key: str):
    return 'dummy value'


def test_loads_empty(fs):
  os.environ['PYTHON_ENV'] = 'test'
  default_config_file = ''
  fs.create_file('/config/default.yml', contents=default_config_file)
  config = load_config(Schema, config_dir='/config')
  assert config.person == None


def test_override(fs):
  os.environ['PYTHON_ENV'] = 'test'
  default_config_file = '''
  person:
    name: Alice
  '''
  override_config_file = '''
  person:
    name: Bob
  '''
  fs.create_file('/config/default.yml', contents=default_config_file)
  fs.create_file('/config/test.yml', contents=override_config_file)
  config = load_config(Schema, config_dir='/config')
  assert config.person.name == 'Bob'


def test_default_config_sad():
  os.environ['PYTHON_ENV'] = 'test'
  with pytest.raises(Exception) as e:
    load_config()
    assert str(e).startswith('Failed to find the default configuration file')


def test_python_env_sad():
  with pytest.raises(Exception) as e:
    load_config()
    assert str(e) == 'PYTHON_ENV environment variable is not defined'


def test_plugin(fs):
  os.environ['PYTHON_ENV'] = 'test'
  default_config_file = '''
  person:
    name: ${test:name}
  '''
  fs.create_file('/config/default.yml', contents=default_config_file)
  config = load_config(Schema, config_dir='/config', plugins=[TestPlugin()])
  assert config.person.name == 'dummy value'


def test_validation(fs):
  os.environ['PYTHON_ENV'] = 'test'
  default_config_file = '''
  person:
    name: Alice
  '''
  fs.create_file('/config/default.yml', contents=default_config_file)
  config = load_config(Schema, config_dir='/config', plugins=[TestPlugin()])
  assert config.person.name == 'Alice'


def test_validation_sad(fs):
  os.environ['PYTHON_ENV'] = 'test'
  default_config_file = '''
  person:
    hello: world
  '''
  fs.create_file('/config/default.yml', contents=default_config_file)
  with pytest.raises(DataError) as e:
    load_config(Schema, config_dir='/config', plugins=[TestPlugin()])
    assert e == {'person': {'hello': 'Rogue field'}}