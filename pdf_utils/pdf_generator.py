from collections import defaultdict
from django.http import FileResponse
import os

from json import *
from pdf_utils.PCreateTable import *
from pdf_utils.PBox import *
from pdf_utils.PPie import CreatePieChart, CreatePieChart2
from pdf_utils.pdf_compiler import compile_latex_to_bytes


def getPurchaseSaleInvoicePDF(data: dict):
    id = data["id"]
    invoice_type = data["invoice_type"]
    customer = data["customer"]["name"]
    warehouse = data["warehouse"]["name"]
    date = data["date"]
    notes = data["notes"]
    created_at = data["created_at"]
    updated_at = data["updated_at"]

    headers = [
        "ID",
        "TYPE",
        "CUSTOMER",
        "WAREHOUSE",
        "DATE",
        "NOTES",
        "CREATED",
        "UPDATED",
    ]

    rows = [
        [id, invoice_type, customer, warehouse, date, notes, created_at, updated_at]
    ]  #

    latexStr = ""
    latexStr = latexStr + CreateVerticalTable(tableHeaders=headers, tableRows=rows)

    return compile_latex_to_bytes(latexStr)


def getReportStockByProductPDF(data: dict):
    required_keys = ["summary", "detail"]
    for key in required_keys:
        assert key in data, f"Missing required field: {key}"

    totalStock = data["summary"]["total_stock"]
    detail = data["detail"]

    byProduct = detail["by_product"]
    products = byProduct.keys()

    latexStr = ""
    latexStr += CreateHorizontalTable(
        tableFormats=["X"],
        tableHeaders=[],
        tableRows=[["\\Large\\textbf{Stock by Products}"]],
    )

    for p in products:
        tableRows = []
        for item in byProduct[p]:
            tableRows.append(["", str(item["warehouse"]), str(item["stock"])])

        latexStr += CreateHorizontalTable(
            tableFormats=["X", "X", "X"],
            tableHeaders=[str(p), "Warehouse", "Stock"],
            tableRows=tableRows,
        )

    latexStr += CreateHorizontalTable(
        tableFormats=["X", "X", "X"],
        tableHeaders=[],
        tableRows=[["", "", str(totalStock)]],
    )

    latexStr += "\\clearpage"
    latexStr += CreateHorizontalTable(
        tableFormats=["X"],
        tableHeaders=[],
        tableRows=[["\\Large\\textbf{Stock by Warehouses}"]],
    )

    byWarehouse = detail["by_warehouse"]
    warehouses = byWarehouse.keys()
    for w in warehouses:
        tableRows = []
        for item in byWarehouse[w]:
            tableRows.append(["", str(item["product"]), str(item["stock"])])
        latexStr += CreateHorizontalTable(
            tableFormats=["X", "X", "X"],
            tableHeaders=[str(w), "Product", "Stock"],
            tableRows=tableRows,
        )

    latexStr += CreateHorizontalTable(
        tableFormats=["X", "X", "X"],
        tableHeaders=[],
        tableRows=[["", "", str(totalStock)]],
    )

    return compile_latex_to_bytes(latexStr)


def getReportLowStockPDF(data: list):
    latexStr = ""
    latexStr += CreateHorizontalTable(
        tableFormats=["X"], tableHeaders=[], tableRows=[["\\Large\\textbf{Low Stock}"]]
    )

    tableRows = []
    for item in data:
        tableRows.append(
            [item["product__name"], item["warehouse__name"], str(item["quantity"])]
        )
    if len(tableRows) != 0:
        latexStr += CreateHorizontalTable(
            tableFormats=["X", "X", "X"],
            tableHeaders=["Product", "Warehouse", "Quantity"],
            tableRows=tableRows,
        )
    else:
        latexStr += "No Stock \n"

    return compile_latex_to_bytes(latexStr)


