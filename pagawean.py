from bs4 import BeautifulSoup as  bs4 
import pandas as pd
import requests

def scrape_find_job(position,location):
    position   = position.lower().replace(' ','-')
    location   = location.lower().replace(' ','-')
    base_url = f'https://id.jobstreet.com/id/{position}-jobs/in-{location}'

    response = requests.get(base_url)
    soup = bs4(response.text,'html.parser')
    jobs = []
    for job_card in soup.find_all('article',{'data-testid' : 'job-card'}): 
        try:
            job_element = job_card.find('a',{'data-testid':'job-card-title'}) 
            title = job_card.find('a',{'data-testid':'job-card-title'}).text.strip()
            company = job_card.find('a',{'data-automation':'jobCompany'}).text.strip()
            link = job_element['href']

            jobs.append({
                        'Title':title,
                        'Company':company,
                        'Job Link':'https://id.jobstreet.com'+link
                        })
        except AttributeError:
            continue
    return pd.DataFrame(jobs)

job_position =input('Job Position : ')
job_location =input('Job Location : ')

job_list = scrape_find_job(job_position,job_location)
df = pd.DataFrame(job_list)
df.to_excel('loker_cocok.xlsx',index=False)
print('Mangga tah lamaran hungkul loba')