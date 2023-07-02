import sys, re, csv
from PIL import Image
import pytesseract
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QFileDialog, QMessageBox
from PyQt5.QtGui import QPixmap, QFont


class BookInvoicingSystem(QMainWindow): # Application's primary class

    def __init__(self): # Defining the class's constructor
        super().__init__() # Calling inherited QMainWindow's constructor

        self.setWindowTitle("Book Invoicing System") # Setting the name of the application
        self.setGeometry(100, 100, 800, 600) # Setting the dimensions [x axis, y axis, width, length] of the application
        # self.setStyleSheet("background-image: url(C:/Users/AST/Desktop/finalProject/libraryManagementSystem/background.jpg); background-repeat: no-repeat; background-position: center;")

        self.headingLabel = QLabel("Book Invoicing System", self)
        self.headingLabel.setGeometry(20, 20, 760, 50)
        self.headingLabel.setStyleSheet("font-size: 24px; font-weight: bold; color: #000000;")

        # self.invoice_label = QLabel(self)
        # self.invoice_label.setGeometry(20, 90, 400, 400)

        
        self.importButton = QPushButton("Import Invoice", self) # Create an Import Button
        self.importButton.setGeometry(300, 520, 200, 40) # Set its dimensions
        self.importButton.setStyleSheet("background-color: #4CAF50; color: #FFFFFF; font-weight: bold; border: none; padding: 10px;") # Set its CSS Properties
        self.importButton.clicked.connect(self.importInvoice) # Connect Button to importInvoice function

        self.exportButton = QPushButton("Export Invoice", self) # Create an Export Button
        self.exportButton.setGeometry(520, 520, 200, 40) # Set its dimensions
        self.exportButton.setStyleSheet("background-color: #008CBA; color: #FFFFFF; font-weight: bold; border: none; padding: 10px;") # Set its CSS Properties
        self.exportButton.clicked.connect(self.exportInvoice) # Connect Button to importInvoice function

        self.show() # Display the application

    def importInvoice(self):
        fileDialog = QFileDialog() # pyqt5's method to work with files
        filePath, _ = fileDialog.getOpenFileName(self, "Import Invoice", "", "Image Files (*.png *.jpg)") # Displaying a file dialog to the user allowing them to choose the image file which they want to import

        if filePath: # Check if the filePath is stored in the variable
            ocrText = self.perform_ocr(filePath) # Perform OCR text extraction using pytesseract on the imported invoice image
            
            invoiceNumber = self.extractInvoiceNumber(ocrText) # Extract invoice number from the OCR text
            invoiceDate = self.extractInvoiceDate(ocrText) # Extract invoice date from the OCR text
            totalAmount = self.extractTotalAmount(ocrText) # Extract total Amount from the OCR text

            # Display the extracted invoice information or further process it as needed
            print(f"IN: {invoiceNumber} \nID: {invoiceDate}  \nTA: {totalAmount}")

            self.importButton.setText("Invoice Imported") # Display a message when invoice is imported
            self.importButton.setEnabled(False) # Disable the import button until the current imported file is exported

            self.invoiceData = { # Store the extracted data in a dictionary
                'invoiceNumber': invoiceNumber,
                'invoiceDate': invoiceDate,
                'totalAmount': totalAmount
            }

    def exportInvoice(self):
        if not hasattr(self, 'invoiceData'):
            return

        fileDialog = QFileDialog()
        filePath, _ = fileDialog.getSaveFileName(self, "Export Invoice", "", "CSV Files (*.csv)")

        if filePath:
            existing_csv = False
            if filePath.endswith('.csv'):
                existing_csv = True

            mode = 'a' if existing_csv else 'w'

            if existing_csv:
                choice_dialog = QMessageBox()
                choice_dialog.setWindowTitle("Export Invoice")
                message = "Choose export option:"
                if existing_csv:
                    message += "\n\nSelected file: " + filePath
                choice_dialog.setText(message)

                append_button = choice_dialog.addButton("Append to Existing", QMessageBox.ActionRole)
                overwrite_button = choice_dialog.addButton("Overwrite Existing", QMessageBox.ActionRole)
                cancel_button = choice_dialog.addButton("Cancel", QMessageBox.RejectRole)
                choice_dialog.exec_()

                if choice_dialog.clickedButton() == append_button:
                    mode = 'a'
                elif choice_dialog.clickedButton() == overwrite_button:
                    mode = 'w'
                elif choice_dialog.clickedButton() == cancel_button:
                    return

            with open(filePath, mode, newline='') as csv_file:
                writer = csv.writer(csv_file)

                if mode == 'w':
                    writer.writerow(['Invoice Number', 'Invoice Date', 'Total Amount'])

                writer.writerow([
                    self.invoiceData['invoiceNumber'],
                    self.invoiceData['invoiceDate'],
                    self.invoiceData['totalAmount']
                ])

            print("Invoice data exported successfully!")
            # Enable the import button again
            self.importButton.setText("Import Invoice")
            self.importButton.setEnabled(True)

    def perform_ocr(self, image_path):
        image = Image.open(image_path) # Open the image using pillow's Image.open method
        ocrText = pytesseract.image_to_string(image) # Perform OCR and store result in the ocrText variable
        return ocrText # Return the result

    def extractInvoiceNumber(self, ocrText):
        # Implement logic to extract the invoice number from the OCR text
        # Assume the invoice number is a string of digits
        invoiceNumber = ""
        for word in ocrText.split():
            if word.isdigit():
                invoiceNumber = word
                break
        return invoiceNumber

    def extractInvoiceDate(self, ocrText):
        # Implement logic to extract the invoice date from the OCR text
        # Assume the date format is "DD/MM/YYYY"
        invoiceDate = ""
        date_regex = r"\d{2}/\d{2}/\d{4}"
        match = re.search(date_regex, ocrText)
        if match:
            invoiceDate = match.group()
        return invoiceDate

    def extractTotalAmount(self, ocrText):
        # Implement logic to extract the total amount from the OCR text
        # Assume the total amount is preceded by a currency symbol ($ or €) and followed by digits and/or decimal points
        totalAmount = ""
        amount_regex = r"(?:\$|€|(?:PKR))\s*([\d.,]+)"
        match = re.search(amount_regex, ocrText)
        if match:
            totalAmount = match.group(1)
        return totalAmount

    def save_invoice_to_csv(self, invoiceData):
        # Implement functionality to save the extracted invoice data to a CSV file
        filePath, _ = QFileDialog.getSaveFileName(self, "Save Invoice Data", "", "CSV Files (*.csv)")
        if filePath:
            with open(filePath, 'a', newline='') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(['Invoice Number', 'Invoice Date', 'Total Amount'])
                writer.writerow([invoiceData['invoiceNumber'], invoiceData['invoiceDate'], invoiceData['totalAmount']])
            print("Invoice data saved successfully!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    book_invoicing_system = BookInvoicingSystem()
    sys.exit(app.exec_())