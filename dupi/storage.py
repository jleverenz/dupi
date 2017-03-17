import json
import os
from collections import defaultdict


class Storage:
    """Data model for filepath information.

    'Storage' stores two dictionaries:
        1. path keys to stats values
        2. hash keys to list values of duplicate files with common hash
    """

    def __init__(self, filename):
        self.filename = filename
        self.path_dict = dict()
        self.hash_dict = defaultdict(list)
        if os.path.exists(filename):
            with open(filename) as f:
                json_text = f.read()
                if json_text != "":
                    data = json.loads(json_text)

                    self.path_dict = data['paths']
                    self.hash_dict = defaultdict(list, data['hashes'])

    def get(self, path):
        if path in self.path_dict:
            return self.path_dict[path]
        else:
            return None

    def update(self, stats):
        fullpath = stats['fullpath']
        self.remove(fullpath)

        self.path_dict[fullpath] = stats

        hash_key = stats['sha256']
        files = self.hash_dict[hash_key]
        if fullpath not in files:
            files.append(fullpath)

    def insert(self, stats):
        self.update(stats)

    def all(self):
        return self.path_dict.values()

    def save(self):
        data = dict()
        data['paths'] = self.path_dict
        data['hashes'] = self.hash_dict

        with open(self.filename, "w") as f:
            f.write(json.dumps(data))

    def remove(self, filepath):
        if filepath in self.path_dict:
            del self.path_dict[filepath]
        for v in self.hash_dict.values():
            if filepath in v:
                v.remove(filepath)

    def purge(self):
        open(self.filename, 'w').close()  # empties file
        self.path_dict = dict()
        self.hash_dict = defaultdict(list)
