## IMPORTS ##
from bs4 import BeautifulSoup as bs
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options

## PATHS & URLS ##
pGECKO = './geckodriver.exe'
pBILLS = './bills.json'
uBILLS = 'https://www.asuci.uci.edu/senate/legislation/'

## HELPER FUNCTIONS ##
def get_soup(url, by, elem):
    '''
    returns the beautiful soup for a non-static page
    works by calling selenium webdriver and waiting until a certain element loads
    '''
    soup = None 

    opts = Options()
    opts.add_argument('--headless')
    opts.add_argument('--disable-gpu')
    driver = webdriver.FireFox(executable_path = pGECKO, options = opts)
    driver.get(url)

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((by, elem))
        )
    finally:
        soup = bs(driver.page_source, 'html.parser')
        driver.quit()

    return soup

def get_bill_basic(tr):
    ''' 
    takes in a table row html element (beautiful soup object) and constructs basic bill
    properties:
     - item         (int)
     - id           (str)
     - url          (str)
     - synopsis     (str)
     - vote_yea     (int)
     - vote_abs     (int)
     - vote_nay     (int)
     - status       (str)
    '''
    row = tr.find_all('td')

    vot = row[3].text.split('-')
    bill = {
        'item': int(row[0].text),
        'id': row[1].text.strip(),
        'url': row[2].find('a').get('href').strip(),
        'synopsis': row[2].text.strip(),
        'vote_yea': int(v[0]) if v[0] else None,
        'vote_abs': int(v[1]) if v[1] else None,
        'vote_nay': int(v[2]) if v[2] else None,
        'status': row[4].text.strip()
    }

    return bill

def get_bill_full(bill):
    '''
    takes a basic bill object and get this add'nl info:
     - authors          (lst_str)
     - seconds          (lst_str)
     - date_presented   (str, has to be converted to datetime for Discord.Embed())
     - date_voted       (str, see above)
     - vote_required    (str)
     - content          (str)
    not implemented
     - references       (str)
    '''
    bill = None

    soup = get_soup(url=bill.get('url'), by=By.CLASS_NAME, elem='asucilegislation')
    
    pars = soup.find_all('div')
    for div in pars:
        if div.get('id') and 'frmapi' in div.get('id'):
            divparsS = div.find_all('strong')
            divparsP = div.find_all('p')

            bill['authors'] = divparsS[1].text.replace(',', '').split()
            bill['seconds'] = divparsS[2].text.replace(',', '').split()
            bill['date_presented'] = str_date(divpars[3].text.strip(), return_str = True)

            return bill

## MAIN FUNCTIONS ##
def get_all_bills(url = uBILLS):
    '''
    retrieves every single bill and completely rewrites bills.json
    '''
    bills = []

    soup = get_soup(url = url, by = By.TAG_NAME, elem = 'table')

    pars = soup.find('tbody').find_all('tr')

    for tr in pars:
        bill = get_bill_basic(tr)
        bill = get_bill_full(bill)

        bills.append(bill)