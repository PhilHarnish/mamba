# -*- coding: utf-8 -*-

import inspect

from mamba.example_group import ExampleGroup
from mamba.example import Example

class Loader(object):

    def load_examples_from(self, module):
        loaded = []
        example_groups = self._example_groups_for(module)

        for klass in example_groups:
            example_group = self._create_example_group(klass)
            self._load_hooks(klass, example_group)
            self._load_examples(klass, example_group)
            loaded.append(example_group)

        return loaded

    def _example_groups_for(self, module):
        return [klass for name, klass in inspect.getmembers(module, inspect.isclass) if name.endswith('__description')]

    def _create_example_group(self, klass):
        return ExampleGroup(self._name_for(klass))

    def _name_for(self, example_group):
        return example_group.__name__.replace('__description', '')

    def _load_hooks(self, klass, example_group):
        for hook in self._hooks_in(klass):
            example_group.hooks[hook.__name__].append(hook)

    def _hooks_in(self, example_group):
        return [method for name, method in inspect.getmembers(example_group, inspect.ismethod) if name.startswith('before')]

    def _load_examples(self, klass, example_group):
        for example in self._examples_in(klass):
            example_group.append(Example(example))

    def _examples_in(self, example_group):
        return [method for name, method in inspect.getmembers(example_group, inspect.ismethod) if name.startswith('it')]

