from langchain.document_loaders import AsyncChromiumLoader
from langchain.document_transformers import BeautifulSoupTransformer
from langchain.document_transformers import Html2TextTransformer
from langchain.text_splitter import MarkdownHeaderTextSplitter

loader = AsyncChromiumLoader(["https://www.zuyd.nl/opleidingen/hbo-ict"])
html = loader.load()

#bs_transformer = BeautifulSoupTransformer()
#docs_transformed = bs_transformer.transform_documents(html, tags_to_extract=["span"])

html2text = Html2TextTransformer()
docs_transformed = html2text.transform_documents(html)


headers_to_split_on = [
    ("#", "Header 1"),
    ("##", "Header 2"),
    ("###", "Header 3"),
]

# MD splits
markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
md_header_splits = markdown_splitter.split_text(docs_transformed[0].page_content)

from langchain.text_splitter import RecursiveCharacterTextSplitter

chunk_size = 250
chunk_overlap = 30
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=chunk_size, chunk_overlap=chunk_overlap
)

# Split
splits = text_splitter.split_documents(md_header_splits)
splits


for (i, split) in enumerate(splits):
    file_object = open("docs/hbo-ict-" + str(i) + ".md", "w")
    file_object.write(split.page_content)
    file_object.close()
