import json
import os


class Storage:

    def __init__(self, filename):
        self.filename = filename
        self.path_dict = dict()
        if os.path.exists(filename):
            with open(filename) as f:
                json_text = f.read()
                if json_text != "":
                    self.path_dict = json.loads(json_text)

    def get(self, path):
        if path in self.path_dict:
            return self.path_dict[path]
        else:
            return None

    def update(self, stats):
        fullpath = stats['fullpath']
        self.path_dict[fullpath] = stats

    def insert(self, stats):
        self.update(stats)

    def all(self):
        return self.path_dict.values()

    def save(self):
        with open(self.filename, "w") as f:
            f.write(json.dumps(self.path_dict))

    def remove(self, filepath):
        if filepath in self.path_dict:
            del self.path_dict[filepath]

    def purge(self):
        open(self.filename, 'w').close()
        self.path_dict = dict()
