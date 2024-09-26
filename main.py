import os
import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import shutil

# Function to perform OCR on a single PDF and save the result as a .txt file
def ocr_pdf_to_txt(pdf_file, output_txt):
    try:
        # Convert PDF to images
        pages = convert_from_path(pdf_file, 300)  # Convert PDF pages to images, 300 dpi for good quality
        
        # Create or open the output text file
        with open(output_txt, 'w', encoding='utf-8') as f:
            # Iterate over all pages
            for page_num, page in enumerate(pages):
                # Perform OCR on the image using pytesseract
                text = pytesseract.image_to_string(page)
                # Write the OCR result to the text file
                f.write(f"\n\n--- Page {page_num + 1} ---\n\n")
                f.write(text)
                
        print(f"OCR complete. Output saved in {output_txt}")
    except Exception as e:
        print(f"Error processing file {pdf_file}: {e}")

# Function to create a mirror directory structure in the target folder
def create_txt_folder_structure(source_folder, target_folder):
    for root, dirs, files in os.walk(source_folder):
        # Construct corresponding target folder structure
        relative_path = os.path.relpath(root, source_folder)
        target_path = os.path.join(target_folder, relative_path)
        os.makedirs(target_path, exist_ok=True)

# Main function
def main():
    # Ask the user for the folder containing the PDF files
    source_folder = input("Enter the folder path where the PDF files are located: ")

    # Create a "TXT" folder to store the OCR results
    target_folder = os.path.join(source_folder, "TXT")
    os.makedirs(target_folder, exist_ok=True)

    # Create a mirrored folder structure inside the "TXT" folder
    create_txt_folder_structure(source_folder, target_folder)

    # Walk through the source folder to find PDF files
    for root, dirs, files in os.walk(source_folder):
        for file in files:
            if file.endswith(".pdf"):
                # Get the full path to the PDF file
                pdf_file_path = os.path.join(root, file)

                # Create the corresponding path in the TXT folder
                relative_path = os.path.relpath(root, source_folder)
                txt_file_dir = os.path.join(target_folder, relative_path)
                txt_file_path = os.path.join(txt_file_dir, f"{os.path.splitext(file)[0]}.txt")

                # Perform OCR on the PDF and save the result as a .txt file
                print(f"Processing {pdf_file_path}...")
                ocr_pdf_to_txt(pdf_file_path, txt_file_path)

if __name__ == "__main__":
    main()