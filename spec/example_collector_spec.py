# -*- coding: utf-8 -*-
from mamba import description, context, it
from expects import expect, be_true, have_length, equal, be_a, have_property, be_none

import os
import inspect

from mamba import example, example_group, loader
from mamba.example_collector import ExampleCollector


def spec_relpath(name):
    return os.path.join('spec', 'fixtures', name)


def spec_abspath(name):
    return os.path.join(os.path.dirname(__file__), 'fixtures', name)


IRRELEVANT_PATH = spec_abspath('without_inner_contexts.py')
PENDING_DECORATOR_PATH = spec_abspath('with_pending_decorator.py')
PENDING_DECORATOR_AS_ROOT_PATH = spec_abspath('with_pending_decorator_as_root.py')
WITH_RELATIVE_IMPORT_PATH = spec_abspath('with_relative_import.py')
WITH_TAGS_PATH = spec_abspath('with_tags.py')
WITH_FOCUS_PATH = spec_abspath('with_focus.py')


def _load_module(path):
    example_collector = ExampleCollector([path])
    return list(example_collector.modules())[0]


with description(ExampleCollector):
    with context('when loading from file'):
        with it('loads module from absolute path'):
            module = _load_module(IRRELEVANT_PATH)

            expect(inspect.ismodule(module)).to(be_true)

        with it('loads module from relative path'):
            module = _load_module(spec_relpath('without_inner_contexts.py'))

            expect(inspect.ismodule(module)).to(be_true)

    #FIXME: Mixed responsabilities in test [collect, load]??
    with context('when loading'):
        with it('orders examples by line number'):
            module = _load_module(spec_abspath('without_inner_contexts.py'))

            examples = loader.Loader().load_examples_from(module)

            expect(examples).to(have_length(1))
            expect([example.name for example in examples[0].examples]).to(equal(['it first example', 'it second example', 'it third example']))

        with it('places examples together and groups at the end'):
            module = _load_module(spec_abspath('with_inner_contexts.py'))

            examples = loader.Loader().load_examples_from(module)

            expect(examples).to(have_length(1))
            expect([example.name for example in examples[0].examples]).to(equal(['it first example', 'it second example', 'it third example', '#inner_context']))

    with context('when reading tags'):
        with it('reads tags from description parameters'):
            module = _load_module(WITH_TAGS_PATH)

            examples = loader.Loader().load_examples_from(module)

            expect(examples).to(have_length(1))
            expect(examples[0].has_tag('integration')).to(be_true)

        with it('reads tags from spec parameters'):
            module = _load_module(WITH_TAGS_PATH)

            examples = loader.Loader().load_examples_from(module)
            spec = next(iter(examples[0]))

            expect(spec).not_to(be_none)
            expect(spec.has_tag('unit')).to(be_true)

    with context('when reading focus'):
        with it('adds focus tag to spec'):
            module = _load_module(WITH_FOCUS_PATH)

            examples = loader.Loader().load_examples_from(module)
            spec = next(iter(examples[0]))

            expect(spec).not_to(be_none)
            expect(spec.has_tag('focus')).to(be_true)
            expect(spec.has_tag('unit')).to(be_true)

        with it('adds focus to context'):
            module = _load_module(WITH_FOCUS_PATH)

            examples = loader.Loader().load_examples_from(module)

            expect(examples).to(have_length(2))
            expect(examples[1].has_tag('focus')).to(be_true)
            expect(examples[1].has_tag('integration')).to(be_true)

    with context('when a pending decorator loaded'):
        with it('mark example as pending'):
            module = _load_module(PENDING_DECORATOR_PATH)

            examples = loader.Loader().load_examples_from(module)

            expect(examples).to(have_length(1))
            expect(examples[0].examples[0]).to(be_a(example.PendingExample))

        with it('marks example group as pending'):
            module = _load_module(PENDING_DECORATOR_PATH)

            examples = loader.Loader().load_examples_from(module)

            expect(examples).to(have_length(1))
            expect(examples[0].examples[1]).to(be_a(example_group.PendingExampleGroup))

    with context('when a pending decorator loaded_as_root'):
        with it('mark inner examples as pending'):
            module = _load_module(PENDING_DECORATOR_AS_ROOT_PATH)

            examples = loader.Loader().load_examples_from(module)

            expect(examples).to(have_length(1))
            examples_in_root = examples[0].examples

            expect(examples_in_root).to(have_length(2))
            expect(examples_in_root[0]).to(be_a(example.PendingExample))
            expect(examples_in_root[1]).to(be_a(example_group.PendingExampleGroup))
            expect(examples_in_root[1].examples[0]).to(be_a(example.PendingExample))

    with context('when loading with relative import'):
        with it('loads module and perform relative import'):
            module = _load_module(WITH_RELATIVE_IMPORT_PATH)

            expect(module).to(have_property('HelperClass'))
