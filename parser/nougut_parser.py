import subprocess

def parse_with_nougat(pdf_path):
    """Parse a PDF by invoking the nougat CLI and return stdout text."""
    # Run the CLI as a subprocess so parser output can be captured programmatically.
    result = subprocess.run(
        ["nougat", pdf_path],
        capture_output=True,
        text=True
    )
    return result.stdout