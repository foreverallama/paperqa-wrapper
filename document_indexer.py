import os
import pickle
from paperqa import Docs
from utils import load_pickle
import logging

class DocumentIndexer:

    def __init__(self, pickle_path):
        self.pickle_path = pickle_path

        if os.path.exists(self.pickle_path):
            obj = load_pickle(self.pickle_path)
            if isinstance(obj, DocumentIndexer):
                self.__dict__.update(obj.__dict__)
                logging.getLogger(__name__).info(f"Loaded existing Docs object from {self.pickle_path}")
            else:
                print("[WARNING] Pickled file does not contain a valid object. Creating a new one.")
                self.docs = Docs()
                self.added_pdfs = set()

        else:
            logging.getLogger(__name__).info(f"Creating new Docs object at {self.pickle_path}")
            self.docs = Docs()
            self.added_pdfs = set()  

    def add_pdfs_from_directory(self, directory, settings):
        """Add all PDFs from a directory to the Doc object, avoiding duplicates."""

        if not os.path.isdir(directory):
            logging.getLogger(__name__).error(f"{directory} is not a valid directory.")
            return

        for filename in os.listdir(directory):
            
            if filename in self.added_pdfs:
                logging.getLogger(__name__).info(f"Skipping {filename} as it is already added.")
                continue

            if filename.endswith(".pdf"):
                pdf_path = os.path.join(directory, filename)
                self.docs.add(pdf_path, settings=settings)
                print(f"Added {filename} to the document index.")
                self.added_pdfs.add(filename)

        self.save()
    
    def save(self):

        if os.path.exists(self.pickle_path):
            logging.getLogger(__name__).warning(f"{self.pickle_path} already exists. Overwriting...")

        try:
            with open(self.pickle_path, "wb") as f:
                pickle.dump(self, f)
                print("Document index saved to", self.pickle_path)
        except Exception as e:
            logging.getLogger(__name__).error(f"Error saving pickle file: {e}")

    # def remove_document(self, file_path):
    #     """Remove a document from the Doc object."""
    #     self.doc.docs = [d for d in self.doc.docs if d.metadata["source"] != file_path]
    #     print(f"Removed {file_path} from index.")