def getReportProfitReportPDF(data: dict):
    summary = data["summary"]

    # Revenue=Profit+Cost
    revenue = summary["total_revenue"]
    cost = abs(summary["total_cost"])
    profit = abs(summary["total_profit"])
    revenue = cost + profit

    latexStr = ""

    latexStr += CreateHorizontalTable(
        tableFormats=["X", "X", "X"],
        tableHeaders=["Profit", "Cost", "Revenue"],
        tableRows=[[str(profit), str(cost), str(profit)]],
    )

    latexStr += CreatePieChart(
        labels=["-" + str(round(cost, 2)), "+" + str(round(profit, 2))],
        values=[round(100 * cost / revenue, 2), round(100 * profit / revenue, 2)],
    )

    byWarehouse = data["detail"]["by_warehouse"]
    warehouses = byWarehouse.keys()
    for w in warehouses:
        tableRows = []
        for item in byWarehouse[w]:
            tableRows.append(
                [
                    "",
                    str(item["product"]),
                    str(item["sold_quantity"]),
                    str(item["revenue"]),
                    str(item["bought_quantity"]),
                    str(item["cost"]),
                    str(item["profit"]),
                ]
            )
        tableHeaders = [
            str(w),
            "Product",
            "Sold Quantity",
            "Revenue",
            "Bought Quantity",
            "Cost",
            "Profit",
        ]
        tableFormats = ["X", "X", "X", "X", "X", "X", "X"]

        latexStr += CreateHorizontalTable(
            tableFormats=tableFormats,
            tableHeaders=tableHeaders,
            tableRows=tableRows,
        )

    latexStr += "\\clearpage"

    byProduct = data["detail"]["by_product"]
    products = byProduct.keys()
    for p in products:
        tableRows = []
        for item in byProduct[p]:
            tableRows.append(
                [
                    "",
                    str(item["warehouse"]),
                    str(item["sold_quantity"]),
                    str(item["revenue"]),
                    str(item["bought_quantity"]),
                    str(item["cost"]),
                    str(item["profit"]),
                ]
            )
        tableHeaders = [
            str(p),
            "Warehouse",
            "Sold Quantity",
            "Revenue",
            "Bought Quantity",
            "Cost",
            "Profit",
        ]
        tableFormats = ["X", "X", "X", "X", "X", "X", "X"]

        latexStr += CreateHorizontalTable(
            tableFormats=tableFormats,
            tableHeaders=tableHeaders,
            tableRows=tableRows,
        )

    return compile_latex_to_bytes(latexStr)


