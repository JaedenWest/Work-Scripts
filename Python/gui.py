#Tkinter window, buttons, labels, status messages
import tkinter as tk # names tkinter tk
from file_manager import move_pdf, get_latest_pdf, open_pdf
from validators import extract_site_number
from config import change_folder

BACKGROUND = "#1e1e1e"
FRAME_COLOR = "#2b2b2b"
TEXT_COLOR = "#ffffff"

#Fonts
TITLE_FONT = ("Segoe UI", 18, "bold")
SECTION_FONT = ("Segoe UI", 12, "bold")
NORMAL_FONT = ("Segoe UI", 10)
BUTTON_FONT = ("Segoe UI", 11)

def create_window(pdf, site_number):
    root = tk.Tk()
    root.configure(bg=BACKGROUND)

    root.title("PDF File/Folder Automation")
    root.geometry("500x450")

    current_pdf = {"value": pdf}

    #job options
    selected_document = tk.StringVar()
    selected_status = tk.StringVar()

    #Default stats
    selected_status.set("Approved")

    #button References
    jha_button = None
    wo_button = None

    approved_button = None
    fixing_button = None

    def select_document(document):

        selected_document.set(document)
        #changing the visual and button color of JHA and WO buttons based on selection
        if document == "JHA":
            jha_button.config(
                relief="sunken",
                bg="#555555"
            )
            wo_button.config(
                relief="raised",
                bg="SystemButtonFace"
            )
        elif document == "WO":
            wo_button.config(
                relief="sunken",
                bg="#555555"
            )
            jha_button.config(
                relief="raised",
                bg="SystemButtonFace"
            )
    #changing the visual and button color of Approved and Needs Fixing buttons based on selection
    def select_status(status):
        if status == "Approved":
            approved_button.config(
                relief="sunken",
                bg="#555555"
            )
            fixing_button.config(
                relief="raised",
                bg="SystemButtonFace"
            )
        elif status == "Needs Fixing":
            fixing_button.config(
                relief="sunken",
                bg="#555555"
            )
            approved_button.config(
                relief="raised",
                bg="SystemButtonFace"
            )
    
    pdf_frame = tk.Frame(
        root,
        bg=FRAME_COLOR,
        padx=20,
        pady=0
    )
    pdf_frame.pack(
        pady=5,
        padx=20,
        fill="x"
    )

    tk.Label(
        pdf_frame,
        text="PDF:",
        bg=FRAME_COLOR,
        fg=TEXT_COLOR,
        font=SECTION_FONT,
    ).pack(
        pady=(0,0)
    )

    pdf_name_label = tk.Label(
        pdf_frame,
        text=pdf.name,
        bg=FRAME_COLOR,
        fg=TEXT_COLOR,
        font=NORMAL_FONT,
        wraplength=400
    )
    
    pdf_name_label.pack(
        pady=(0,10)
    )

    if(site_number):
        site_text = (
            f"Detected Site Number:\n{site_number}"
        )
    else:
        site_text = (
            f"Site Number Not Detected"
        )

    tk.Label(
        pdf_frame,
        text="Detected Site Number:",
        bg=FRAME_COLOR,
        fg=TEXT_COLOR,  
        font=SECTION_FONT
    ).pack(
        pady=(5,0)
    )
    site_number_label = tk.Label(
        pdf_frame,
        text=site_number if site_number else "Site Not Detected",
        bg=FRAME_COLOR,
        fg=TEXT_COLOR,  
        font=SECTION_FONT
    )
    
    site_number_label.pack(
        pady=(0,5)
    )



    document_frame = tk.Frame(
        root,
        bg=FRAME_COLOR,
        pady=10,
        padx=20
    )
    document_frame.pack(
        pady=5,
        padx=20,
        fill="x"
    )

    tk.Label(
        document_frame,
        text="Document Type:",
        bg=FRAME_COLOR,
        fg=TEXT_COLOR,
        font=SECTION_FONT
    ).pack(
        pady=(0,5)
    )
    document_buttons = tk.Frame(
        document_frame,
        bg=FRAME_COLOR
        )
    document_buttons.pack()

    jha_button = tk.Button(
        document_buttons,
        text="JHA",
        width=10,
        command=lambda: select_document("JHA")
    )
    jha_button.pack(
        side="left",
        padx=5
    )

    wo_button = tk.Button(
        document_buttons,
        text="WO",
        width=10,
        command=lambda: select_document("WO")
    )
    wo_button.pack(
        side="left",
        padx=5
    )

    #Status Section

    status_frame = tk.Frame(
        root,
        bg=FRAME_COLOR,
        pady=10,
        padx=20
    )
    status_frame.pack(
        pady=5,
        padx=20,
        fill="x"
    )

    tk.Label(
        status_frame,
        text="Status:",
        bg=FRAME_COLOR,
        fg=TEXT_COLOR,
        font=SECTION_FONT
    ).pack(
        pady=(0,5)
    )

    status_buttons = tk.Frame(
        status_frame,
        bg=FRAME_COLOR
    )
    status_buttons.pack()

    approved_button = tk.Button(
        status_buttons,
        text="Approved",
        width=12,
        command=lambda: select_status("Approved")
    )
    approved_button.pack(
        side="left",
        padx=5
    )

    fixing_button = tk.Button(
        status_buttons,
        text="Needs Fixing",
        width=12,
        command=lambda: select_status("Needs Fixing")
    )
    fixing_button.pack(
        side="left",
        padx=5
    )

    #automatically selects approved
    select_status("Approved")

    #automatically selects document type if detected
    if "JHA" in pdf.name.upper():
        select_document("JHA")
    elif "WO" in pdf.name.upper():
        select_document("WO")


    submit_container = tk.Frame(
        root,
        bg=BACKGROUND
    )

    submit_container.pack(
        pady=0
    )

    submit_frame = tk.Frame(
        submit_container,
        bg=BACKGROUND
    )

    submit_frame.pack(
        pady=20
    )
    
    status_label = tk.Label(
        submit_container,
        text="",
        bg = BACKGROUND,
        fg="white",
        font=NORMAL_FONT
    )

    def refresh_pdf():
        #calls the new pdf to be = to the return value of the latest pdf
        new_pdf = get_latest_pdf()
        #if there is no new pdf print out and return
        if new_pdf is None:
            pdf_name_label.config(text="No PDF found in Downloads.")
            site_number_label.config(text="Site Not Detected")
            return
        #if there is new pdf set the current value to it
        current_pdf["value"] = new_pdf
        #configure it
        pdf_name_label.config(text=new_pdf.name)
        #pull the site number from the new pdf
        new_site_number = extract_site_number(new_pdf.name)
        #print the site number if there is not site number return statement
        site_number_label.config(text=new_site_number if new_site_number else "Site Not Detected")
        #open the pdf
        open_pdf(new_pdf)
        #if its a JHA select the JHA option
        if "JHA" in new_pdf.name.upper():
            select_document("JHA")
        #if its a WO select the WO option
        elif "WO" in new_pdf.name.upper():
            select_document("WO")
        
        status_label.config(text="")

    #change_folders button
    def change_folders():
        change_folder("JHA_Folder", "JHA - Autozone")
        change_folder("WO_Folder", "WO - Autozone")
        status_label.config(
            text="Folders changed successfully.",
            fg="lime green"
        )
    #Submit Button
    def submit():

        document_type = selected_document.get()
        status_type = selected_status.get()

        if status_type != "Approved":
            print("Needs fixing selected")
            return
        
        current_site_number = extract_site_number(current_pdf["value"].name)

        print(f"Document Type: {document_type}")
        print(f"Status Type: {status_type}")
        success, message = move_pdf(
            current_pdf["value"],
            document_type,
            current_site_number     
        )

        if success:
            status_label.config(
                text=message,
                fg="lime green"
            )
        else:
            status_label.config(
                text=message,
                fg="red"
            )
    tk.Button(
        submit_frame, 
        text="Refresh PDF",
        width=15,
        command=refresh_pdf
    ).pack(
        side="left",
        padx=10
    )
    tk.Button(
        submit_frame,
        text="Submit",
        width=15,
        command=submit
    ).pack(
        side="left"
    )

    tk.Button(
        submit_frame,
        text="Change_Folder",
        width=15,
        command=change_folders       
    ).pack(
        side="left",
        padx=10
    )

    status_label.pack(
        pady=(5,10)
    )


    root.mainloop()

