from unittest import TestCase
from markdown_to_json import MarkdownContext


class TestMarkdown(TestCase):
    def setUp(self):
        self.md_context = MarkdownContext()
        self.md = """
Markdown
========

Download
--------

[Markdown 1.0.1][dl] (18 KB) -- 17 Dec 2004

[dl]: http://daringfireball.net/projects/downloads/Markdown_1.0.1.zip


Introduction
------------

Markdown is a text-to-HTML conversion tool for web writers. Markdown
allows you to write using an easy-to-read, easy-to-write plain text
format, then convert it to structurally valid XHTML (or HTML).

Thus, "Markdown" is two things: (1) a plain text formatting syntax;
and (2) a software tool, written in Perl, that converts the plain text
formatting to HTML. See the [Syntax][] page for details pertaining to
Markdown's formatting syntax. You can try it out, right now, using the
online [Dingus][].

  [syntax]: /projects/markdown/syntax
  [dingus]: /projects/markdown/dingus
"""

    def tearDown(self):
        pass

    def test_parse(self):
        obj = self.md_context.parse(self.md)

        self.assertIsNotNone(obj)
        self.assertEqual(1, len(obj["documents"]))
        self.assertEqual("Markdown", obj["documents"][0]["title"])

        self.assertEqual(2, len(obj["documents"][0]["subjects"]))
        self.assertEqual("Download", obj["documents"][0]["subjects"][0]["title"])
        self.assertEqual("Introduction", obj["documents"][0]["subjects"][1]["title"])