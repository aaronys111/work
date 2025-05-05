from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import requests

def pn(link):
    HEADERS = ({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US, en;q=0.5'
    })
    pn = 'N/A'
    new_webpage = requests.get("https://www.pcpartpicker.com" + link, headers=HEADERS)
    new_soup = BeautifulSoup(new_webpage.content, "lxml")
    
    table = new_soup.find("table", attrs={'class':'partlist partlist--mini'})
    #print(tables.prettify())
    table2 = table.find("tbody")
    #print(table2.prettify())
    for row in table2.find_all("tr"):
        component_cell = row.find("td", class_="td__component")
        if component_cell:
            h4_tag = component_cell.find("h4")
            if h4_tag and h4_tag.get_text(strip=True) == "CPU Cooler":
                #print("CPU Cooler found in this row.")
                next_row = row.find_next_sibling("tr")
                if next_row:
                    price_cell = next_row.find("td", class_="td__name")
                    if price_cell:
                        price_tag = price_cell.find("p", class_="td__price")
                        if price_tag:
                            pn = price_tag.get_text(strip=True)  # Extract price text
                            print(f"Price of CPU Cooler: {pn}")
                # Example placeholder; replace with actual data extraction
                break
                        
    return pn

def extract_titles(titles):
    titlelist = []
    link = 'NA'
    for title in titles:
        # Find the <a> tag inside the <li> element
        link_tag = title.find("a", class_="logGroup__target")
        
        # Check if <a> tag and 'href' attribute exist
        if link_tag and link_tag.get('href'):
            link = link_tag['href']
            #print(f"Found href: {link}")
            mpn = pn(link)
            titlelist.append(mpn)
        else:
            print("No href found for this title.")
    return titlelist

def get_title(soup):
    titles = soup.find_all("li", attrs={'class':'logGroup logGroup__card_2023'})
    if titles:
        print("Titles found:", len(titles))
    else:
        print("No titles found.")
    return titles

def get_price(soup):
    prices = soup.find_all("div", attrs={'class':'logGroup__content--wrapper2'})
    return prices

def price_extract(prices):
    pricelist = []
    for price in prices:
        price2 = price.find("div", attrs={'class':'log__numbers'})
        sale_price = price2.find("p", attrs={'class':'log__price'})
        if sale_price is None: # if no sale price, then leave as 'N/A' to prevent crash
            dollar = 'N/A'
        else: ## extracts the html attribute with the price as a string    
            dollar =  sale_price.string.strip()
            #add to list of prices and prints if it is not null    
        pricelist.append(dollar)
        print(dollar)
    return pricelist

def newlist(titlelist, pricelist):
    finalist = []
    for t, p in zip(titlelist, pricelist):
        finalstring = t + ',' + p
        finalist.append(finalstring)
    return finalist

if __name__ == '__main__':
    URL = "https://pcpartpicker.com/builds/#h=386661,425596,413823,437268,386662,386663,542709,535597&page=48"
    PATH = ""  # Update this with the correct path to your ChromeDriver

    service = Service(PATH)
    options = webdriver.ChromeOptions()
    options.headless = True
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(URL)
    driver.maximize_window()

    # Scroll to the bottom of the page to load all items
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Wait for new items to load
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # Parse the page content with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, "lxml")
    
    # Close the Selenium driver
    driver.quit()
    #print(soup.prettify())
    # Extract prices and titles
    prices = get_price(soup)
    pricelist = price_extract(prices)
    titles = get_title(soup)
    titlelist = extract_titles(titles)

    finalist = newlist(titlelist, pricelist)
    
    for item in finalist:
        print(item)

    print(f"\n\nTotal items: {len(finalist)}")
