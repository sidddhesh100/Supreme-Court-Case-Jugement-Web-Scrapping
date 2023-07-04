import requests
from bs4 import BeautifulSoup
import csv
import re
import time

def get_captcha():
    """get captcha

    This method will make a api on this url https://main.sci.gov.in/php/captcha_num.php will get the captacha

    Returns:
        str: returns a captcha
    """
    captcha_url = "https://main.sci.gov.in/php/captcha_num.php"
    payload={}
    headers = {
    'Cookie': 'BNI_persistence=nqPBLLmSI9ljDVReJQaxg_yXTbzNBS61w9lwfTGBByBFIlZAfhoxtRwiWJLKO2sb1DzL68BBrE7ruIihSdy6Kw==; SERVERID=php_130_88; SESS3e237ce09ea0ff0fb3e315573005c968=rODTdbKE5lUCZOXedzPp_Q10pqWjlI_oTpmKCzUW-y0'
    }
    response_1 = requests.request("GET", captcha_url, headers=headers, data=payload)
    return response_1.text

def get_data(start_date, end_date, captcha, url):
    """get data

    this method will make a api call on url get the html data

    Args:
        start_date (str): start date
        end_date (str): end date
        captcha (str): captach
        url (str): url

    Returns:
        Response: returns the Api response
    """
    payload=f'JBJfrom_date={start_date}&JBJto_date={end_date}&jorrop=J&ansCaptcha={captcha}'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': 'BNI_persistence=nqPBLLmSI9ljDVReJQaxg_yXTbzNBS61w9lwfTGBByBFIlZAfhoxtRwiWJLKO2sb1DzL68BBrE7ruIihSdy6Kw==; SERVERID=php_130_88; SESS3e237ce09ea0ff0fb3e315573005c968=rODTdbKE5lUCZOXedzPp_Q10pqWjlI_oTpmKCzUW-y0'
    }
    return requests.request("POST", url, headers=headers, data=payload)

def scrape_supreme_court_data(start_date, end_date):
    """scrap supreme court data

    This format all the data we ge it from supreme court site and format it to create CSV

    Args:
        start_date (str): strat date
        end_date (str): end date

    Returns:
        list: return the formatted data
    """
    url = "https://main.sci.gov.in/php/v_judgments/getJBJ.php"
    base_url = "https://main.sci.gov.in"
    results = []

    captcha = get_captcha()
    time.sleep(3)
    response = get_data(start_date, end_date, captcha, url)
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup('tr')

    if table is not None:
        for row in range(0, len(table), 9):
            dairy_no = get_dairy_number(table[row].text.replace("\n"," ").strip()).replace(" / ","/")
            case_no = get_case_number(table[row+1].text.replace("\n"," ").strip()).replace(" / ","/").replace(" ","")
            petitioner_name = get_petitioner_name(table[row+2].text.replace("\n"," ").strip())
            respondent_name = get_respodant_name(table[row+3].text.replace("\n"," ").strip())
            petitioner_advocate = get_petitioners_advocate_name(table[row+4].text.replace("\n"," ").strip())
            respondent_advocate = get_respondant_advocate_name(table[row+5].text.replace("\n"," ").strip())
            bench_name = get_bench_name(table[row+6].text.replace("\n"," ").strip())
            judgment_by = get_judgement_by(table[row+7].text.replace("\n"," ").strip())
            judgment_link = base_url + table[row+1].contents[5].contents[0].attrs.get("href","")
            judgment_date = table[row+1].contents[5].text[0:10]

            results.append({
                'dairy_no': dairy_no,
                'case_no': case_no,
                'petitioner_name': petitioner_name,
                'respondent_name': respondent_name,
                'petitioner_advocate': petitioner_advocate,
                'respondent_advocate': respondent_advocate,
                'bench_name': bench_name,
                'judgment_by': judgment_by,
                'judgment_link': judgment_link,
                'judgment_date': judgment_date
            })
    else:
        print("Table not found for the requested start and end date please try again later or try with other dates")

    return results


# This function are used to get required data from the strings
def get_dairy_number(string):
    pattern = r"Diary Number (\d+ \/ \d+)"

    match = re.search(pattern, string)

    if match:
        extracted_value = match.group(1)
        return extracted_value
    
def get_case_number(string):
    string_to_list = string[12:].split(" ")
    string_to_list.pop(-1)
    string_to_list.pop(-1)
    return ' '.join(string_to_list)

def get_petitioner_name(string):
    pattern = r"Petitioner Name (\D+)"
    match = re.search(pattern, string)
    if match:
        petitioner_name = match.group(1)
        return petitioner_name
    
def get_respodant_name(string):
    pattern = r"Respondent Name (\D+)"
    match = re.search(pattern, string)
    if match:
        respodant_name = match.group(1)
        return respodant_name

def get_petitioners_advocate_name(string):
    pattern = r"Petitioner's Advocate (\D+)"
    match = re.search(pattern, string)
    if match:
        petitioners_advocate_name = match.group(1)
        return petitioners_advocate_name

def get_respondant_advocate_name(string):
    pattern = r"Respondent's Advocate (\D+)"
    match = re.search(pattern, string)
    if match:
        respondant_advocate_name = match.group(1)
        return respondant_advocate_name
    
def get_bench_name(string):
    pattern = r"Bench (\D+)"
    match = re.search(pattern, string)
    if match:
        bench_nae = match.group(1)
        return bench_nae
    
def get_judgement_by(string):
    pattern = r"Judgment By (\D+)"
    match = re.search(pattern, string)
    if match:
        judgement_by = match.group(1)
        return judgement_by


def save_to_csv(data, filename):
    """Save to csv 

    This method will save formated data into a csv file

    Args:
        data (list): data
        filename (str): name of the file
    """
    keys = data[0].keys()
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=keys, delimiter=',', quoting=csv.QUOTE_ALL)
        writer.writeheader()
        writer.writerows(data)

start_date = '01-01-2023'
end_date = '01-03-2023'
data = scrape_supreme_court_data(start_date, end_date)
if len(data) != 0 :
    save_to_csv(data, f'supreme_court_from_{start_date}_to_{end_date}.csv')
else:
    print("data not found for the requested start and end date please try again later or try with other dates")