def getReportSummaryPDF(data: dict):

    ###########################################################
    # Purchase
    ###########################################################
    latexStr = ""
    latexStr += CreateHorizontalTable(
        tableFormats=["X"],
        tableHeaders=[],
        tableRows=[["\\Large\\textbf{Purchase}"]],
    )
    purchase = data["purchase"]
    summary = purchase["summary"]
    tableHeaders = ["Product", "Total Quantity", "Total Value", "Average Price"]
    tableRows = []
    for item in summary:
        tableRows.append(
            [
                item["product__name"],
                str(item["total_quantity"]),
                str(item["total_value"]),
                str(item["avg_price"]),
            ]
        )
    latexStr += CreateHorizontalTable(
        tableFormats=["X"] * len(tableHeaders),
        tableHeaders=tableHeaders,
        tableRows=tableRows,
    )

    details = purchase["details"]
    # grouping ids
    grouped = defaultdict(list)

    # Group by invoice__id
    for item in details:
        invoice_id = item["invoice__id"]
        grouped[invoice_id].append(item)

    # Convert to regular dict if needed
    grouped_dict = dict(grouped)

    for invoice_id, items in grouped_dict.items():
        tableHeaders = [
            items[0]["invoice__date"].strftime("%H:%M:%S %d.%m.%Y"),
            "Product",
            "Quantity",
            "Unit Price",
            "Value",
            "Warehouse",
            "Customer",
        ]
        tableRows = []
        for detail in items:
            tableRows.append(
                [
                    "",
                    str(detail["product__name"]),
                    str(detail["quantity"]),
                    str(detail["unit_price"]),
                    str(detail["value"]),
                    str(detail["invoice__warehouse__name"]),
                    str(detail["invoice__customer__name"]),
                ]
            )

        latexStr += CreateHorizontalTable(
            tableFormats=["X"] * len(tableHeaders),
            tableHeaders=tableHeaders,
            tableRows=tableRows,
        )

    ###########################################################
    # Sale
    ###########################################################
    latexStr += "\\clearpage"
    latexStr += CreateHorizontalTable(
        tableFormats=["X"],
        tableHeaders=[],
        tableRows=[["\\Large\\textbf{Sale}"]],
    )
    purchase = data["sale"]
    summary = purchase["summary"]
    tableHeaders = ["Product", "Total Quantity", "Total Value", "Average Price"]
    tableRows = []
    for item in summary:
        tableRows.append(
            [
                item["product__name"],
                str(item["total_quantity"]),
                str(item["total_value"]),
                str(item["avg_price"]),
            ]
        )
    latexStr += CreateHorizontalTable(
        tableFormats=["X"] * len(tableHeaders),
        tableHeaders=tableHeaders,
        tableRows=tableRows,
    )

    details = purchase["details"]
    # grouping ids
    grouped = defaultdict(list)

    # Group by invoice__id
    for item in details:
        invoice_id = item["invoice__id"]
        grouped[invoice_id].append(item)

    # Convert to regular dict if needed
    grouped_dict = dict(grouped)

    for invoice_id, items in grouped_dict.items():
        tableHeaders = [
            items[0]["invoice__date"].strftime("%H:%M:%S %d.%m.%Y"),
            "Product",
            "Quantity",
            "Unit Price",
            "Value",
            "Warehouse",
            "Customer",
        ]
        tableRows = []
        for detail in items:
            tableRows.append(
                [
                    "",
                    str(detail["product__name"]),
                    str(detail["quantity"]),
                    str(detail["unit_price"]),
                    str(detail["value"]),
                    str(detail["invoice__warehouse__name"]),
                    str(detail["invoice__customer__name"]),
                ]
            )

        latexStr += CreateHorizontalTable(
            tableFormats=["X"] * len(tableHeaders),
            tableHeaders=tableHeaders,
            tableRows=tableRows,
        )

    ###########################################################
    # Transfer
    ###########################################################
    latexStr += "\\clearpage"
    latexStr += CreateHorizontalTable(
        tableFormats=["X"],
        tableHeaders=[],
        tableRows=[["\\Large\\textbf{Transfer}"]],
    )
    transfer = data["transfer"]
    summary = transfer["summary"]
    tableHeaders = ["Product", "Total Quantity"]
    tableRows = []
    for item in summary:
        tableRows.append(
            [
                item["product__name"],
                str(item["total_quantity"]),
            ]
        )
    latexStr += CreateHorizontalTable(
        tableFormats=["X"] * len(tableHeaders),
        tableHeaders=tableHeaders,
        tableRows=tableRows,
    )

    details = transfer["all_transfers"]

    tableHeaders = ["Date", "Product", "Quantity", "Warehouse(From)", "Warehouse(To)"]
    for item in details:
        tableRows = []
        tableRows.append(
            [
                item["invoice__date"].strftime("%H:%M:%S %d.%m.%Y"),
                str(item["product__name"]),
                str(item["quantity"]),
                str(item["invoice__source_warehouse__name"]),
                str(item["invoice__destination_warehouse__name"]),
            ]
        )

        latexStr += CreateHorizontalTable(
            tableFormats=["X"] * len(tableHeaders),
            tableHeaders=tableHeaders,
            tableRows=tableRows,
        )

    return compile_latex_to_bytes(latexStr)


def getReportTopCustomerPDF(vec: list):
    latexStr = ""
    latexStr += CreateHorizontalTable(
        tableFormats=["X"],
        tableHeaders=[],
        tableRows=[["\\Large\\textbf{Top Customers}"]],
    )

    tableHeaders = ["Customer", "Total Spent"]
    tableRows = []
    for item in vec:
        name = item["customer__name"]
        spent = item["total_spent"]

        tableRows.append([str(name), str(spent)])

        latexStr += CreateHorizontalTable(
            tableFormats=["X"] * len(tableHeaders),
            tableHeaders=tableHeaders,
            tableRows=tableRows,
        )

    return compile_latex_to_bytes(latexStr)


def getReportCustomerHistoryPDF(data: dict):
    customer = data["customer"]

    latexStr = ""

    tableHeaders = ["Name", "Email", "Phone"]
    latexStr += CreateHorizontalTable(
        tableFormats=["X"] * len(tableHeaders),
        tableHeaders=tableHeaders,
        tableRows=[[customer["name"], customer["email"], customer["phone"]]],
    )

    invoices = data["invoices"]

    for invoice in invoices:

        tableHeaders = ["Invoice", "Warehouse", "Notes", "Date"]
        tableRows = [
            [
                str(invoice["invoice_type"]).upper(),
                invoice["warehouse"]["name"],
                invoice["notes"],
                invoice["date"],
            ]
        ]

        items = invoice["items"]
        for i in items:
            tableRows.append(
                [
                    i["product"]["name"],
                    str(i["quantity"]),
                    str(i["unit_price"]),
                    str(i["quantity"] * i["unit_price"]),
                ]
            )
        latexStr += CreateHorizontalTable(
            tableFormats=["X"] * len(tableHeaders),
            tableHeaders=tableHeaders,
            tableRows=tableRows,
        )

    return compile_latex_to_bytes(latexStr)


