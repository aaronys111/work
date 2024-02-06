from bs4 import BeautifulSoup
import requests

# Function to combine MPN and price into a single string, separated by comma
# The separation by comma is so that this can be extracted into a .CSV file in the future
def newlist(titlelist, pricelist):
        finalist = []
        # the zip is to make sure that there is so that each MPN and price is one-to-one
        for t, p in zip(titlelist, pricelist):
                finalstring = t + ',' + p
                finalist.append(finalstring)
                print(finalstring)
        return finalist

# Function to find MPN in each product page from list
def pn(link):
        # make new soup for each product page
        # NOTE: User agent needs to change once in a while since Amazon will eventually know which one is scraping the website,
        # blocking it from further use
        HEADERS = ({'User-Agent':
	            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
	            'Accept-Language': 'en-US, en;q=0.5'})
        pn = 'N/A'
        new_webpage =  requests.get("https://www.amazon.com" + link, headers=HEADERS)
        new_soup = BeautifulSoup(new_webpage.content, "lxml")
        table = new_soup.find("div", attrs={'id':'prodDetails'})
        # Returns 'N/A' if no MPN is found on product page
        if table is None:
                return pn
        # Divides each row in Product Details table into individual objects to see which one has the MPN
        rows = table.find_all('tr')
        for row in rows:
                th = row.find('th').string.strip()
                if (th=='Item model number'):
                        # extracts MPN based on the index immediately next to "Item model number"
                        pn = row.find('td').string.strip()
                        break
        #check if MPN is being printed so it is not null
        print(pn)
        return pn


def extract_titles(titles):
        titlelist = []
        for title in titles:
                #finds the weblink for the product page
                link = title.get('href')
                #finds the MPN in the weblink
                mpn = pn(link)
                #adds MPN to list
                titlelist.append(mpn)
        #print(len(titlelist))
        return titlelist

def get_title(soup):

	#gets all of the product titles and puts them in a list
	titles =  soup.find_all("a", attrs={'class':'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})
	return titles
                                

# Function to extract all product prices into a list
def get_price(soup):
        
	prices = soup.find_all("span", attrs={'class':'a-price'})
	return prices

def price_extract(prices):
        pricelist = []
        for price in prices:
            sale_price = price.find("span", attrs={'class':'a-offscreen'})
            # if no sale price, then leave as 'N/A' to prevent crash
            if sale_price is None:
                    dollar = 'N/A'
            # extracts the html attribute with the price as a string    
            else:
                    dollar =  sale_price.string.strip()
            #add to list of prices and prints if it is not null    
            pricelist.append(dollar)
            print(dollar)
        print(len(pricelist))
        return pricelist

# Function to extract Product Rating

if __name__ == '__main__':

	# Headers for request
	
	# NOTE: User agent needs to change once in a while since Amazon will eventually know which one is scraping the website,
        # blocking it from further use
        
	HEADERS = ({'User-Agent':
	            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
	            'Accept-Language': 'en-US, en;q=0.5'})

	# The webpage URL
	URL = "https://www.amazon.com/s?k=asus&i=computers&rh=n%3A172282%2Cn%3A541966%2Cn%3A193870011%2Cn%3A17923671011%2Cn%3A1048424%2Cp_89%3AASUS&dc&ds=v1%3AiLhhKO5%2FIdl5N%2Fj9ITNk29258h6OQ7luQ0NMCc%2FLtBE&crid=96UW2CDN9MKL&qid=1699662048&rnid=172282&sprefix=asus%2Ccomputers%2C135&ref=sr_nr_n_12"

	# HTTP Request
	webpage = requests.get(URL, headers=HEADERS)
	# Soup Object containing all data
	soup = BeautifulSoup(webpage.content, "lxml")

	# Function calls to display all necessary product information
	#print("Product Title =", get_title(soup))
	prices = get_price(soup)
	pricelist = price_extract(prices)
	titles =  get_title(soup)
	titlelist = extract_titles(titles)
	
	finalist = newlist(titlelist,pricelist)
	
	print()
	print()

