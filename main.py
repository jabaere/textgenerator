# -*- coding: utf-8 -*-

import tkinter as tk
import pyperclip
import fitz  # PyMuPDF
import re
from tkinter import filedialog
import tkinter.font as font
import os


# Construct the full path to 'panda.png' using a relative path
# Specify the full path to 'panda.png'
script_dir = os.path.dirname(os.path.abspath(__file__))
# icon_path = 'C:/Users/frosk/Desktop/generator/panda.png'
image_path = os.path.join(script_dir, "panda.png")
# Create the main window
root = tk.Tk()
root.title("Text Generator")
# Load the icon image using the constructed path
if os.path.exists(image_path):
    icon_image = tk.PhotoImage(file=image_path)

    # Set the window icon
    root.iconphoto(True, icon_image)
else:
    print(f"File not found: {image_path}")


# Create a Font object with your custom font family and size
# BPG Nino Mtavruli
georgian_font = font.Font(family='Georgia', size=12)
# Use a Georgian font, adjust size as needed
root.option_add("*Font", "Georgia 12")
root.option_add("*Font", f"{georgian_font} 12")


# Create a global String variables
text_output = tk.StringVar()

custom_font = font.Font(family="Georgia", size=12)


# radio button -- 'ყადაღით/ყადაღის გარეშე'
radio_var = tk.StringVar()
radio_var.set("ყადაღით")
label = tk.Label(root, text="", font=("Georgia", 12))


# Function to be called when Button 2 is clicked
def copy():
    label.config(text="text copied")


def on_radio_select():
    selected_option_text = radio_var.get().upper()
    selected_option_label.config(text="Selected Option: " + " " + selected_option_text,
                                 background='yellow', border=4, padx=4, pady=4, width=30)


def create_left_side(root):
    left_frame = tk.Frame(root)
    left_frame.pack(side=tk.LEFT, padx=10, pady=10)


def extract_and_generate_text(text_output_widget, generated_text_widget):
    global generated_text
    # Open a file dialog for the user to choose a PDF file
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])

    # Check if a file was selected
    if file_path:
        try:
            # Open the selected PDF file
            pdf_document = fitz.open(file_path)

            # Initialize an empty list to store the extracted numbers
            extracted_numbers = []
            # Initialize an empty list to store the extracted numbers

        # Extract text from the PDF
            for page_num in range(len(pdf_document)):
                page = pdf_document[page_num]
                page_text = page.get_text()

            # Use regular expressions to find and extract numbers
            numbers = re.findall(r'\d+\.\d+|\d+', page_text)
            extracted_numbers.extend(numbers)
            # Initialize an empty string to store the extracted data
            extracted_name = ""
            extracted_case_number = ""
            generated_text = ""
            extracted_payment_number = ""
            extracted_enforcement_names = ''
            # Extract specific data from the PDF
            for page_num in range(len(pdf_document)):
                page = pdf_document[page_num]
                page_text = page.get_text()

                # Example: Extract and display lines containing a specific keyword
                keyword = "რესპონდენტი:"
                keyword2 = "SP"
                keyword3 = "PC"

                keyword5 = "მოვალე"

                lines_with_keyword = [
                    line for line in page_text.split('\n') if keyword in line]
                lines_with_keyword2 = [
                    line for line in page_text.split('\n') if keyword2 in line]
                lines_with_keyword3 = [
                    line for line in page_text.split('\n') if keyword3 in line]

                lines_with_keyword5 = [
                    line for line in page_text.split('\n') if keyword5 in line]

                # Append the lines with the keyword to the extracted data
                extracted_name += '\n'.join(lines_with_keyword) + '\n'
                extracted_case_number += '\n'.join(lines_with_keyword2) + '\n'
                extracted_payment_number += '\n'.join(
                    lines_with_keyword3) + '\n'

                extracted_enforcement_names += '\n'.join(
                    lines_with_keyword5) + '\n'
                # ---------------------------------------------------------
                filtered_numbers = [num for num in numbers if re.match(
                    r'^\d+(\.\d+)?$', num) and len(num) <= 8]

                # for 'საგარანტიო'
                enf_numbers = [num for num in numbers if len(num) == 10]

                print(enf_numbers)
                # Sort the filtered numbers
                # sorted_numbers = sorted(filtered_numbers)
                # Print the sorted numbers
                # for num in filtered_numbers:
                # print(num)
            # Close the PDF document
            pdf_document.close()

            # Display the extracted data in the text_output_widget
            text_output_widget.config(state=tk.NORMAL)
            text_output_widget.delete(1.0, tk.END)  # Clear previous text
            text_output_widget.insert(tk.END, extracted_enforcement_names if radio_var.get(
            ) == 'საგარანტიო' else extracted_name)
            text_output_widget.config(state=tk.DISABLED)

            # Generate additional text based on the extracted data
            if radio_var.get() == 'ყადაღის გარეშე':
                generated_text = f"""
გთხოვთ პრობლემური კლიენტის { extracted_name}, საქმეზე  დაგვიმტკიცოთ გამარტივებული წარმოების ხარჯი:
200 ლარი - სააპლიკაციო საფასური;
თანხები არის დაბრუნებადი.
გთხოვთ, დამტკიცების შემთხვევაში გადარიცხოთ თანხები შემდეგი დანიშნულებით:
მიმღების დასახელება: სსიპ აღსრულების ეროვნული ბიურო
საიდენტიფიკაციო კოდი: 205263873
მიმღების ბანკი: სს "საქართველოს ბანკი"
ბანკის კოდი: BAGAGE22
ანგარიშის ნომერი: GE39BG0000000252525252
1. 200 ლარი
დანიშნულება: სააპლიკაციო საფასური, საქმის ნომერი #{extracted_case_number[0:11]}, სს კრედო ბანკი (205232238) - გადახდის ნომერი - {extracted_payment_number[:13]}.
"""
            elif radio_var.get() == 'ყადაღით':
                generated_text = f""" 
გთხოვთ პრობლემური კლიენტის  {extracted_name}, საქმეზე  დაგვიმტკიცოთ გამარტივებული წარმოების ხარჯი:
200 ლარი - სააპლიკაციო საფასური;
{filtered_numbers[4]} ლარი - ყადაღის საფასური;
{filtered_numbers[5]}  ლარი  - საგარანტიო თანხა;
თანხები არის დაბრუნებადი.

გთხოვთ, დამტკიცების შემთხვევაში გადარიცხოთ თანხები შემდეგი დანიშნულებით:
მიმღების დასახელება: სსიპ აღსრულების ეროვნული ბიურო
საიდენტიფიკაციო კოდი: 205263873
მიმღების ბანკი: სს "საქართველოს ბანკი"
ბანკის კოდი: BAGAGE22
ანგარიშის ნომერი: GE39BG0000000252525252

1. 200 ლარი
დანიშნულება: სააპლიკაციო საფასური, საქმის ნომერი #{extracted_case_number[0:11]}, სს კრედო ბანკი (205232238) - გადახდის ნომერი - {extracted_payment_number[:13]}.
2. {filtered_numbers[4]} ლარი
დანიშნულება:ყადაღის საფასური საქმის ნომერი #{extracted_case_number[0:11]}, სს კრედო ბანკი (205232238) - გადახდის ნომერი - {extracted_payment_number[13:27]}.
3. {filtered_numbers[5]} ლარი
დანიშნულება: საგარანტიო თანხა : საქმის ნომერი #{extracted_case_number[0:11]}, სს კრედო ბანკი (205232238) - გადახდის ნომერი - {extracted_payment_number[27:41]}.


"""
            elif radio_var.get() == 'საგარანტიო':
                generated_text = f"""
მოგესალმებით,გთხოვთ პრობლემური კლიენტის {extracted_enforcement_names}
საქმეზე  დაგვიმტკიცოთ აღსრულების ეროვნული ბიუროში საგარანტიო თანხის გადარიცხვა:
{filtered_numbers[9]} ლარი - საგარანტიო თანხა;
გთხოვთ, დამტკიცების შემთხვევაში გადარიცხოთ თანხები შემდეგი დანიშნულებით:
მიმღების დასახელება: სსიპ აღსრულების ეროვნული ბიურო
საიდენტიფიკაციო კოდი: 205263873
მიმღების ბანკი: სს "საქართველოს ბანკი"
ბანკის კოდი: BAGAGE22
ანგარიშის ნომერი: GE41BG0000000222222222
1. {filtered_numbers[9]} ლარი
დანიშნულება: საგარანტიო თანხა, სს კრედო ბანკი (205232238) - გადახდის იდენტიფიკატორი - {enf_numbers[0]}.
                """
            generated_text_widget.config(state=tk.NORMAL)
            # Clear previous generated text
            generated_text_widget.delete(1.0, tk.END)
            generated_text_widget.insert(tk.END, generated_text)
            generated_text_widget.config(state=tk.DISABLED)
        except Exception as e:
            text_output_widget.config(state=tk.NORMAL)
            text_output_widget.delete(1.0, tk.END)
            text_output_widget.insert(tk.END, f"Error: {str(e)}")
            text_output_widget.config(state=tk.DISABLED)