def getReportCompanyOverviewPDF(data: dict):
    summary = data["summary"]
    warehouses = data["details"]["warehouses"]

    cards = [
        ("Revenue", f"{summary['total_revenue']}"),
        ("Cost", f"{summary['total_cost']}"),
        ("Profit", f"{summary['profit']}"),
        ("Customers", f"{summary['total_customers']}"),
        ("Products", f"{summary['total_products']}"),
        ("Warehouses", f"{summary['total_warehouses']}"),
    ]

    latexStr = ""
    latexStr += "\centering\\Large\\textbf{Summary}"
    # cardssss
    max_per_row = 3
    x_spacing = 5
    y_spacing = 2
    latexStr += "\\begin{center} \n"
    latexStr += "\\begin{tikzpicture} \n"

    for i, (label, value) in enumerate(cards):
        row = i // max_per_row
        col = i % max_per_row
        x = col * x_spacing
        y = -row * y_spacing
        latexStr += "\\node[draw, minimum width=4cm, minimum height=1.5cm,align=center,"
        latexStr += f"fill=blue!10, rounded corners] at ({x}, {y}) "
        latexStr += "{ "
        latexStr += "\\textbf{"
        latexStr += label
        latexStr += "}\\\\\n "
        latexStr += f"{value}"
        latexStr += "};\n"

    latexStr += "\end{tikzpicture} \n"
    latexStr += "\end{center} \n"

    latexStr += "\centering\\Large\\textbf{Warehouses}"
    tableHeaders = ["Name", "Revenue", "Cost", "Profit", "Stock"]
    tableRows = []
    for w in warehouses:
        tableRows.append(
            [
                w["name"],
                str(w["revenue"]),
                str(w["cost"]),
                str(w["profit"]),
                str(w["stock"]),
            ]
        )

    latexStr += CreateHorizontalTable(
        tableFormats=["X"] * len(tableHeaders),
        tableHeaders=tableHeaders,
        tableRows=tableRows,
    )
    spacing = 2  # cm between rows
    bar_width = 20  # pt

    latexStr += "\centering\\Large\\textbf{Warehouse Profits}"
    latexStr += "\\begin{center}\n"
    latexStr += "\\begin{tikzpicture}\n"

    for i, w in enumerate(warehouses):
        name = w["name"]
        profit = float(w["profit"])
        color = "green!70" if profit >= 0 else "red!70"
        y_shift = -i * spacing
        label_y = 0.5 + y_shift
        axis_y = y_shift - 0.5  # for label space above bar

        # Place warehouse name above
        latexStr += f"\\node at (0,{label_y}) {{\\textbf{{{name}}}}};\n"
        latexStr += f"\\begin{{scope}}[yshift={axis_y}cm]\n"
        latexStr += "\\begin{axis}[\n"
        latexStr += "xbar,\n"
        latexStr += "xmin=-2000, xmax=2000,\n"
        latexStr += "ymin=-0.5, ymax=0.5,\n"
        latexStr += "width=10cm, height=2cm,\n"
        latexStr += "axis lines=none,\n"
        latexStr += "xtick=\\empty,\n"
        latexStr += "ytick=\\empty,\n"
        latexStr += f"bar width={bar_width}pt,\n"
        latexStr += "clip=false,\n"
        latexStr += "nodes near coords,\n"
        anchor = "west" if profit >= 0 else "east"
        latexStr += f"every node near coord/.append style={{font=\\footnotesize, anchor={anchor}}}\n"
        latexStr += "]\n"
        latexStr += (
            f"\\addplot+[draw=none, fill={color}] coordinates {{({profit}, 0)}};\n"
        )
        latexStr += "\\end{axis}\n"
        latexStr += "\\end{scope}\n\n"

    latexStr += "\\end{tikzpicture}\n"
    latexStr += "\\end{center}\n"

    latexStr += "\\clearpage\n"
    latexStr += "\centering\\Large\\textbf{Stocks}"
    total_stock = summary["total_stock"]
    latexStr += CreatePieChart2(
        labels=[w["name"] for w in warehouses],
        values=[round(100 * w["stock"] / total_stock, 2) for w in warehouses],
        colors=["red!50", "blue!50"],
    )
    return compile_latex_to_bytes(latexStr)
