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

class Markdown(object):
    def __init__(self):
        pass
