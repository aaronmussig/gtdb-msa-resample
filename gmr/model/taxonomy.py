from pathlib import Path
from typing import Dict

from gmr.model.rank import Rank


class Taxonomy:

    def __init__(self, data: Dict[str, str]):
        self.data = data

    @classmethod
    def from_path(cls, path: Path):
        hits = cls.read(path)
        return cls(hits)

    @staticmethod
    def read(path: Path):
        hits = dict()
        with path.open() as f:
            for line in f.readlines():
                gtdb_id, gtdb_tax = line.strip().split('\t')
                hits[gtdb_id] = gtdb_tax
        return hits

    def get_rank_to_gids(self, rank: Rank, gtdb_gids):
        out = dict()
        rank_idx = rank.to_idx()
        for gid, tax in self.data.items():
            if gid in gtdb_gids:
                tax_split = tax.replace('; ', ';').split(';')
                taxon = tax_split[rank_idx]
                if taxon not in out:
                    out[taxon] = set()
                out[taxon].add(gid)
        return {k: list(v) for k, v in out.items()}