# Create a text widget to display the extracted data
text_output = tk.Text(root, wrap=tk.WORD, height=5,
                      width=70, state=tk.DISABLED)
text_output.pack()
# Create a button to trigger data extraction and text generation
extract_and_generate_button = tk.Button(root, text="აირჩიეთ ფაილი",
                                        command=lambda: extract_and_generate_text(text_output, generated_text_widget), font='Georgia 12', padx=5, pady=5, border=0)
extract_and_generate_button.pack(fill=tk.BOTH, expand=True)
# Create a text widget to display the generated text
generated_text_widget = tk.Text(
    root, wrap=tk.WORD, height=15, width=70, state=tk.DISABLED)
generated_text_widget.pack()

# copy text


def copy_to_clipboard():
    pyperclip.copy(generated_text)


copy_button = tk.Button(
    root, text="კოპირება", command=copy_to_clipboard, border=0)
copy_button.pack(fill=tk.BOTH, expand=True)
#


def create_right_side(root):
    right_frame = tk.Frame(root)
    right_frame.pack(side=tk.BOTTOM, padx=10, pady=10)

    radio_option1 = tk.Radiobutton(
        right_frame, text="ყადაღით", variable=radio_var, value="ყადაღით", command=on_radio_select)
    radio_option1.pack()

    radio_option2 = tk.Radiobutton(right_frame, text="ყადაღის გარეშე",
                                   variable=radio_var, value="ყადაღის გარეშე", command=on_radio_select)
    radio_option2.pack()

    radio_option3 = tk.Radiobutton(right_frame, text="საგარანტიო",
                                   variable=radio_var, value="საგარანტიო", command=on_radio_select)
    radio_option3.pack()

    global selected_option_label  # Declare it as a global variable
    selected_option_label = tk.Label(right_frame, text="Selected Option: " + " " +
                                     radio_var.get().upper(), background='yellow', border=4, padx=4, pady=4, width=30)
    selected_option_label.pack()


# Create the left and right sides of the GUI
create_left_side(root)
create_right_side(root)


# Start the main loop
root.mainloop()
