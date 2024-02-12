# Reminder I made this code using chatgpt, I know how dir buster works, but because my python skills lack, I had to use AI
# I appreciate your interest and contribution to the project!
import requests
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore, init
import logging
import sys

init(autoreset=True)
logging.basicConfig(level=logging.INFO)

valid_count = 0
invalid_count = 0

def validate_url(url):
    global valid_count, invalid_count
    try:
        if not url.startswith('http'):
            url = f'https://{url}'
        response = requests.get(url, timeout=5)  # Timeout set to 5 seconds
        status = response.status_code
        if status == 200:
            valid_count += 1
            with open('status_200_urls.txt', 'a') as file:
                file.write(f"{url}\n")
            print_current_status(url, Fore.GREEN)  # Print in green for valid URLs
        else:
            invalid_count += 1
            print_current_status(url, Fore.RED)  # Print in red for invalid URLs
        return status, url
    except Exception as e:
        logging.error(f"Error validating {url}: {str(e)}")
        invalid_count += 1
        print_current_status(url, Fore.RED)  # Print in red for errors
        return None

def print_current_status(url, color):
    sys.stdout.write(f"\rValid: {Fore.GREEN}{valid_count}{Fore.RESET}, Invalid: {Fore.RED}{invalid_count}{Fore.RESET}, Current URL: {color}{url}{Fore.RESET}")
    sys.stdout.flush()

def validate_subfolders(url, subfolders):
    global valid_count, invalid_count
    valid_count = 0
    invalid_count = 0

    with ThreadPoolExecutor(max_workers=3) as executor:  # Adjust max_workers as needed
        futures = [executor.submit(validate_url, f"{url}/{subfolder}") for subfolder in subfolders]

        for future in futures:
            result = future.result()
            if result:
                status_code, subfolder_url = result

    print_summary()

def print_summary():
    print("\n" + "-"*50)
    print("Summary:")
    print(f"{Fore.GREEN}Existing URLs: {valid_count}{Fore.RESET}")
    print(f"{Fore.RED}Not Existing URLs: {invalid_count}{Fore.RESET}")
    print("-"*50)

if __name__ == "__main__":
    main_url = input("Enter the base URL (e.g., example.com): ").strip()
    
    # Check main URL
    validate_url(main_url)

    # Check subfolders
    subfolder_file = 'subfolders.txt'
    with open(subfolder_file, 'r') as file:
        subfolder_list = [subfolder.strip() for subfolder in file.readlines()]

    validate_subfolders(main_url, subfolder_list)
