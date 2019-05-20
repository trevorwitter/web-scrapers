import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
from time import sleep
import datetime


def pause():
    """Greetings, fellow human"""
    return sleep(np.random.choice(range(4,7)))

def get_page_reviews(reviews,times):
    review_df = pd.DataFrame(columns=['Date',
                                      'reviewer detail',
                                      'employee status', 
                                      'Author Location',
                                      'summary',
                                      'rating',
                                      'Pros',
                                      'Cons',
                                      'Advice to Management',
                                      'Recommend',
                                      'Outlook',
                                      'CEO Approval'])
    for x in range(len(reviews)):
        review_dict = {}
        review_dict['summary'] = reviews[x].find_all("span", class_="summary")[0].text
        review_dict['rating'] = float(reviews[x].find_all(class_="value-title")[0].get('title'))
        try:
            review_dict['Date'] = times[x].text
        except:
            review_dict['Date'] = np.nan
        try:
            review_dict['employee status'] = reviews[x].find_all(class_="authorJobTitle middle reviewer")[0].text.split(" - ")[0]
        except:
            review_dict['employee status'] = np.nan
        try:
            review_dict['reviewer detail'] = reviews[x].find_all(class_="authorJobTitle middle reviewer")[0].text.split(" - ")[1]
        except:
            review_dict['reviewer detail'] = np.nan
        try:
            review_dict['Author Location'] = reviews[x].find_all(class_="authorLocation")[0].text
        except:
            review_dict['Author Location'] = np.nan

        recommends = [span.text for span in reviews[x].find_all(class_='row reviewBodyCell recommends')[0].find_all('span')]
        try:
            review_dict['Recommend'] = [s for s in recommends if "ecommen" in s][0]
        except:
            review_dict['Recommend'] = np.nan
        try:
            review_dict['Outlook'] = [s for s in recommends if "Outlook" in s][0]
        except:
            review_dict['Outlook'] = np.nan
        try:
            review_dict['CEO Approval'] = [s for s in recommends if "CEO" in s][0]
        except:
            review_dict['CEO Approval'] = np.nan
        for y in range(3):
            try:
                review_dict[reviews[x].find_all(class_='description')[0].find_all(class_='mt-md')[y].find_all('p')[0].text] = \
                    reviews[x].find_all(class_='description')[0].find_all(class_='mt-md')[y].find_all('p')[-1].text
            except:
                pass
        review_df = review_df.append(review_dict,ignore_index=True)
    return review_df

def get_company_reviews(company,checkpoint=False):
    df = pd.DataFrame()
    for page in range(1,290):
        URL = 'https://www.glassdoor.com/Reviews/{0}-Reviews-E525_P{1}.htm'.format(company,str(page))
        response = requests.get(URL,
                                headers={'User-Agent': 'Mozilla/5.0'})
        print("Page {0} Status: {1}".format(page, response.status_code))
        soup = BeautifulSoup(response.content, 'html.parser')
        reviews = soup.find_all(class_="col-sm-11 pl-sm-lg mx-0")
        times = soup.find_all(class_='date subtle small')
        page_df = get_page_reviews(reviews,times) 
        print('Reviews scraped from page {0}: {1}'.format(page, len(page_df)))
        if len(page_df) == 0:
            wait = np.random.choice(range(40,70))
            "Page not scraped; retry in {0} seconds".format(wait) 
            sleep(wait)
            page_df = get_page_reviews(reviews,times)
        else:
            pass
        df = df.append(page_df,ignore_index=True)
        if checkpoint==True:
            filename='{0}_reviews_ckpt.csv'.format(company)
            df.to_csv(filename,index=False)
        else:
            pass
        print("Page {} complete".format(page))
        pause()
        if page % 10 == 0:
            wait = np.random.choice(range(40,70))
            "Page {0} - Sleeping {1} seconds".format(page, wait)
            sleep(wait)
        else:
            pass
    return df


if __name__ == "__main__":
    company = input('Enter company name:')
    today = datetime.datetime.today()
    date = "{0}-{1}-{2}".format(str(today.month), str(today.day), str(today.year))
    all_reviews = get_company_reviews(company, checkpoint=True)
    all_reviews.to_csv('{0}_glassdoor_{1}.csv'.format(company, date),index=False)
