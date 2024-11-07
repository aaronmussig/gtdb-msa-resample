import importlib.metadata

try:
    __version__ = importlib.metadata.version('gmr')
except importlib.metadata.PackageNotFoundError:
    __version__ = '?.?.?'
