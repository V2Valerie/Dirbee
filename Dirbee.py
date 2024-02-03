import requests
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore, init
import logging

init(autoreset=True)
logging.basicConfig(level=logging.INFO)

def validate_url(url):
    try:
        if not url.startswith('http'):
            url = f'https://{url}'
        response = requests.get(url)
        status = response.status_code
        if status == 200:
            logging.info(f"{url}: {Fore.GREEN}Exists{Fore.RESET}")
            with open('status_200_urls.txt', 'a') as file:
                file.write(f"{url}\n")
        else:
            logging.info(f"{url}: {Fore.RED}Doesn't Exist{Fore.RESET}")
        return status, url
    except Exception as e:
        logging.error(f"Error validating {url}: {str(e)}")
        return None

def validate_subfolders(url, subfolders):
    existing_count = 0
    not_existing_count = 0

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(validate_url, f"{url}/{subfolder}") for subfolder in subfolders]

        for future in futures:
            result = future.result()
            if result:
                status_code, subfolder_url = result
                if status_code == 200:
                    existing_count += 1
                else:
                    not_existing_count += 1

    logging.info(f"\n{Fore.GREEN}Existing URLs: {existing_count}{Fore.RESET}")
    logging.info(f"{Fore.RED}Not Existing URLs: {not_existing_count}{Fore.RESET}")

if __name__ == "__main__":
    main_url = input("Enter the base URL (e.g., example.com): ").strip()
    
    # Check main URL
    validate_url(main_url)

    # Check subfolders
    subfolder_file = 'subfolders.txt'
    with open(subfolder_file, 'r') as file:
        subfolder_list = [subfolder.strip() for subfolder in file.readlines()]

    validate_subfolders(main_url, subfolder_list)
