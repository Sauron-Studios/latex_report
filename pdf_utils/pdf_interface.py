from http.client import HTTPException
from pdf_generator import *

PDF_INTERFACES = [
    "getPurchaseSaleInvoicePDF",
    "getReportStockByProductPDF",
    "getReportLowStockPDF",
    "getReportProfitReportPDF",
    "getReportSummaryPDF",
    "getReportTopCustomerPDF",
    "getReportCustomerHistoryPDF",
    "getReportCompanyOverviewPDF"
]

def pdf_caller(func_name:str,data):
    try:
        if func_name not in PDF_INTERFACES:
            raise HTTPException(status_code=500, detail=f"Function is not registered!")
        
        if not callable(func_name):
            raise HTTPException(status_code=500, detail=f"Function '{func_name}' not found or not callable")

        return func_name(data)
        
    except Exception as e:
        print(str(e))


