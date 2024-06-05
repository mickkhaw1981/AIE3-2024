import os
from typing import List
import fitz  # PyMuPDF

"""
To augment the TextFileLoader class to support PDFs in addition to .txt files, we can use the PyMuPDF library (fitz module) to handle PDF files. This will allow us to read the text content from PDF files and include them in the self.documents list along with .txt files.

Here are the changes to the TextFileLoader class:

Modify the __init__ method to accept a list of file paths.
Add a method to handle PDF files.
Adjust the load and load_file methods to handle multiple file types.
Update the load_documents method to iterate over a list of paths.

"""

class TextFileLoader:
    def __init__(self, *paths: str, encoding: str = "utf-8"):
        self.documents = []
        self.paths = paths
        self.encoding = encoding

    def load(self):
        for path in self.paths:
            if os.path.isdir(path):
                self.load_directory(path)
            elif os.path.isfile(path):
                if path.endswith(".txt"):
                    self.load_text_file(path)
                elif path.endswith(".pdf"):
                    self.load_pdf_file(path)
                else:
                    raise ValueError(f"Unsupported file type: {path}")
            else:
                raise ValueError(f"Provided path is neither a valid directory nor a supported file: {path}")

    def load_text_file(self, path: str):
        with open(path, "r", encoding=self.encoding) as f:
            self.documents.append(f.read())

    def load_pdf_file(self, path: str):
        with fitz.open(path) as doc:
            text = ""
            for page in doc:
                text += page.get_text()
            self.documents.append(text)

    def load_directory(self, path: str):
        for root, _, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                if file.endswith(".txt"):
                    self.load_text_file(file_path)
                elif file.endswith(".pdf"):
                    self.load_pdf_file(file_path)

    def load_documents(self):
        self.load()
        return self.documents




class CharacterTextSplitter:
    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
    ):
        assert (
            chunk_size > chunk_overlap
        ), "Chunk size must be greater than chunk overlap"

        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def split(self, text: str) -> List[str]:
        chunks = []
        for i in range(0, len(text), self.chunk_size - self.chunk_overlap):
            chunks.append(text[i : i + self.chunk_size])
        return chunks

    def split_texts(self, texts: List[str]) -> List[str]:
        chunks = []
        for text in texts:
            chunks.extend(self.split(text))
        return chunks


if __name__ == "__main__":
    loader = TextFileLoader("data/PMarcaBlogs.txt", "data/BHorowitz_Good_PM.pdf")
    loader.load()
    splitter = CharacterTextSplitter()
    chunks = splitter.split_texts(loader.documents)
    print(len(chunks))
    print(chunks[0])
    print("--------")
    print(chunks[1])
    print("--------")
    print(chunks[-2])
    print("--------")
    print(chunks[-1])
