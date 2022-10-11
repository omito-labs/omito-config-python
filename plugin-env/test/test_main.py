from schematics.models import Model
from schematics.types import StringType
from omito_config_plugin_env import EnvPlugin
from omito_config_core import load_config
import os
import pytest


class Schema(Model):
  name = StringType(required=True)


def test_env_plugin(fs):
  os.environ['PYTHON_ENV'] = 'test'
  os.environ['NAME'] = 'Bob'
  default_config_file = '''
  name: ${env:NAME}
  '''
  fs.create_file('/config/default.yml', contents=default_config_file)
  config = load_config(Schema, config_dir='/config', plugins=[EnvPlugin()])
  assert config.name == 'Bob'


def test_env_plugin_not_defined(fs):
  os.environ['PYTHON_ENV'] = 'test'
  default_config_file = '''
  name: ${env:NAME}
  '''
  fs.create_file('/config/default.yml', contents=default_config_file)
  with pytest.raises(Exception) as e:
    load_config(Schema, config_dir='/config', plugins=[EnvPlugin()])
    assert str(e) == 'Environment variable NAME is not defined'