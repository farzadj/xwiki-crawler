from langchain.schema import Document
from langchain.text_splitter import CharacterTextSplitter, TokenTextSplitter, RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings

docs = []
for url, page_data in collected_pages:
    # Combine all relevant text fields
    page_text = f"Source link: {url}\n\n" 

    # ✅ Extract Title
    if "title" in page_data and page_data["title"].strip():
        page_text += f"{page_data['title']}\n\n"

    # ✅ Extract Sections
    for section in page_data.get("sections", []):
        if "header" in section and section["header"].strip():
            page_text += f"{section['header']}\n"
        if "body" in section and section["body"].strip():
            page_text += f"{section['body']}\n"

        # ✅ Extract Lists
        for lst in section.get("lists", []):
            list_text = "\n".join(f"- {item}" for item in lst.get("items", []))
            page_text += f"\n{list_text}\n"

        # ✅ Extract Tables (Handling List and Dict Formats)
        for table in section.get("tables", []):
            if table and "rows" in table and table["rows"]:
                table_text = ""
                
                # Check if headers exist
                if "headers" in table and table["headers"]:
                    table_text += " | ".join(table["headers"]) + "\n" + "-" * 50 + "\n"

                # Process each row (handle both list & dict cases)
                for row in table["rows"]:
                    if isinstance(row, dict):  # Dictionary case
                        table_text += " | ".join(map(str, row.values())) + "\n"
                    elif isinstance(row, list):  # List case
                        table_text += " | ".join(map(str, row)) + "\n"

                page_text += f"\n{table_text}\n"

        # ✅ Extract Images (Exclude Specific Ones)
        if "images" in section and section["images"]:
            image_links = "\n".join(
                [f"[Image: {img['alt']}]({img['src']})" for img in section["images"]
                 if "farzad" not in img['alt'].lower() and "wiki" not in img['alt'].lower()]
            )
            if image_links:
                page_text += f"\nRelated Images:\n{image_links}\n"

    # ✅ Skip if extracted text is too short
    if len(page_text.strip()) < 10:
        continue

    # ✅ Create LangChain Document
    docs.append(Document(page_content=page_text.strip()))#, metadata={"source": url}))

# ✅ Check if valid documents exist
if not docs:
    raise ValueError("No valid documents extracted. Ensure pages have text!")


# ------------------------------------------------------------------------------
# 2. Split Documents into Chunks
# ------------------------------------------------------------------------------
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_documents(docs)  # Split long documents into smaller parts

# ✅ Check if valid chunks exist before proceeding
if not chunks:
    raise ValueError("No valid chunks were created. Check text extraction!")

# ------------------------------------------------------------------------------
# 3. Create Vector Store (FAISS)
# ------------------------------------------------------------------------------
embeddings = HuggingFaceEmbeddings(model_name="intfloat/e5-large-v2")
#embeddings = HuggingFaceEmbeddings(model_name="hkunlp/instructor-xl")
vectors = FAISS.from_documents(chunks, embeddings)
#vectors.save_local("faiss_index")
