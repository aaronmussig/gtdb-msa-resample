import re
from pathlib import Path
from typing import Dict

from gmr.util import exit_error

RE_MSA = re.compile(r'>(.+)\n(.+)')


class Msa:

    def __init__(self, data: Dict[str, str]):

        # Verify that all sequences are the same length
        seq_lengths = set(len(seq) for seq in data.values())
        if len(seq_lengths) != 1:
            exit_error("Not all sequences are the same length.")
        self.data = data

    @classmethod
    def from_path(cls, path: Path):
        hits = cls.read(path)
        return cls(hits)

    @staticmethod
    def read(path: Path):
        with path.open() as f:
            hits = RE_MSA.findall(f.read())
        hits_parsed = {k: v for k, v in hits}
        if len(hits_parsed) != len(hits):
            exit_error("Duplicate sequence IDs found.")
        return hits_parsed

    def gids(self):
        return set(self.data.keys())
