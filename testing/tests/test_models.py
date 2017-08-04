from datetime import datetime

import pytest
from django.utils import timezone
from freezegun import freeze_time

from legaltext.models import LegalText, LegalTextVersion
from testing.factories import (
    LegalTextCheckboxFactory, LegalTextFactory, LegalTextVersionFactory)


@pytest.mark.django_db
class TestLegalText:

    def test_str(self):
        legal_text = LegalTextFactory.create(name='Foo Bar Text')
        assert str(legal_text) == 'Foo Bar Text'

    def test_current_version_no_version_yet(self):
        version = LegalText.current_version('test-version')
        assert isinstance(version, LegalTextVersion)
        assert version.legaltext.slug == 'test-version'
        assert version.legaltext.name == 'test-version'
        assert version.content == ''

    @freeze_time('2016-01-02')
    def test_current_version(self):
        legal_text = LegalTextFactory.create(name='Foo Bar Text', slug='foo-bar')

        LegalTextVersionFactory.create(
            legaltext=legal_text,
            valid_from=timezone.make_aware(datetime(2015, 1, 1, 10, 0)))
        version_present = LegalTextVersionFactory.create(
            legaltext=legal_text,
            valid_from=timezone.make_aware(datetime(2016, 1, 1, 10, 0)))
        LegalTextVersionFactory.create(
            legaltext=legal_text,
            valid_from=timezone.make_aware(datetime(2017, 1, 1, 10, 0)))

        version = LegalText.current_version('foo-bar')

        assert version.legaltext.slug == 'foo-bar'
        assert version.legaltext.name == 'Foo Bar Text'
        assert version.pk == version_present.pk

    def test_get_current_version_no_version_yet(self):
        legal_text = LegalTextFactory.create(name='Foo Bar Text')
        version = legal_text.get_current_version()
        assert isinstance(version, LegalTextVersion)
        assert version.legaltext.slug == 'foo-bar-text'
        assert version.legaltext.name == 'Foo Bar Text'
        assert version.content == ''

    @freeze_time('2016-01-02')
    def test_get_current_version(self):
        legal_text = LegalTextFactory.create(name='Foo Bar Text', slug='foo-bar-test')

        LegalTextVersionFactory.create(
            legaltext=legal_text,
            valid_from=timezone.make_aware(datetime(2015, 1, 1, 10, 0)),
            content='Test content 1')
        version_present = LegalTextVersionFactory.create(
            legaltext=legal_text,
            valid_from=timezone.make_aware(datetime(2016, 1, 1, 10, 0)),
            content='Test content 2')
        LegalTextVersionFactory.create(
            legaltext=legal_text,
            valid_from=timezone.make_aware(datetime(2017, 1, 1, 10, 0)),
            content='Test content 3')

        version = legal_text.get_current_version()
        assert isinstance(version, LegalTextVersion)
        assert version.legaltext.slug == 'foo-bar-test'
        assert version.legaltext.name == 'Foo Bar Text'
        assert version.content == 'Test content 2'
        assert version.pk == version_present.pk


@pytest.mark.django_db
class TestLegalTextVersion:

    def test_str(self):
        legal_text_version = LegalTextVersionFactory.create(legaltext__name='Foo Bar Text')
        assert 'Foo Bar Text' in str(legal_text_version)
        assert '{0:%x}'.format(legal_text_version.valid_from) in str(legal_text_version)

    def test_name(self):
        legal_text_version = LegalTextVersionFactory.create(legaltext__name='Foo Bar Text')
        assert legal_text_version.name == 'Foo Bar Text'

    def test_render_content(self):
        legal_text_version = LegalTextVersionFactory.create(content='Text Text Text')
        assert legal_text_version.render_content() == '<p>Text Text Text</p>'

    def test_render_content_with_anchor(self):
        legal_text_version = LegalTextVersionFactory.create(
            content='Text [block:foo]Text[/block] Text [block:bar]Text bar[/block]')

        assert legal_text_version.render_content() == (
            '<p>Text <div class="legaltext-block legaltext-block-foo"><span id="foo">'
            '</span><p>Text</p></div> Text <div class="legaltext-block legaltext-block-bar">'
            '<span id="bar"></span><p>Text bar</p></div></p>'
        )


@pytest.mark.django_db
class TestLegalTextCheckbox:

    def test_str(self):
        checkbox = LegalTextCheckboxFactory.create(
            legaltext_version__legaltext__name='Foo Bar Text')

        assert 'Checkbox' in str(checkbox)
        assert checkbox.legaltext_version.name in str(checkbox)
        assert '{0:%x}'.format(checkbox.legaltext_version.valid_from) in str(checkbox)

    def test_render_content(self):
        checkbox = LegalTextCheckboxFactory.create(content='Checkbox test text', )
        assert checkbox.render_content() == 'Checkbox test text'

    @pytest.mark.xfail
    def test_render_content_with_link(self):
        checkbox = LegalTextCheckboxFactory.create(
            content='Checkbox [[test]] text', anchor='',
            legaltext_version__legaltext__slug='test-1')

        assert checkbox.render_content() == (
            'Checkbox <a href="/test-1/" title="test">test</a> text')

    def test_render_content_with_link_and_anchor(self):
        checkbox = LegalTextCheckboxFactory.create(
            legaltext_version__legaltext__slug='test-2',
            content='Text [anchor:foo]Text[/anchor] Text [anchor]bar[/anchor]')

        assert checkbox.render_content() == (
            'Text <a href="/test-2/#foo" class="legaltext-anchor" target="_blank">Text'
            '</a> Text <a href="/test-2/" class="legaltext-anchor" target="_blank">bar</a>'
        )