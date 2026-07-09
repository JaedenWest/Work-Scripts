#creates the folder, moves the pdf into folder
import os # allows interaction with the os
import shutil # allows you to move files
from config import DOWNLOADS_FOLDER

from config import JHA_Folder, WO_Folder

def move_pdf(pdf_path, document_type, site_number):
    """
    Moves the PDF to the appropriate folder based on the document type and site number.
    """
    if document_type == "JHA":
        destination_folder = JHA_Folder
    elif document_type == "WO":
        destination_folder = WO_Folder
    else:
        return False, "Invalid document type"
    
    # pad the site number with leading zeros to make it 4 digits
    folder_name = site_number.zfill(4)

    # Create a subfolder for the site number if it doesn't exist
    site_folder = destination_folder / folder_name
    
    #dont allow duplicate folders
    if site_folder.exists():
        return False, f"Folder {folder_name} already exists."
    site_folder.mkdir()

    # Move the PDF to the appropriate folder
    try:
        shutil.move(str(pdf_path), str(site_folder / pdf_path.name))
    except Exception as error:
        return False, str(error)

    return True, "File moved successfully"


def get_latest_pdf():
    """Return the newest PDF in the user's Downloads folder."""
    #downloads looks in download folder
    #pdf finds downloads ending in .pdf
    pdfs = list(DOWNLOADS_FOLDER.glob("*.pdf"))

    if not pdfs:
        return None
    
    #returns the most recent modified pdf file
    return max(pdfs, key=lambda pdf: pdf.stat().st_mtime)

def open_pdf(pdf_path):
    #opens PDF using the default windows program
    os.startfile(pdf_path)
