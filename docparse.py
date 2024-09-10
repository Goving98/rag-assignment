from unstructured.partition.pdf import partition_pdf
from unstructured.partition.docx import partition_docx
from unstructured.partition.html import partition_html
from unstructured.partition.xml import partition_xml
from unstructured.partition.csv import partition_csv
from unstructured.partition.pptx import partition_pptx
from unstructured.documents.elements import Element
import io

def parse_document(content: bytes, filename: str) -> str:
    """
    Parses the content of a document and returns the extracted text.
    This function handles different file types by using specific partition functions.
    """
    file_extension = filename.split('.')[-1].lower()
    file_like_obj = io.BytesIO(content)

    if file_extension == 'pdf':
        elements = partition_pdf(file=file_like_obj)
    elif file_extension == 'docx':
        elements = partition_docx(file=file_like_obj)
    elif file_extension == 'html':
        elements = partition_html(file=file_like_obj)
    elif file_extension == 'xml':
        elements = partition_xml(file=file_like_obj)
    elif file_extension == 'csv':
        elements = partition_csv(file=file_like_obj)
    elif file_extension == 'pptx':
        elements = partition_pptx(file=file_like_obj)
    else:
        raise ValueError(f"Unsupported file type: {file_extension}")
    parsed_text = "\n".join([element.text for element in elements if isinstance(element, Element)])    
    return parsed_text
