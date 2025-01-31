from paperqa import Docs
from utils import load_pickle

def query_docs(query, settings, file_path):
    indexer = load_pickle(file_path)
    response = indexer.docs.query(query, settings)
    return response