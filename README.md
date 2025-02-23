# XFEL_LLM

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

## 📦 Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/xwiki-crawler.git
   cd xwiki-crawler
