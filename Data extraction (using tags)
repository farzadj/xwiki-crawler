from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
import time
import json

def save_collected_pages(collected_pages, filename="collected_pages.json"):
    """Save extracted pages to a JSON file."""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(collected_pages, f, indent=4, ensure_ascii=False)
    print(f"✅ Successfully saved {len(collected_pages)} pages to {filename}")

# ------------------------------------------------------------------------------
# 1. WebDriver Setup
# ------------------------------------------------------------------------------
firefox_options = Options()
firefox_options.add_argument("--headless")  # Run in headless mode
service = Service("path to geckodriver")  # Adjust path
driver = webdriver.Firefox(service=service, options=firefox_options)

# ------------------------------------------------------------------------------
# 2. Helper Functions
# ------------------------------------------------------------------------------

def login_xwiki(username, password):
    """Logs into XWiki, handling OTP if required."""
    driver.get("https://xwiki.desy.de/xwiki/bin/login/XWiki/XWikiLogin")
    time.sleep(2)
    driver.find_element(By.ID, "username").send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.ID, "kc-login").click()
    time.sleep(3)

    # Check for OTP
    if "otp" in driver.page_source.lower():
        print("OTP required!")
        otp_value = input("Enter the OTP sent to your device: ")
        driver.find_element(By.ID, "otp").send_keys(otp_value)
        driver.find_element(By.ID, "kc-login").click()
        time.sleep(3)

def find_sidebar():
    """Locate the sidebar panel using multiple XPaths."""
    sidebar_xpaths = [
        '//div[contains(@class, "panel")]',
        '//div[contains(@id, "main-navigation")]',
        '//nav[contains(@class, "aui-sidebar")]',
        '//div[contains(@class, "wiki-tree")]',
    ]
    for xpath in sidebar_xpaths:
        try:
            sidebar = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            return sidebar
        except TimeoutException:
            pass
    return None

def expand_tree_in_place(sidebar):
    """Expands all sidebar menus dynamically before collecting links."""
    icon_xpath = './/span[contains(@class, "aui-iconfont-page-tree")]'
    while True:
        icons = sidebar.find_elements(By.XPATH, icon_xpath)
        clicked_any = False
        for i in range(len(icons)):
            try:
                icons[i].click()
                time.sleep(1)  # Wait for expansion
                clicked_any = True
                break  # Re-locate elements fresh
            except StaleElementReferenceException:
                sidebar = find_sidebar()
                if not sidebar:
                    return
                break
            except Exception:
                pass
        if not clicked_any:
            break

def gather_sidebar_links(sidebar):
    """Collect all links from the expanded sidebar in sequential order."""
    results = []
    while True:
        try:
            link_elements = sidebar.find_elements(By.XPATH, ".//a")
            current_links = []
            for link_el in link_elements:
                try:
                    href = link_el.get_attribute("href")
                    text = link_el.text.strip()
                    if href and text:
                        current_links.append((text, href))
                except StaleElementReferenceException:
                    sidebar = find_sidebar()
                    break
            else:
                results = current_links
                break
        except StaleElementReferenceException:
            sidebar = find_sidebar()
            if not sidebar:
                break
    return results

def extract_tags():
    """Extract all unique HTML tags from the current page."""
    elements = driver.find_elements(By.XPATH, "//*")  # Select all elements
    return {element.tag_name for element in elements}  # Collect unique tag names

