import os
import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import time

class OCRProcessor:
    def __init__(self, source_folder):
        self.source_folder = source_folder
        self.base_dir = os.path.dirname(source_folder)
        self.source_folder_name = os.path.basename(source_folder)
        self.target_folder = os.path.join(self.base_dir, f"{self.source_folder_name}_TXT")
        self.total_pages = 0
        self.create_target_folder()

    def create_target_folder(self):
        if not os.path.exists(self.target_folder):
            os.makedirs(self.target_folder)

    def create_txt_folder_structure(self):
        for root, dirs, files in os.walk(self.source_folder):
            relative_path = os.path.relpath(root, self.source_folder)
            target_path = os.path.join(self.target_folder, relative_path)
            os.makedirs(target_path, exist_ok=True)

    def ocr_pdf_to_txt(self, pdf_file, output_txt):
        start_time = time.time()
        try:
            pages = convert_from_path(pdf_file, 300)  # Convert PDF pages to images, 300 dpi for good quality
            num_pages = len(pages)
            print(f"[INFO] {os.path.basename(pdf_file)}: {num_pages} pages found.")
            processed_pages = 0

            with open(output_txt, 'w', encoding='utf-8') as f:
                for page_num, page in enumerate(pages):
                    text = pytesseract.image_to_string(page)
                    f.write(f"\n\n--- Page {page_num + 1} ---\n\n")
                    f.write(text)
                    processed_pages += 1
                    print(f"\r[INFO] Processing page {processed_pages}/{num_pages} of {os.path.basename(pdf_file)}", end="")

            total_time = time.time() - start_time
            avg_page_time = total_time / num_pages if num_pages > 0 else 0
            print(f"\n[INFO] Finished processing {os.path.basename(pdf_file)}.")
            print(f"[INFO] Time taken: {total_time:.2f} seconds. Average time per page: {avg_page_time:.2f} seconds.")

            self.total_pages += num_pages

        except Exception as e:
            print(f"[ERROR] Error processing file {os.path.basename(pdf_file)}: {e}")

    def process_pdfs(self):
        self.create_txt_folder_structure()

        # Find all PDF files
        pdf_files = []
        for root, dirs, files in os.walk(self.source_folder):
            for file in files:
                if file.endswith(".pdf"):
                    pdf_file_path = os.path.join(root, file)
                    pdf_files.append(pdf_file_path)

        total_files = len(pdf_files)
        print(f"[INFO] Found {total_files} PDF files.")

        if total_files == 0:
            print("[INFO] No PDF files found.")
            return

        # Show list of all found PDF files (only filenames)
        print("\n[INFO] List of found PDF files:")
        for idx, file in enumerate(pdf_files, start=1):
            print(f"{idx}. {os.path.basename(file)}")
        print("\n")

        current_file = 0
        start_total_time = time.time()

        for pdf_file_path in pdf_files:
            current_file += 1
            relative_path = os.path.relpath(os.path.dirname(pdf_file_path), self.source_folder)
            txt_file_dir = os.path.join(self.target_folder, relative_path)
            txt_file_path = os.path.join(txt_file_dir, f"{os.path.splitext(os.path.basename(pdf_file_path))[0]}.txt")

            print(f"\n[INFO] Starting processing file {current_file}/{total_files}: {os.path.basename(pdf_file_path)}")
            self.ocr_pdf_to_txt(pdf_file_path, txt_file_path)
            time.sleep(1)  # Ensure at least 1 second between updates

        total_time_taken = time.time() - start_total_time
        avg_file_time = total_time_taken / total_files if total_files > 0 else 0
        avg_page_time_total = total_time_taken / self.total_pages if self.total_pages > 0 else 0

        print(f"\n[INFO] Completed processing {total_files} files.")
        print(f"[INFO] Total time: {total_time_taken:.2f} seconds.")
        print(f"[INFO] Total pages processed: {self.total_pages}.")
        print(f"[INFO] Average time per file: {avg_file_time:.2f} seconds.")
        print(f"[INFO] Average time per page: {avg_page_time_total:.2f} seconds.")

class OCRApplication:
    def __init__(self):
        self.source_folder = self.get_source_folder()

    def get_source_folder(self):
        source_folder = input("Enter the folder path where the PDF files are located: ")
        if not os.path.exists(source_folder):
            raise FileNotFoundError(f"The folder {source_folder} does not exist.")
        return source_folder

    def run(self):
        ocr_processor = OCRProcessor(self.source_folder)
        ocr_processor.process_pdfs()


if __name__ == "__main__":
    app = OCRApplication()
    app.run()
