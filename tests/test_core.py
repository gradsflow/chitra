import os
import subprocess

import tensorflow as tf

from chitra.core import get_basename
from chitra.core import load_imagenet_labels
from chitra.core import remove_dsstore


def test_remove_dsstore():
    os.makedirs('chitra_temp', exist_ok=True)
    subprocess.call('touch chitra_temp/.DS_Store', shell=True)
    remove_dsstore('chitra_temp')
    assert not os.path.exists('chitra_temp/.DS_Store')
    os.removedirs('chitra_temp')


def test_get_basename():
    assert get_basename(tf.constant('hello/world')) == 'world'


def test_load_imagenet_labels():
    labels = load_imagenet_labels()

    assert "\n" not in labels
    assert len(labels) == 1000 + 1
