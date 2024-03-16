import time
from robocorp.tasks import task
from robocorp import browser
from RPA.HTTP import HTTP
from RPA.Tables import Tables
from RPA.PDF import PDF

main_URL = "https://robotsparebinindustries.com/#/robot-order"
csv_URL = "https://robotsparebinindustries.com/orders.csv"

@task
def order_robots_from_RobotSpareBin():
    """
    Orders robots from RobotSpareBin Industries Inc.
    Saves the order HTML receipt as a PDF file.
    Saves the screenshot of the ordered robot.
    Embeds the screenshot of the robot to the PDF receipt.
    Creates ZIP archive of the receipts and the images.
    """
    # Configure may be used to set the basic robocorp.browser settings.
    # It must be called prior to calling APIs which create playwright objects.
    browser.configure(
	browser_engine="firefox",
	headless=False,
    slowmo=100
    )
    open_robot_order_website()
    close_annoying_modal()
    fill_the_form()

def open_robot_order_website():
    browser.goto(main_URL)

def get_orders():
    http = HTTP()
    http.download(url=csv_URL, overwrite=True)
    # Initialize the Tables library
    tables = Tables()
    # Read data from a CSV file into a table
    return tables.read_table_from_csv("orders.csv", header=True)

def close_annoying_modal():
    page = browser.page()
    page.click("//*[@class='btn btn-danger']")

def fill_the_form():
    page = browser.page()
    orders = get_orders()
    for rows in orders:
        curr_body = "#id-body-"+str(rows["Body"])
        page.select_option("#head", str(rows["Head"]))
        page.click(curr_body)
        page.fill("//*[@class='form-control']",str(rows["Legs"]))
        page.fill("#address",str(rows["Address"]))
        order_num = str(rows["Order number"])
        #print(curr_body)
        #print(rows["Head"])
        page.click("#preview")
        #page.click("#order",click_count=2)
        page.click("#order")
        #receiptnum = page.locator("//*[@class='badge badge-success']").inner_text()
        #print(receiptnum)
        store_receipt_as_pdf(order_num)
        page.click("#order-another")
        close_annoying_modal()

def store_receipt_as_pdf(order_number):
    page = browser.page()
    receipt_html = page.locator("receipt").inner_html()
    pdf = PDF()
    pdf.html_to_pdf(receipt_html, "output/receipts/"+order_number+".pdf")
