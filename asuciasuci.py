## IMPORTS ##
from bs4 import BeautifulSoup as bs
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options

import utils

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

def bill_info_basic(tr):
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

def bill_info_full(bill):
    '''
    takes a basic bill object and get this add'nl info:
     - authors          (lst_str)
     - seconds          (lst_str)
     - date_presented   (str, has to be converted to datetime for Discord.Embed())
     - date_voted       (str, see above)
     - vote_required    (str)
     - content          (str)
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
            bill['date_presented'] = str2date(divpars[3].text.strip(), return_str = True)

            dv = divpars[-2].text.strip()
            bill['date_voted'] = dv if dv else None
            vr = divpars[-6].text.strip()
            bill['vote_required'] = vr if vr else None

            divtxt = div.text.strip()
            first_p = None

            for p in divparsP:
                if p.text.strip():
                    first_p = p.text.strip()
                    break

            ind_fp = divtxt.index(first_p)
            ind_rf = divtxt.rfind('References:')
            ind_vr = divtxt.rfind('Vote Required:')
            if 'References:' in divtxt:
                bill['content'] = divtxt[ind_fp:ind_rf].strip()
                bill['references'] = divtxt[ind_rf:ind_vr].strip()
            else:
                bill['content'] = divtxt[ind_fp:ind_vr].strip()

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
        bill = bill_info_basic(tr)
        bill = bill_info_full(bill)

        bills.append(bill)
    
    utils.save_json(bills, pBILLS)

    return bills

def get_new_bills(url = uBILLS):

    bills = utils.load_json(pBILLS, [])
    delta = [] # list of bill IDs for bills that were modified or new

    soup = get_soup(url = url, by = By.TAG_NAME, elem = 'table')

    pars = soup.find('tbody').find_all('tr')

    for tr in pars:
        bill = bill_info_basic(tr)

        bill_id = bill.get('id')   

        if not bill_id in [b.get('id') for b in bills]:
            print(f'New bill!: {bill.get("id")}')
            delta.append(bill.get('id'))
            bills.append(bill_info_full(bill))
        else:
            old_bill = get_by_kv(bills, 'id', bill.get('id'))

            if bill.get('status') != old_bill.get('status'):
                print(f'Bill diff: {bill.get("id")}')
                delta.append(bill.get('id'))
                bills[bills.index(old_bill)] = bill_info_full(bill)
            else:
                print(f'Same shit: {bill.get("id")}')

    return bills, delta