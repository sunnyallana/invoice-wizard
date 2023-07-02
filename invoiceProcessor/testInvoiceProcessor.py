from invoiceProcessor import InvoicingSystem

def test_extractInvoiceNumber():
    invoicingSystem = InvoicingSystem()
    ocrText = "100234"
    invoiceNumber = invoicingSystem.extractInvoiceNumber(ocrText)
    assert invoiceNumber == "100234"

def test_extractInvoiceDate():
    invoicingSystem = InvoicingSystem()
    ocrText = "Invoice Date: 2023/02/30"
    invoiceDate = invoicingSystem.extractInvoiceDate(ocrText)
    assert invoiceDate == "2023/06/30"
    ocrText = "Invoice Date: 12/01/2023"
    invoiceDate = invoicingSystem.extractInvoiceDate(ocrText)
    assert invoiceDate == "12/01/2023"

def test_extractTotalAmount():
    invoicingSystem = InvoicingSystem()
    ocrText = "Total Amount: $23.50"
    totalAmount = invoicingSystem.extractTotalAmount(ocrText)
    assert totalAmount == "23.50"

    ocrText = "Total Amount: € 102"
    totalAmount = invoicingSystem.extractTotalAmount(ocrText)
    assert totalAmount == "102"

    ocrText = "Total Amount: PKR 100.50"
    totalAmount = invoicingSystem.extractTotalAmount(ocrText)
    assert totalAmount == "100.50"