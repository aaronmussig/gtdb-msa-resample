from enum import Enum


class Rank(str, Enum):
    DOMAIN = 'domain',
    PHYLUM = 'phylum',
    CLASS = 'class',
    ORDER = 'order',
    FAMILY = 'family',
    GENUS = 'genus',
    SPECIES = 'species'

    def to_idx(self):
        if self == Rank.DOMAIN:
            return 0
        if self == Rank.PHYLUM:
            return 1
        if self == Rank.CLASS:
            return 2
        if self == Rank.ORDER:
            return 3
        if self == Rank.FAMILY:
            return 4
        if self == Rank.GENUS:
            return 5
        if self == Rank.SPECIES:
            return 6
        raise ValueError(f'Unknown rank: {self}')

    def to_plural(self):
        if self == Rank.DOMAIN:
            return 'domain'
        if self == Rank.PHYLUM:
            return 'phyla'
        if self == Rank.CLASS:
            return 'classes'
        if self == Rank.ORDER:
            return 'orders'
        if self == Rank.FAMILY:
            return 'families'
        if self == Rank.GENUS:
            return 'genera'
        if self == Rank.SPECIES:
            return 'species'
        raise ValueError(f'Unknown rank: {self}')
