import re


def load_text_file(file) -> str:
    content = file.read()
    if isinstance(content, bytes):
        return content.decode("utf-8")
    return str(content)


def split_into_chunks(text: str):
    raw_chunks = re.split(r"\n\s*\n", text)
    chunks = [chunk.strip() for chunk in raw_chunks if chunk.strip()]
    return chunks


def score_chunk(query: str, chunk: str) -> int:
    query_words = set(re.findall(r"\w+", query.lower()))
    chunk_words = set(re.findall(r"\w+", chunk.lower()))
    return len(query_words.intersection(chunk_words))


def simple_retrieve(query: str, document_text: str, top_k: int = 3):
    chunks = split_into_chunks(document_text)
    scored = [(chunk, score_chunk(query, chunk)) for chunk in chunks]
    scored.sort(key=lambda x: x[1], reverse=True)
    top_chunks = [chunk for chunk, score in scored[:top_k] if score > 0]

    if not top_chunks and chunks:
        top_chunks = chunks[:top_k]

    return top_chunks