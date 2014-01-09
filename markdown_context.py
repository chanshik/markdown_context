"""
Convert markdown context to JSON.

Project A
=========

Task A
------

Note A


convert to JSON.

{
    "projects": [
        {
            "name": "Project A",
            "tasks": [
                {
                    "name": "Task A",
                    "notes": [
                        {
                            "paragraph": "It's a note.\n
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
        self.re_project = re.compile(r"=====+")
        self.re_task = re.compile(r"-----+")
        self.obj = dict(projects=list())
        self.cur_prj = None
        self.cur_task = None

    def parse(self, md):
        lines = md.split("\n")
        notes = []

        for i in range(len(lines)):
            # Each paragraph separated by empty line.
            if lines[i].strip() == "":
                if self.cur_prj and self.cur_task and len(notes) > 0:
                    self.add_note("\n".join(notes), self.cur_task)

                    notes = []
                continue

            if self.cur_prj and self.cur_task:
                notes.append(lines[i])

            is_prj = self.find_and_add_project(lines, i)
            is_task = self.find_and_add_task(lines, i)

            if (is_prj or is_task) and len(notes) > 0:
                # Remove 2 lines before current line.
                #   Title   Name
                #   =====   ----
                #   --> Current line position.
                notes.pop()
                notes.pop()

        return self.obj

    def get_note(self):
        return self.obj

    def find_and_add_project(self, lines, idx):
        if self.re_project.match(lines[idx]):
            return self.add_project(lines[idx - 1])
        else:
            return None

    def add_project(self, title):
        exist_prj = False
        for prj in self.obj["projects"]:
            if title == prj["name"]:
                exist_prj = True

                self.cur_prj = prj
                break

        if exist_prj is False:
            self.obj["projects"].append({
                "name": title,
                "tasks": list()
            })
            # Last element is recently added project.
            self.cur_prj = self.obj["projects"][-1]

        return self.cur_prj

    def find_and_add_task(self, lines, idx):
        if self.re_task.match(lines[idx]):
            if self.cur_prj is None:
                # Add default 'projects'
                self.cur_prj = self.add_project("untitled")

            return self.add_task(self.cur_prj, lines[idx - 1])
        else:
            return None

    def add_task(self, prj, name):
        exist_task = False
        for task in prj["tasks"]:
            if name == task["name"]:
                exist_task = True

                self.cur_task = task
                break

        if exist_task is False:
            prj["tasks"].append({
                "name": name,
                "notes": list()
            })

            self.cur_task = prj["tasks"][-1]

        return self.cur_task

    @staticmethod
    def add_note(note, task):
        task["notes"].append(note)

    def export(self, md_obj=None):
        if md_obj is None:
            md_obj = self.obj

        if not isinstance(md_obj, dict):
            return None

        if "projects" not in md_obj:
            return None

        result = ""
        for project in md_obj["projects"]:
            if "name" not in project or "tasks" not in project:
                continue

            result += project["name"] + "\n"
            result += "=" * len(project["name"]) + "\n\n"

            for task in project["tasks"]:
                if "name" not in task or "notes" not in task:
                    continue

                result += task["name"] + "\n"
                result += "-" * len(task["name"]) + "\n\n"
                for note in task["notes"]:
                    result += note + "\n"

        return result
