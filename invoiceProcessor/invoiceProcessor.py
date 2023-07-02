import sys, re, csv, os
from PIL import Image
import pytesseract
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QFileDialog, QMessageBox

class InvoicingSystem(QMainWindow): # Application's primary class

    def __init__(self): # Defining the class's constructor
        super().__init__() # Calling inherited QMainWindow's constructor

        self.setWindowTitle("Invoicing System") # Setting the name of the application
        self.setGeometry(600, 300, 800, 600) # Setting the dimensions [x axis, y axis, width, length] of the application
        # self.setStyleSheet("background-image: url(C:/Users/AST/Desktop/finalProject/libraryManagementSystem/background.jpg); background-repeat: no-repeat; background-position: center;")

        self.headingLabel = QLabel("Invoicing System", self)
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
        if not hasattr(self, 'invoiceData'): # Check if self has the attribute invoiceData
            return

        fileDialog = QFileDialog()
        filePath, _ = fileDialog.getSaveFileName(self, "Export Invoice", "", "CSV Files (*.csv)") # Using pyqt5's file dialog, allow users to navigate to the directory where they want to save the file

        if filePath: # Determine if selected file has a .csv extension or not
            existingCsv = False
            if filePath.endswith('.csv'):
                existingCsv = True

            mode = 'w'

            if existingCsv and os.path.isfile(filePath):
                choiceDialog = QMessageBox()
                choiceDialog.setWindowTitle("Export Invoice") # If file already exists, ask user whether to append or overwrite to the existing file
                message = "Choose export option:"
                message += "\n\nSelected file: " + filePath
                choiceDialog.setText(message) # Display the path of the file selected

                appendButton = choiceDialog.addButton("Append", QMessageBox.ActionRole)
                overwriteButton = choiceDialog.addButton("Overwrite", QMessageBox.ActionRole)
                cancelButton = choiceDialog.addButton("Cancel", QMessageBox.RejectRole)
                choiceDialog.exec_()

                if choiceDialog.clickedButton() == appendButton:
                    mode = 'a'
                elif choiceDialog.clickedButton() == overwriteButton:
                    mode = 'w'
                elif choiceDialog.clickedButton() == cancelButton:
                    return

            with open(filePath, mode, newline='') as csvFile:
                writer = csv.writer(csvFile)

                if mode == 'w':
                    writer.writerow(['Invoice Number', 'Invoice Date', 'Total Amount']) # Write headers

                writer.writerow([
                    self.invoiceData['invoiceNumber'],
                    self.invoiceData['invoiceDate'],
                    self.invoiceData['totalAmount']
                ]) # Write values of the provided keys to the csv file

            print("Invoice data exported successfully!")
            self.importButton.setText("Import Invoice")
            self.importButton.setEnabled(True) # Enable the import button again

    def perform_ocr(self, image_path):
        image = Image.open(image_path) # Open the image using pillow's Image.open method
        ocrText = pytesseract.image_to_string(image) # Perform OCR and store result in the ocrText variable
        return ocrText # Return the result

    def extractInvoiceNumber(self, ocrText):
        invoiceNumber = ""
        for word in ocrText.split(): # If a word in ocrText contains just digits, it is considered as a potential invoiceNumber
            if word.isdigit():
                invoiceNumber = word
                break
        return invoiceNumber

    def extractInvoiceDate(self, ocrText):
        invoiceDate = ""
        dateRegex = r"(\d{2}/\d{2}/\d{4})|(\d{4}/\d{2}/\d{2})" # Assuming invoice could have date in different formats
        if match := re.search(dateRegex, ocrText): # Walrus operator to search for regex pattern and check for condition
            invoiceDate = match.group()
        return invoiceDate

    def extractTotalAmount(self, ocrText):
        totalAmount = ""
        amountRegex = r"(?:\$|€|(?:PKR))\s*([\d.,]+)" # Assumption that total amount would be preceeded by $/PKR/€
        if match := re.search(amountRegex, ocrText): # Check for both regex pattern match and condition using Walrus operator
            totalAmount = match.group(1)
        return totalAmount # Return the amount

if __name__ == "__main__":
    app = QApplication(sys.argv)
    general_invoicing_system = InvoicingSystem() # Create an object of the InvoicingSystem class
    sys.exit(app.exec_())