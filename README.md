# 🕷️ XWiki Crawler using Selenium

A Python-based web crawler built with **Selenium** to automate the extraction of structured data from **XWiki** pages. It handles login (including OTP), sidebar navigation, page content extraction (titles, text, lists, tables, images), and saves the structured data in a **JSON** format.

---

## 📋 Features

- 🔒 **Automated Login** — Supports standard login and OTP-based authentication.
- 📂 **Sidebar Crawler** — Dynamically expands the sidebar tree and crawls all pages.
- 📑 **Structured Data Extraction** — Extracts titles, sections, lists, tables, and images.
- ⚡ **Stale Element Handling** — Re-attempts extraction on dynamic content.
- 🖼️ **Image Filtering** — Excludes predefined unwanted images.
- 💾 **JSON Export** — Saves all extracted pages in a clean JSON format.

---

## 🛠️ Technologies Used

- **Python 3.x**
- **Selenium WebDriver**
- **Firefox (GeckoDriver)**

---

## ⚙️ Command Flow
1. Login to XWiki: Handles standard and OTP-based authentication.
2. Expand Sidebar: Dynamically expands the navigation tree.
3. Sequential Crawling: Visits each page and extracts content.
4. Content Extraction:
- **Page Titles**
- **Section Headers & Body Text**
- **Lists (ordered/unordered)**
- **Tables with proper mapping**
- **Images (filtered for irrelevant ones)**
5. Data Export: Saves all data in structured JSON.

## Install Dependencies:
pip install -r requirements.txt
