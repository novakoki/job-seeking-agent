from unstructured.partition.html import partition_html
from unstructured.chunking.title import chunk_by_title

def chunk_html(html):
    return chunk_by_title(partition_html(text=html), multipage_sections=False, max_characters=500)

