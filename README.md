# Supreme Court Case Jugement Web Scrapping

## Task

Supreme court publishes case judgements on their website.
Your task is to scrape/extract these tabular data/information and store them in .csv file.
site url:- https://main.sci.gov.in/judgments

* Extract the data for the date range :- from date 01-01-2023  -  to date 01-03-2023.
* If there is a pagination in a page then your code should must be able to get the data from all different pages as well.

* All the resulting data should must be saved in .csv/json file as per below given format.


Data to Extract :-
Header's/column/key name should contain below fields:-                   datatype's
dairy_no                                                                                                             string
case_no                                                                                                             string
petitioner_name                                                                                               string
respondent_name                                                                                            string
petitioner_advocate                                                                                         string
respondent_advocate                                                                                      string
bench_name                                                                                                      string
judgment_by                                                                                                      string
judgment_link                                                                                                    string
judgment_date                                                                                                  string


Note:- judgment_link should must contain the url of english judgment pdf displayed under judgment column



## Installation Setup

To set up the project on your local machine, follow these steps:

1. Install Python 3.x or a higher version on your system.
2. Use the following command to install the required dependencies listed in the `requirements.txt` file:
    pip install -r requirements.txt


## How to Run?

To run the project, follow these steps:

1. Make sure you have completed the installation setup steps mentioned above.
2. Open the `app.py` file in a text editor.
3. Locate lines 171 and 172 in the file.
4. Modify the start date and end date values according to the data range you want to extract:
5. Use following command to run the code 
    python app.py
