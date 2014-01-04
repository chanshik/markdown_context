from unittest import TestCase
from markdown_context import MarkdownContext
import pprint


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
        self.assertEqual(3, len(obj["documents"][0]["subjects"][1]["contexts"]))

        subjects = obj["documents"][0]["subjects"]
        self.assertEqual(
            "[Markdown 1.0.1][dl] (18 KB) -- 17 Dec 2004",
            subjects[0]["contexts"][0])
        self.assertEqual(
            "Markdown",
            subjects[1]["contexts"][0].split(" ")[0])
        self.assertEqual(
            "Thus,",
            subjects[1]["contexts"][1].split(" ")[0])
        self.assertEqual(
            "  [syntax]: /projects/markdown/syntax",
            subjects[1]["contexts"][2].split("\n")[0])

    def test_parse_document_only(self):
        doc_only = """
Markdown
========
"""
        obj = self.md_context.parse(doc_only)

        self.assertEqual(1, len(obj["documents"]))

    def test_parse_document_and_subject_only(self):
        doc_and_sub_only = """
Markdown
========

Download
--------



Introduction
------------
"""
        obj = self.md_context.parse(doc_and_sub_only)

        self.assertEqual(1, len(obj["documents"]))
        self.assertEqual(2, len(obj["documents"][0]["subjects"]))

    def test_export(self):
        simple_md = """Markdown
========

Download
--------

Introduction
------------

This is a very simple markdown text.
Markdown is a text-to-HTML conversion tool for web writers.
"""
        obj = self.md_context.parse(simple_md)

        plain_text = self.md_context.export(obj)
        self.assertEqual(simple_md, plain_text)

        plain_text = self.md_context.export()
        self.assertEqual(simple_md, plain_text)

    def test_export_with_no_document(self):
        simple_md = """Download
--------

Introduction
------------
"""
        obj = self.md_context.parse(simple_md)
        md_text = self.md_context.export(obj)

        self.assertEqual("""document
========

Download
--------

Introduction
------------

""", md_text)

    def test_no_document(self):
        no_doc = """
Download
--------


Introduction
------------
"""
        obj = self.md_context.parse(no_doc)

        self.assertEqual(1, len(obj["documents"]))
        self.assertEqual(2, len(obj["documents"][0]["subjects"]))
        self.assertEqual("document", obj["documents"][0]["title"])

    def test_parse_with_separated_section(self):
        separated_md = """
Category A
========

Thing A
-------

"Thing A" in Category A

Thing B
-------

"Thing B" in Category A

Category B
==========

Thing C
-------

"Thing C" in Category B

Category A
==========

Thing A
-------

"Thing A" in another Category A

Category B
==========

Thing C
-------

"Thing C" in another Category B

Thing D
-------

"Thing D" in another Category B

"""
        obj = self.md_context.parse(separated_md)

        self.assertEqual(2, len(obj["documents"]))
        self.assertEqual(2, len(obj["documents"][0]["subjects"]))
        self.assertEqual(2, len(obj["documents"][1]["subjects"]))

    def test_parse_repeatable(self):
        md_a = """
Category A
==========

Thing A
-------

Task A
"""
        md_b = """
Category A
==========

Thing A
-------

Task B
"""

        self.md_context.parse(md_a)
        self.md_context.parse(md_b)

        obj = self.md_context.get_context()

        self.assertEqual(2, len(obj["documents"][0]["subjects"][0]["contexts"]))

    def test_export_with_invalid_object(self):
        self.assertIsNone(self.md_context.export([]))
        self.assertIsNone(self.md_context.export({}))
        self.assertEqual("", self.md_context.export({
            "documents": [
                {
                    "title": "Title"
                }
            ]
        }))
        self.assertEqual("""Title
=====

""", self.md_context.export({
            "documents": [
                {
                    "title": "Title",
                    "subjects": [
                        {
                            "title": "Subject Title"
                        }
                    ]
                }
            ]
        }))