# Invoice Wizard Application

**Author: Sunny Allana**  
**GitHub: [Sunny Allana](https://github.com/sunnyallana/)**  
**LinkedIn: [Sunny Allana](https://www.linkedin.com/in/sunnyallana/)**
**Instagram: [Sunny Allana](https://www.instagram.com/imsunnyallana/)**
**Youtube Link: [Sunny Allana](https://youtu.be/m1fA5uJhOHU)**

The Invoice Wizard is a desktop application implemented in Python and PyQt5 that allows users to import invoice images, utilize Optical Character Recognition (OCR) to extract relevant information, and export the extracted data into a CSV file.

## Application Structure

The application follows the Model-View-Controller (MVC) architectural pattern. The primary class, `InvoicingSystem`, extends PyQt5's `QMainWindow`. Here's an overview of the application's components:

### Model
The application doesn't explicitly employ a separate model class. Instead, the extracted invoice data is stored in the `invoiceData` dictionary attribute of the `InvoicingSystem` class.

### View
The view component handles the graphical user interface (GUI). PyQt5 widgets like `QLabel` and `QPushButton` are used to create GUI elements. The main window, created with `QMainWindow`, contains labels for the heading, imported image, and extracted OCR text. Import and export buttons allow users to import invoice images and export the extracted data, respectively. The imported image is displayed using a `QLabel` widget, while the extracted OCR text is displayed using another `QLabel` widget.

### Controller
The controller manages interactions between the model and view components. The `InvoicingSystem` class has methods for importing invoices, performing OCR on imported images, extracting relevant information (invoice number, date, and total amount) from OCR text, and exporting the extracted data to a CSV file. The import button's `clicked` signal is connected to the `importInvoice` method, allowing users to select an invoice image file via a file dialog. The selected image undergoes OCR for text extraction. The export button's `clicked` signal is connected to the `exportInvoice` method, where users select a destination for the exported CSV file via a file dialog. If the required data is available, the extracted information is written to the CSV file.

## OCR and Text Extraction
OCR functionality is implemented using the `pytesseract` library, a Python wrapper for Google's Tesseract OCR engine. The `perform_ocr` method accepts the path to an imported image file, opens it using the `PIL` library, and performs OCR using `pytesseract.image_to_string`. The extracted OCR text is returned as a string.

## Information Extraction
Extracted OCR text is processed to retrieve relevant information such as the invoice number, date, and total amount. The `extractInvoiceNumber`, `extractInvoiceDate`, and `extractTotalAmount` methods utilize regular expressions (`re`) to search for patterns in the OCR text and extract the required information. Extracted information is stored in the `invoiceData` dictionary for future use.

## Importing and Exporting
The import button allows users to select an invoice image file via a file dialog. The selected file is passed to the `perform_ocr` method to extract the OCR text. The extracted data is then displayed in the GUI. The export button allows users to select a destination for the exported CSV file via a file dialog. If the required data is available, the extracted information is written to the CSV file. Users are prompted to choose whether to append to an existing CSV file or overwrite it.

## Running the Application
The `main` function creates an instance of the `InvoicingSystem` class and starts the application's event loop using `app.exec_()`. The `QApplication` class from PyQt5 is utilized.