def extract_page_structure():
    """Extract structured content from a single page dynamically, handling stale elements."""
    
    found_tags = extract_tags()
    page_data = {"source_url": driver.current_url, "sections": []}

    # Define a list of unwanted images (URLs or alt texts)
    excluded_images = [
        "https://xwiki.desy.de/xwiki/bin/download/FlamingoThemes/Iceberg/DESY_logo_white_web.png",
        "https://xwiki.desy.de/xwiki/bin/skin/resources/icons/xwiki/noavatar.png",
        "Wiki Logo"
    ]

    try:
        # Extract Title
        if "h1" in found_tags:
            try:
                title_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.TAG_NAME, "h1"))
                )
                page_data["title"] = title_element.text.strip() if title_element else "Untitled"
            except TimeoutException:
                page_data["title"] = "Untitled"
        else:
            page_data["title"] = "Untitled"

        # Extract Sections with Headers
        headers = driver.find_elements(By.XPATH, "//h1 | //h2 | //h3 | //h4")

        if headers:
            for header in headers:
                section = {"header": header.text.strip(), "body": "", "lists": [], "tables": [], "images": []}
                next_elements = header.find_elements(By.XPATH, "./following-sibling::*")

                for elem in next_elements:
                    if elem.tag_name == "p":
                        section["body"] += elem.text.strip() + "\n"
                    elif elem.tag_name in {"ul", "ol"}:
                        items = [li.text.strip() for li in elem.find_elements(By.TAG_NAME, "li") if li.text.strip()]
                        if items:
                            section["lists"].append({"type": elem.tag_name, "items": items})
                    elif elem.tag_name == "table":
                        table_data = extract_table(elem)
                        if table_data:
                            section["tables"].append(table_data)
                    elif elem.tag_name == "img":
                        image_src = elem.get_attribute("src")
                        image_alt = elem.get_attribute("alt")
                        
                        # Exclude unwanted images
                        if (image_src and not any(excluded in image_src for excluded in excluded_images)) and \
                           (image_alt and image_alt not in excluded_images):
                            section["images"].append({"alt": image_alt, "src": image_src})
                    elif elem.tag_name in {"h1", "h2", "h3", "h4"}:
                        break  # Stop when reaching the next header

                if section["body"] or section["lists"] or section["tables"] or section["images"]:
                    page_data["sections"].append(section)

        # If No Headers Found, Extract General Content
        if not page_data["sections"]:
            general_section = {"header": "General Content", "body": "", "lists": [], "tables": [], "images": []}

            # Extract all paragraphs
            if "p" in found_tags:
                paragraphs = driver.find_elements(By.TAG_NAME, "p")
                general_section["body"] = "\n".join([p.text.strip() for p in paragraphs if p.text.strip()])


            # Extract all tables
            if "table" in found_tags:
                tables = driver.find_elements(By.TAG_NAME, "table")
                for table in tables:
                    table_data = extract_table(table)
                    if table_data:
                        general_section["tables"].append(table_data)

            # Extract all images (excluding specific ones)
            if "img" in found_tags:
                images = driver.find_elements(By.TAG_NAME, "img")
                for img in images:
                    image_src = img.get_attribute("src")
                    image_alt = img.get_attribute("alt")

                    if (image_src and not any(excluded in image_src for excluded in excluded_images)) and \
                       (image_alt and image_alt not in excluded_images):
                        general_section["images"].append({"alt": image_alt, "src": image_src})

            # Only append if there is content
            if general_section["body"] or general_section["lists"] or general_section["tables"] or general_section["images"]:
                page_data["sections"].append(general_section)

    except StaleElementReferenceException:
        print("⚠️ Stale element encountered during extraction. Retrying...")
        return extract_page_structure()  

    return page_data

def extract_table(table_element):
    """Extract structured table data, linking it to the nearest header."""
    table_info = {"headers": [], "rows": []}

    # Extract headers if present
    headers = table_element.find_elements(By.TAG_NAME, "th")
    if headers:
        table_info["headers"] = [th.text.strip() for th in headers if th.text.strip()]

    # Extract rows
    rows = table_element.find_elements(By.TAG_NAME, "tr")
    for row in rows:
        cells = row.find_elements(By.TAG_NAME, "td")
        row_data = [cell.text.strip() for cell in cells if cell.text.strip()]

        # Map row to headers if headers exist
        if table_info["headers"] and row_data:
            row_dict = dict(zip(table_info["headers"], row_data))
            table_info["rows"].append(row_dict)
        elif row_data:  # If no headers, store as simple list
            table_info["rows"].append(row_data)

    return table_info if table_info["rows"] else None


def sequential_crawl(start_url, start_from_index, end_index):
    """Crawls the sidebar pages sequentially and extracts structured content dynamically."""
    
    driver.get(start_url)
    time.sleep(2)

    visited = set()
    collected_pages = []
    excluded_links = set()

    sidebar = find_sidebar()
    if not sidebar:
        print("Sidebar not found. Exiting.")
        return collected_pages

    expand_tree_in_place(sidebar)
    sidebar = find_sidebar()

    if sidebar:
        all_links = gather_sidebar_links(sidebar)

        if len(all_links) > start_from_index:
            excluded_links.update(link[1] for link in (all_links[:start_from_index] + all_links[end_index:]))
            queue = all_links[start_from_index:end_index]
        else:
            print("Not enough links to skip, starting from the first available.")
            queue = all_links[:end_index]
    else:
        return collected_pages

    while queue:
        link_text, link_url = queue.pop(0)
        if link_url in visited or link_url in excluded_links:
            continue

        print(f"\nVisiting: {link_text} → {link_url}")
        visited.add(link_url)
        driver.get(link_url)
        time.sleep(2)

        try:
            page_data = extract_page_structure()
            collected_pages.append((link_url, page_data))
            print(f"Extracted structured content from: {link_url}")
        except:
            print("Could not extract structured content from:", link_url)
            pass

        sidebar = find_sidebar()
        if not sidebar:
            continue
        expand_tree_in_place(sidebar)
        sidebar = find_sidebar()

        if sidebar:
            new_links = gather_sidebar_links(sidebar)
            for new_text, new_url in new_links:
                if (new_url not in visited) and (new_url not in excluded_links) and (new_url not in [q[1] for q in queue]):
                    queue.append((new_text, new_url))

    print("\nCrawling complete! Visited pages:", len(visited))
    for v in visited:
        print(f'"{v}",')
    return collected_pages  

# ------------------------------------------------------------------------------
# 3. Main Execution: Start from Sidebar and Extract Structured Data
# ------------------------------------------------------------------------------
try:
    login_xwiki("username", "password")
    start_url = "https://xwiki.desy.de/xwiki/bin/view/XFELOp/"
    start_from_index = 1
    end_index = 1000
    collected_pages = sequential_crawl(start_url, start_from_index, end_index)
    save_collected_pages(collected_pages, "collected_pages.json")
finally:
    driver.quit()
