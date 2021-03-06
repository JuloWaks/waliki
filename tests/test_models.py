#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import mock
from django.test import TestCase
from waliki.models import Page
from waliki.settings import deep_update
from waliki import settings


rst = """
Title
=====

some rst markup
"""

rst_html = """\n    <h2>Title</h2>\n    <p>some rst markup</p>\n"""

md = """
# Hi

I'm Markdown
"""

md_html = """<h2 id="hi">Hi</h2>\n<p>I'm Markdown</p>\n"""


class TestPage(TestCase):

    def test_content_saved_on_attribute_set(self):
        page = Page(path='test.rst')
        page.raw = rst
        path = os.path.join(settings.WALIKI_DATA_DIR, 'test.rst')
        self.assertEqual(page.abspath, path)
        self.assertTrue(os.path.exists(path))
        content = open(path).read()
        self.assertEqual(content, rst)

    def test_raw_empty_if_file_doesnt_exist(self):
        page = Page(path='test3.rst')
        assert not os.path.exists(page.abspath)
        self.assertEqual(page.raw, "")

    def test_path_populated_from_slug_if_not_given(self):
        page = Page(slug='some/slug')
        page.save()
        self.assertEqual(page.path, 'some/slug.rst')

    def test_slug_strip_slashes(self):
        page = Page(slug='/some/slug/')
        page.save()
        self.assertEqual(page.slug, 'some/slug')


class TestRestructuredText(TestCase):

    def test_body(self):
        page = Page(path='test.rst')
        page.raw = rst
        self.assertEqual(page.body, rst_html)

    def test_preview(self):
        self.assertEqual(Page.preview('reStructuredText', rst), rst_html)

    def test_link_explicit(self):
        with mock.patch('waliki._markups.get_url') as get_url:
            get_url.return_value = 'xxx'
            html = Page.preview('reStructuredText', 'a link_')
        self.assertEqual(html, '\n    <p>a <a href="xxx">link</a></p>\n')


class TestMarkdown(TestCase):

    def test_body(self):
        page = Page(path='test.md', markup='Markdown')
        page.raw = md
        self.assertEqual(page.body, md_html)

    def test_preview(self):
        self.assertEqual(Page.preview('Markdown', md), md_html)

    def test_link_explicit(self):
        s = settings.WALIKI_MARKUPS_SETTINGS.get('Markdown')
        s['extension_configs']['wikilinks']['build_url'] = mock.Mock(return_value='xxx')
        with mock.patch('waliki.models.settings') as s_mock:
            s_mock.WALIKI_MARKUPS_SETTINGS.get.return_value = s
            html = Page.preview('Markdown', 'a [[Link]]')
        self.assertEqual(html, '<p>a <a class="wikilink" href="xxx">Link</a></p>\n')


class TestMarkupSettings(TestCase):

    def test_deep_update(self):
        d = {'reStructuredText': {
                'settings_overrides': {              # noqa
                        'initial_header_level': 2,
                        'record_dependencies': True}
                },
             'Markdown': ['...']
             }
        u = {'reStructuredText': {
                'settings_overrides': {              # noqa
                        'initial_header_level': 1
            }}}
        expected = {'reStructuredText': {
                    'settings_overrides': {              # noqa
                        'initial_header_level': 1,
                        'record_dependencies': True}
                }, 'Markdown': ['...']
             }
        self.assertEqual(deep_update(d, u), expected)
