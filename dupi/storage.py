import json
import os


class Storage:

    def __init__(self, filename):
        self.filename = filename
        self.hash_dict = dict()
        if os.path.exists(filename):
            with open(filename) as f:
                json_text = f.read()
                if json_text != "":
                    self.hash_dict = json.loads(json_text)

    def get(self, path):
        if path in self.hash_dict:
            return self.hash_dict[path]
        else:
            return None

    def update(self, stats):
        fullpath = stats['fullpath']
        self.hash_dict[fullpath] = stats

    def insert(self, stats):
        self.update(stats)

    def all(self):
        return self.hash_dict.values()

    def save(self):
        with open(self.filename, "w") as f:
            f.write(json.dumps(self.hash_dict))

    def remove(self, filepath):
        if filepath in self.hash_dict:
            del self.hash_dict[filepath]

    def purge(self):
        open(self.filename, 'w').close()
        self.hash_dict = dict()
