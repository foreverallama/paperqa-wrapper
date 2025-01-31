import argparse
from settings import SettingsManager
from document_indexer import DocumentIndexer
from ask_query import query_docs 
from utils import display_answer, get_ollama_model
import logging

# Set up the logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # Set to DEBUG by default

# Create a console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.WARNING)  # Default level

# Define log format
formatter = logging.Formatter("[%(levelname)s] %(message)s")
console_handler.setFormatter(formatter)

# Add handler to logger
logger.addHandler(console_handler)

def setup_logger(verbose: int):
    """
    Adjusts the logger level based on verbosity.
    
    verbose=0 → Only ERROR  
    verbose=1 → WARNING & ERROR  
    verbose=2 → INFO, WARNING, ERROR  
    verbose=3 → DEBUG, INFO, WARNING, ERROR  
    """
    levels = {0: logging.ERROR, 1: logging.WARNING, 2: logging.INFO, 3: logging.DEBUG}
    level = levels.get(verbose, logging.WARNING)  # Default to DEBUG
    console_handler.setLevel(level)
    logger.setLevel(level)

def main():
    parser = argparse.ArgumentParser(description="PaperQA CLI")

    # Global arguments
    parser.add_argument('--llm', choices=['gpt', 'ollama'], help="LLM type (default: ollama)", default='ollama')
    parser.add_argument('--ollama_model', type=str, help="Specify the Ollama model (required if llm_type is 'ollama' or will use one by default)", required=False)
    parser.add_argument('--verbose', type=int, choices=[0, 1, 2, 3], help="Verbose level", default=0)
    
    subparsers = parser.add_subparsers(dest='command')
    
    # Command for adding documents
    add_doc_parser = subparsers.add_parser('add', help="Add documents to the index")
    add_doc_parser.add_argument('--paper_dir', type=str, help="Path to the folder containing papers", default='D:\Code\PhD\Python\paperqa\papers')
    add_doc_parser.add_argument('--file_path', type=str, help="Path to the folder containing the Docs Object", default='D:\Code\PhD\Python\paperqa\paper_index\docs.pkl')
    
    # Command for querying
    query_parser = subparsers.add_parser('query', help="Query your index")
    query_parser.add_argument('query', type=str, help="The query to ask")
    query_parser.add_argument('--file_path', type=str, help="Path to the pickle file (optional)", default='D:\Code\PhD\Python\paperqa\paper_index\docs.pkl')
    
    # Parse the arguments
    args = parser.parse_args()
    setup_logger(args.verbose)

    # Default Ollama model if not provided by the user
    if args.llm == "gpt":
        print(f"Using Model: {args.llm}")
    else:
        if not args.ollama_model:
            ollama_model = get_ollama_model()
            ollama_model = "ollama/" + ollama_model
        else:
            ollama_model = args.ollama_model
    
        print(f"Using model: {ollama_model}")

    manager = SettingsManager(args.llm, ollama_model)
    settings = manager.get_settings()

    if args.command == 'add':
        print("Adding documents...\n")        
        indexer = DocumentIndexer(args.file_path)
        indexer.add_pdfs_from_directory(args.paper_dir, settings)
        
    elif args.command == 'query':
        print("Processing Query...")
        response = query_docs(args.query, settings, args.file_path)
        display_answer(response, verbose=args.verbose)

if __name__ == "__main__":
    main()
