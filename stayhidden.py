import logging
import time
from tqdm import tqdm
from colorama import Fore, Style, init
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

# Initialize colorama
init(autoreset=True)

# Configure logging
logging.basicConfig(filename="stayhidden_log.txt", level=logging.INFO,
                    format="%(asctime)s - %(message)s")

def scan_hidden_elements(url):
    print(Fore.CYAN + f"\n[+] Starting scan for: {url}\n")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Handle page load errors
        try:
            page.goto(url, timeout=60000)
        except PlaywrightTimeoutError:
            print(Fore.RED + f"[!] Timeout while loading {url}")
            browser.close()
            return
        except Exception as e:
            print(Fore.RED + f"[!] Error loading page: {e}")
            browser.close()
            return

        print(Fore.YELLOW + "[*] Scanning page elements...\n")

        # Progress bar for user feedback
        for _ in tqdm(range(30), desc="Scanning"):
            time.sleep(0.03)

        hidden_selectors = [
            "[hidden]",
            "[style*='display:none']",
            "[style*='display: none']",
            "[style*='visibility:hidden']",
            "[style*='visibility: hidden']",
            "input[type='hidden']"
        ]

        hidden_elements = []
        seen = set()

        for selector in hidden_selectors:
            try:
                elements = page.query_selector_all(selector)
                for el in elements:
                    try:
                        el_id = id(el)
                        if el_id not in seen:
                            seen.add(el_id)
                            hidden_elements.append(el)
                    except Exception as e:
                        logging.warning(f"Error processing element from {selector}: {e}")
            except Exception as e:
                logging.error(f"Selector error ({selector}): {e}")

        print(Fore.GREEN + f"\n[✓] Found {len(hidden_elements)} hidden elements\n")

        if not hidden_elements:
            print(Fore.YELLOW + "[!] No hidden elements found.")
        else:
            for idx, el in enumerate(hidden_elements, start=1):
                try:
                    snippet = el.inner_html()
                except Exception:
                    snippet = "<unreadable>"
                print(Fore.MAGENTA + f"[{idx}] Hidden Element:")
                print(Style.DIM + (snippet[:200].strip() if snippet else "<empty>"))
                print("-" * 40)
                logging.info(f"{url} -> Hidden Element {idx}: {snippet}")

        browser.close()
        print(Fore.CYAN + "\n[+] Scan completed!")
        print(Fore.YELLOW + "Results saved in stayhidden_log.txt\n")

def main():
    print(Fore.BLUE + "===================================")
    print(Fore.BLUE + "        STAYHIDDEN SCANNER")
    print(Fore.BLUE + "===================================")

    url = input(Fore.CYAN + "Enter a website URL to scan: ").strip()

    if not url:
        print(Fore.RED + "[!] No URL entered. Exiting...")
        return

    if not (url.startswith("http://") or url.startswith("https://")):
        url = "https://" + url

    try:
        scan_hidden_elements(url)
    except Exception as e:
        print(Fore.RED + f"Error: {e}")
        logging.error(f"Error scanning {url}: {e}")

if __name__ == "__main__":
    main()
