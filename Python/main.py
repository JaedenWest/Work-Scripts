# starts everything
from tkinter import messagebox # creates the box window

from config import JHA_Folder, WO_Folder
from file_manager import get_latest_pdf, open_pdf
from validators import extract_site_number
from gui import create_window

def main():

    # Check that required OneDrive/SharePoint folders exist before doing anything else
    missing_folders = [
        folder for folder in [JHA_Folder, WO_Folder]
        if not folder.exists()
    ]

    if missing_folders:
        missing_list = "\n".join(str(f) for f in missing_folders)
        messagebox.showerror(
            "Setup Needed",
            f"Couldn't find the following folder(s):\n{missing_list}\n\n"
            "Please go to the relevant SharePoint site(s) and click "
            "'Add shortcut to OneDrive', then try again."
        )
        return
    
    latest_pdf = get_latest_pdf()

    if latest_pdf is None:

        messagebox.showerror(
            "Error",
            "No PDFs found in Downloads."
        )

        return
    
    site_number = extract_site_number(
        latest_pdf.name
    )

    open_pdf(latest_pdf)

    create_window(
        latest_pdf,
        site_number
    )

if __name__ == "__main__":
    main()