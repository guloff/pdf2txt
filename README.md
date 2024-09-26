# PDF-to-Text Converter

**pdf2txt** is a Python script that performs Optical Character Recognition (OCR) on all PDF files located in a specified folder and saves the extracted text as `.txt` files. The folder structure from the original location is mirrored in the output directory. This script is powered by Tesseract OCR and is capable of recognizing text in English only.

## Features

- Recursively parses a folder to find all PDF files.
- Creates a new folder named `TXT` with the same structure as the original folder.
- Converts each PDF to text using OCR and saves the result as a `.txt` file with the same name as the PDF.
- Supports multi-page PDF files.
- Text recognition is in English.

## Prerequisites

- Python 3.x
- Tesseract OCR installed and accessible from the system's `PATH`.
- Required Python libraries: `pdf2image`, `pytesseract`, and `Pillow`.

You can install the required libraries using pip:

```bash
pip install pdf2image pytesseract Pillow
```

### Installing Tesseract

On macOS, you can install Tesseract using Homebrew:

```bash
brew install tesseract
```

On Linux:

```bash
sudo apt-get install tesseract-ocr
```

On Windows, download and install Tesseract from the [official repository](https://github.com/tesseract-ocr/tesseract/wiki) and ensure it's added to the system's `PATH`.

## Usage

1. Clone this repository:

```bash
git clone https://github.com/guloff/pdf2txt.git
```

2. Navigate to the project folder:

```bash
cd pdf2txt
```

3. Run the script:

```bash
python3 main.py
```

4. Enter the path to the folder containing the PDF files when prompted.

The script will create a new folder named `TXT` inside the original folder and save the OCR results there in `.txt` format, preserving the original folder structure.

### Example

If your folder structure looks like this:

```
/documents
    /reports
        report1.pdf
        report2.pdf
    /manuals
        manual1.pdf
```

The script will create a `TXT` folder with the following structure:

```
/documents/TXT
    /reports
        report1.txt
        report2.txt
    /manuals
        manual1.txt
```

## License

This project is licensed under the GNU General Public License v3.0. See the [LICENSE](LICENSE) file for details.
