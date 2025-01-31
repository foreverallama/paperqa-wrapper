from colorama import init, Fore, Style
import re
import psutil
import os
import pickle
import logging

def load_pickle(file_path):

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The specified docs file does not exist: {file_path}")
    
    try:
        with open(file_path, "rb") as f:
            return pickle.load(f)
    except Exception as e:
        logging.getLogger(__name__).error(f"Could not load Indexer Object: {e}")

def get_ollama_model():
    """Returns the running ollama model name"""
    # Returns only the first found ollama model for now
    for process in psutil.process_iter(['pid', 'name', 'cmdline']):
        if 'ollama' in process.info['name'].lower():
            cmdline = process.info['cmdline']
            for cmd in cmdline:
                if 'run' in cmd:
                    return cmdline[cmdline.index(cmd) + 1]
    
def display_answer(response, verbose=0):

    # Split the answer into think and non-think parts
    think_part = ''
    non_think_part = ''
    # Regex to capture text inside <think> tags
    match = re.search(r'<think>(.*?)</think>', response.answer, re.DOTALL)
    if match:
        think_part = match.group(1)
        non_think_part = response.answer.replace(f'<think>{think_part}</think>', '').strip()
    else:
        non_think_part = response.answer.strip()

    # Printing question
    print(f"{Fore.CYAN + Style.BRIGHT}QUESTION:{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{response.question}\n")

    # Printing answer with conditional verbose output
    print(f"{Fore.GREEN + Style.BRIGHT}ANSWER:{Style.RESET_ALL}")
    print(f"{Fore.GREEN}{non_think_part}")

    # Printing references (if any)
    if response.references:
        print(f"\n{Fore.BLUE + Style.BRIGHT}REFERENCES:{Style.RESET_ALL}")
        print(f"{Fore.BLUE}{response.references}")

    # Printing number of tokens used
    print(f"\n{Fore.RED + Style.BRIGHT}TOKEN Count:{Style.RESET_ALL}")
    for model, tokens in response.token_counts.items():
        print(Fore.RED + f" - {model}: " + Fore.GREEN + f"{tokens} tokens")

    if verbose >= 1 and think_part:
        print(f"\n{Fore.YELLOW + Style.BRIGHT}LLM Reasoning:{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}{think_part}")

    if verbose >= 2 and response.contexts:
        print(f"\n{Fore.MAGENTA + Style.BRIGHT}Contexts Used:{Style.RESET_ALL}")

        for context in response.contexts:
            print(
                Fore.YELLOW
                + f" - {context.context} "
                + Fore.MAGENTA
                + f"(from {context.text.name})"
            )