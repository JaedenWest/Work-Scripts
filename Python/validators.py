#validates the filename
#validates that the folder exists
import re # allows you to find an expression or specific characters in name

def extract_site_number(filename):
    """
    tries to extract a site number from the filename
    Rules:
    Finds the first numeric value that is 4 digits or less
    Ignores 6+ digits and any number after the first 4 or less
    """
    #find all groups of digits
    numbers = re.findall(r"\d+", filename)
    #store only digits that could be site numbers
    for number in numbers:
        if len(number) <= 4:
           return number
    return None

