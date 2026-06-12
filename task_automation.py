# ============================================================
#   TASK AUTOMATION WITH PYTHON SCRIPTS
#   CodeAlpha Python Internship — Task 3
#   Author  : [Your Name]
#   Version : 1.0
#
#   Includes THREE automation tools:
#     1. Move .jpg files to a new folder
#     2. Extract email addresses from a .txt file
#     3. Scrape the title of a webpage and save it
# ============================================================

import os
import re
import shutil


# ════════════════════════════════════════════════════════════
#  TOOL 1 — Move JPG Files
# ════════════════════════════════════════════════════════════

def move_jpg_files(source_folder: str, destination_folder: str) -> None:
    """
    Scan source_folder for all .jpg / .jpeg files and
    move them into destination_folder (creates it if needed).
    """
    print("\n" + "=" * 50)
    print("  📁  TOOL 1: Move JPG Files")
    print("=" * 50)

    # Validate source folder
    if not os.path.isdir(source_folder):
        print(f"  ❌  Source folder not found: '{source_folder}'")
        return

    # Create destination folder if it doesn't exist
    os.makedirs(destination_folder, exist_ok=True)

    jpg_files = [
        f for f in os.listdir(source_folder)
        if f.lower().endswith((".jpg", ".jpeg"))
    ]

    if not jpg_files:
        print("  ⚠  No .jpg/.jpeg files found in source folder.")
        return

    moved = 0
    for filename in jpg_files:
        src  = os.path.join(source_folder, filename)
        dest = os.path.join(destination_folder, filename)
        shutil.move(src, dest)
        print(f"  ✅  Moved: {filename}")
        moved += 1

    print(f"\n  ✔  Done! {moved} file(s) moved to '{destination_folder}'")


# ════════════════════════════════════════════════════════════
#  TOOL 2 — Extract Email Addresses
# ════════════════════════════════════════════════════════════

def extract_emails(input_file: str, output_file: str) -> None:
    """
    Read input_file, find all email addresses using regex,
    and save the unique results to output_file.
    """
    print("\n" + "=" * 50)
    print("  📧  TOOL 2: Extract Email Addresses")
    print("=" * 50)

    if not os.path.isfile(input_file):
        print(f"  ❌  Input file not found: '{input_file}'")
        return

    # Regex pattern for standard email addresses
    email_pattern = re.compile(
        r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}"
    )

    with open(input_file, "r", encoding="utf-8") as f:
        content = f.read()

    found_emails = email_pattern.findall(content)
    unique_emails = sorted(set(found_emails))   # remove duplicates

    if not unique_emails:
        print("  ⚠  No email addresses found in the file.")
        return

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"Extracted Emails — Total: {len(unique_emails)}\n")
        f.write("=" * 40 + "\n")
        for email in unique_emails:
            f.write(email + "\n")

    print(f"  ✅  Found {len(unique_emails)} unique email(s).")
    print(f"  ✔  Saved to '{output_file}'")

    # Preview in console
    print("\n  Preview:")
    for email in unique_emails[:5]:
        print(f"    • {email}")
    if len(unique_emails) > 5:
        print(f"    ... and {len(unique_emails) - 5} more.")


# ════════════════════════════════════════════════════════════
#  TOOL 3 — Scrape Webpage Title
# ════════════════════════════════════════════════════════════

def scrape_webpage_title(url: str, output_file: str) -> None:
    """
    Fetch a webpage and extract its <title> tag content,
    then save the result to output_file.
    Requires: pip install requests
    """
    print("\n" + "=" * 50)
    print("  🌐  TOOL 3: Scrape Webpage Title")
    print("=" * 50)

    try:
        import requests
    except ImportError:
        print("  ❌  'requests' library not installed.")
        print("  ➡  Run:  pip install requests")
        return

    try:
        print(f"  Fetching: {url}")
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.ConnectionError:
        print("  ❌  No internet connection or invalid URL.")
        return
    except requests.exceptions.Timeout:
        print("  ❌  Request timed out. Try again later.")
        return
    except requests.exceptions.HTTPError as e:
        print(f"  ❌  HTTP Error: {e}")
        return

    # Extract <title> using regex (no BeautifulSoup needed)
    title_match = re.search(
        r"<title[^>]*>(.*?)</title>",
        response.text,
        re.IGNORECASE | re.DOTALL
    )

    if not title_match:
        print("  ⚠  No <title> tag found on the page.")
        return

    title = title_match.group(1).strip()
    # Clean up HTML entities
    title = title.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")

    print(f"\n  ✅  Title found: {title}")

    from datetime import datetime
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"URL   : {url}\n")
        f.write(f"Title : {title}\n")
        f.write(f"Saved : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    print(f"  ✔  Saved to '{output_file}'")


# ════════════════════════════════════════════════════════════
#  MAIN MENU
# ════════════════════════════════════════════════════════════

def main() -> None:
    """Interactive menu to choose an automation tool."""
    print("\n" + "=" * 50)
    print("   🤖  TASK AUTOMATION TOOLKIT  🤖")
    print("        CodeAlpha — Task 3")
    print("=" * 50)

    menu = {
        "1": "Move JPG Files to a New Folder",
        "2": "Extract Emails from a .txt File",
        "3": "Scrape Webpage Title and Save",
        "4": "Run All Three Tools (Demo Mode)",
        "5": "Exit",
    }

    while True:
        print("\n  ── MENU ──────────────────────────────")
        for k, v in menu.items():
            print(f"  [{k}] {v}")
        print("  ──────────────────────────────────────")

        choice = input("  Choose a tool (1–5): ").strip()

        if choice == "1":
            src  = input("  Source folder path  : ").strip() or "sample_files"
            dest = input("  Destination folder  : ").strip() or "jpg_moved"
            move_jpg_files(src, dest)

        elif choice == "2":
            inp = input("  Input .txt file path : ").strip() or "sample_files/emails.txt"
            out = input("  Output file path     : ").strip() or "extracted_emails.txt"
            extract_emails(inp, out)

        elif choice == "3":
            url = input("  Enter URL (e.g. https://www.python.org): ").strip() or "https://www.python.org"
            out = input("  Output file path : ").strip() or "webpage_title.txt"
            scrape_webpage_title(url, out)

        elif choice == "4":
            print("\n  ── DEMO MODE — Running all 3 tools ──")
            move_jpg_files("sample_files", "jpg_moved")
            extract_emails("sample_files/emails.txt", "extracted_emails.txt")
            scrape_webpage_title("https://www.python.org", "webpage_title.txt")
            print("\n  ✔  All 3 tools completed!")

        elif choice == "5":
            print("\n  Automation complete. Goodbye! 🤖\n")
            break
        else:
            print("  ❌  Invalid choice. Enter 1–5.")


# ── Run ──────────────────────────────────────────────────────
if __name__ == "__main__":
    main()
