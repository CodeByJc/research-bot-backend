import requests
from config import GROBID_URL

def parse_with_grobid(pdf_path):
    """Parse a PDF with GROBID and return extracted full-text content."""
    # Send the PDF as multipart form data under the expected "input" field.
    files = {
        'input': open(pdf_path, 'rb')
    }

    response = requests.post(GROBID_URL, files=files)

    # GROBID should return 200 on successful extraction.
    if response.status_code != 200:
        raise Exception("GROBID parsing failed")

    return response.text