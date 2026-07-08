# starts everything
from tkinter import messagebox # creates the box window

from file_manager import get_latest_pdf, open_pdf
from validators import extract_site_number
from gui import create_window

def main():
    
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