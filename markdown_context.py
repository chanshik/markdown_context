"""
Convert markdown context to JSON.

Document A
==========

Subject A
----------

Context A


convert to JSON.

{
    "documents": [
        {
            "title": "Document A",
            "subjects": [
                {
                    "title": "Subject A",
                    "contexts": [
                        {
                            "paragraph": "Context A\n
                        }
                    ]
                }
            ]
        }
    ]
}
"""

import re


class MarkdownContext(object):
    def __init__(self):
        self.re_document = re.compile(r"=====+")
        self.re_subject = re.compile(r"-----+")
        self.obj = dict(documents=list())
        self.cur_doc = None
        self.cur_sub = None

    def parse(self, md):
        lines = md.split("\n")
        paragraph = []

        for i in range(len(lines)):
            if lines[i].strip() == "":
                if self.cur_doc and self.cur_sub and len(paragraph) > 0:
                    self.add_context("\n".join(paragraph), self.cur_doc, self.cur_sub)

                    paragraph = []
                continue

            if self.cur_doc and self.cur_sub:
                paragraph.append(lines[i])

            is_doc = self.find_and_add_document(lines, i)
            is_sub = self.find_and_add_subject(lines, i)

            if (is_doc or is_sub) and len(paragraph) > 0:
                # Remove 2 lines before current line.
                #   Title   Subject
                #   =====   -------
                #   --> Current line position.
                paragraph.pop()
                paragraph.pop()

        return self.obj

    def get_context(self):
        return self.obj

    def find_and_add_document(self, lines, idx):
        if self.re_document.match(lines[idx]):
            return self.add_document(lines[idx - 1])
        else:
            return None

    def add_document(self, title):
        exist_doc = False
        for doc in self.obj["documents"]:
            if title == doc["title"]:
                exist_doc = True

                self.cur_doc = doc
                break

        if exist_doc is False:
            self.obj["documents"].append({
                "title": title,
                "subjects": list()
            })

            self.cur_doc = self.obj["documents"][-1]

        return self.cur_doc


    def find_and_add_subject(self, lines, idx):
        if self.re_subject.match(lines[idx]):
            if self.cur_doc is None:
                # Add default 'document'
                self.cur_doc = self.add_document("document")

            return self.add_subject(self.cur_doc, lines[idx - 1])
        else:
            return None

    def add_subject(self, doc, title):
        exist_sub = False
        for sub in doc["subjects"]:
            if title == sub["title"]:
                exist_sub = True

                self.cur_sub = sub
                break

        if exist_sub is False:
            doc["subjects"].append({
                "title": title,
                "contexts": list()
            })

            self.cur_sub = doc["subjects"][-1]

        return self.cur_sub

    def add_context(self, paragraph, doc, sub):
        sub["contexts"].append(paragraph)

    def export(self, md_obj=None):
        if md_obj is None:
            md_obj = self.obj

        result = ""
        for doc in md_obj["documents"]:
            result += doc["title"] + "\n"
            result += "=" * len(doc["title"]) + "\n\n"

            for sub in doc["subjects"]:
                result += sub["title"] + "\n"
                result += "-" * len(sub["title"]) + "\n\n"
                for para in sub["contexts"]:
                    result += para + "\n"

        return result
