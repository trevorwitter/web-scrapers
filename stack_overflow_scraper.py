import requests
from bs4 import BeautifulSoup
import pandas as pd
import math

tags = ["javascript", 
        "java", 
        "c#", 
        "php", 
        "android", 
        "jquery", 
        "python", 
        "html", 
        "c++", 
        "ios", 
        "css", 
        "mysql", 
        "sql", 
        "asp.net", 
        "ruby-on-rails", 
        "objective-c", 
        "c", 
        ".net", 
        "angularjs", 
        "iphone"]

def ensure_punct(page_qs):
    for x in page_qs:
        if x[-1] not in ['!', '.', '?']:
            x = x + '.'
    return page_qs

def posts_scraper(tag,num_qs=2000):
    """Returns list of stack overflow questions tagged as tag"""
    pages = range(1,int(math.ceil(num_qs/50)+1))
    posts = []
    for x in pages:
        print("Getting {0} data -- {1} percent complete".format(tag,int(x/max(pages)*100)))
        url = 'https://stackoverflow.com/questions/tagged/{0}?sort=newest&page={1}&pagesize=50'.format(tag,x)
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        page_qs = [ensure_punct(x.text) for x in soup.find('div',{'id':'questions'}).find_all('a', {'class':'question-hyperlink'})]
        page_excerpts = [x.text for x in soup.find('div',{'id':'questions'}).find_all('div',{'class':'excerpt'})]
        posts += [x.strip()+" "+y.strip() for x,y in zip(page_qs,page_excerpts)]
    return posts

def stack_overflow_scraper(tags, num_qs):
    tag_dict = {}
    for tag in tags:
        posts = posts_scraper2(tag,num_qs=num_qs)
        tag_dict[tag] = posts
    df = pd.DataFrame()
    for x in tag_dict:
        tags = [x for y in range(len(tag_dict[x]))]
        tag_posts = tag_dict[x]
        tag_df = pd.DataFrame({'tags':tags,'post':tag_posts})
        df = df.append(tag_df,ignore_index=True)
    return df

if __name__ == "__main__":
    data = stack_overflow_scraper(tags, num_qs=2000)
    data.to_csv('stack_overflow_tags.csv',index=False)