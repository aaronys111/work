from bs4 import BeautifulSoup
import requests
import random

# Function to combine MPN and price into a single string, separated by comma
# The separation by comma is so that this can be extracted into a .CSV file in the future
def send_request(session, proxy):
   try:
            
       response = session.get(URL, proxies={'http': f"http://{proxy}"})
       #webpage = requests.get(URL, headers=HEADERS)
       #print(response.json())
       
       
   except:
       pass

def newlist(titlelist, pricelist):
        finalist = []
        # the zip is to make sure that there is so that each MPN and price is one-to-one
        for t, p in zip(titlelist, pricelist):
                finalstring = t + ',' + p
                finalist.append(finalstring)
                print(finalstring)
        return finalist

def pn(link):
        # make new soup for each product page
        # NOTE: User agent needs to change once in a while since Amazon will eventually know which one is scraping the website,
        # blocking it from further use
        HEADERS = ({'User-Agent':
	            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Viewer/97.9.6198.99',
	            'Accept-Language': 'en-US, en;q=0.5'})
        new_webpage =  requests.get(link, headers=HEADERS)
        new_soup = BeautifulSoup(new_webpage.content, "lxml")
        for caption in new_soup.find_all('caption'):
                # Table header for MPN varies from each product page, so each case takes that into account
                if caption.get_text() == 'General':
                        table = caption.find_parent('table', attrs={'class':'table-horizontal'})
                if caption.get_text() == 'Model':
                        table = caption.find_parent('table', attrs={'class':'table-horizontal'})
        rows = table.find_all('tr')
        # Newegg is more consistent with their format, but this line below may need to change to the one similar to Amazon
        pn = rows[len(rows)-1].find('td').string.strip()
        print(pn)
        return pn


def extract_titles(titles):
        titlelist = []
        # Searches in each product page to find the MPN
        for title in titles:
                link = title.get('href')
                # Finds the MPN for each product weblink
                mpn = pn(link)
                # Adds MPN to list
                titlelist.append(mpn)
        # Prints just to make sure it is on the list
        print('title list length: ', len(titlelist))
        return titlelist

def get_title(soup):

	# gets all the product title attrributes to extract each product page's weblink
	titles =  soup.find_all("a", attrs={'class':'item-img'})
	return titles
                                


# Function to extract Product Price
def get_price(soup):
        # finds all current price attributes on the search page and puts them into a list
        #prices = soup.select("li", attrs={'class':'price-current'})
        prices = soup.find_all("li", attrs={'class':'price-current'})
        test = soup.find("span")
        return prices

def price_extract(prices):
        pricelist = []
        for price in prices:
                # if price is null, then return 'N/A'
                if (price.find('strong')) is None:
                        #print('no')
                        dollar = 'N/A'
                # otherwise add price string to list
                else:
                        #print('yes')
                        dollar = price.find('strong').string.strip() + price.find('sup').string.strip()
                print(dollar)
                pricelist.append(dollar)
        # Returns full list of prices
        return pricelist

# Function to extract Product Rating

if __name__ == '__main__':
        
        # Headers for URL
        
        HEADERS = ({'User-Agent':
	            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Viewer/97.9.6198.99',
	            'Accept-Language': 'en-US, en;q=0.5'})
        URL = "https://www.newegg.com/p/pl?N=100006654%2050001315%208000"

        webpage = requests.get(URL, headers=HEADERS)
        
              
        # HTTP Request
        soup = BeautifulSoup(webpage.content, "lxml")
        print(soup.prettify())
        prices = get_price(soup)
        pricelist = price_extract(prices)
        titles =  get_title(soup)
        titlelist = extract_titles(titles)
        finalist = newlist(titlelist,pricelist)
        

        print()
        print()
