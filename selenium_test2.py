import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pandas as pd
import selenium
import requests
from selenium.webdriver.support.ui import WebDriverWait
import unicodedata
import codecs
import re
import json
#urlpage='https://resumes.indeed.com/search?q=datascience&l=india&checkbox=jt&searchFields=jt'
#urlpage = 'https://resumes.indeed.com/search?q=datascience&l=india&checkbox=jt&searchFields=jt' 
urlpage='https://resumes.indeed.com/search?l=&q=datascience&searchFields=jt'
print(urlpage)
print( selenium.__file__)
options = webdriver.ChromeOptions()
#options.add_argument("--incognito")
options.add_argument('disable-infobars')
options.add_argument('--disable-extensions')
options.add_experimental_option('excludeSwitches', ['enable-automation'])

driver = webdriver.Chrome(executable_path = 'C:/Users/ACER/Downloads/indeed-resume-scraper-master/chromedriver.exe',options=options)
driver.get(urlpage)
time.sleep(8)
print("hi")
p_element = driver.page_source
soup = BeautifulSoup(p_element, "lxml")
#a=soup.find_all('div', attrs={'class':("rezemp-ResumeSearchCard")})
#links = soup.find_all('span', attrs={'class':("icl-TextLink icl-TextLink--primary rezemp-ResumeSearchCard-displayName")})
count=0
urllinks=[]
elements = driver.find_elements_by_css_selector("div.rezemp-ResumeSearchCard a")
for element in elements:
    count+=1
    urllinks.append(element.get_attribute("href"))


elements = driver.find_elements_by_css_selector("div.rezemp-ResumeSummaryCard a")
for element in elements:
    count+=1
    urllinks.append(element.get_attribute("href"))
print(count)
print(urllinks)
print(len(urllinks))


for i in range(len(urllinks)):
    
    urlpage=urllinks[i]
    print(urlpage)
    driver = webdriver.Chrome(executable_path = 'C:/Users/ACER/Downloads/indeed-resume-scraper-master/chromedriver.exe')
    driver.get(urlpage)
    p_element = driver.page_source
    soup = BeautifulSoup(p_element, 'lxml')
    education=[]

    education_contents = soup.find_all('div', attrs={'class': 'education-content'})

                        
    education_sections = soup.find_all('div', attrs={'class': 'education-section'})
    #print(len(education_contents))
    for each_section in education_sections:
                            education_item = {}
                            titles = each_section.find_all(name='div', attrs={'class': 'edu_title'})
                            for each_title in titles:
                                education_item['title'] = each_title.text.strip()
                            edu_schools = each_section.find_all(name='div', attrs={'class': 'edu_school'})
                            for each_edu_school in edu_schools:
                                education_item['school'] = each_edu_school.text.strip()
                            edu_dates = each_section.find_all(name='div', attrs={'class': 'edu_dates'})
                            for each_date in edu_dates:
                                education_item['edu_dates'] = each_date.text.strip()
                                #print(education_item['edu_dates'])
                            descriptions = each_section.find_all(name='p', attrs={'class': 'edu_description'})
                            for each_description in descriptions:
                                education_item['description'] = each_description.text.strip()
                            education.append(education_item)	
    #print(education)
    education=([dict(t) for t in {tuple(d.items()) for d in education}])
			

    work_experience=[]
    work_experience_contents = soup.find_all('div', attrs={'class': 'workExperience-content'})
    for each_content in work_experience_contents:
                        work_experience_sections = each_content.find_all('div', attrs={'class': 'work-experience-section'})
                        for each_section in work_experience_sections:
                            work = {}
                            titles = each_section.find_all(name='div', attrs={'class': 'work_title'})
                            for each_title in titles:
                                work['title'] = each_title.text.strip()
                            work_companies = each_section.find_all(name='div', attrs={'class': 'work_company'})
                            for each_company in work_companies:
                                work['company'] = each_company.text.strip()
                            work_dates = each_section.find_all(name='div', attrs={'class': 'work_dates'})
                            for each_date in work_dates:
                                work['work_dates'] = each_date.text.strip()
                            descriptions = each_section.find_all(name='div', attrs={'class': 'work_description'})
                            for each_description in descriptions:
                                work['description'] = each_description.text.strip()
                            work_experience.append(work)
    #print(work_experience)
    work_experience=([dict(t) for t in {tuple(d.items()) for d in work_experience}])
    skills=[]                            
    skill_contents = soup.find_all('div', attrs={'class': 'skills-content'})
    for each_content in skill_contents:
                        skill_sections = each_content.find_all('div', attrs={'id': 'skills-items'})
                        for each_section in skill_sections:
                            skill_texts = each_section.find_all(name='span', attrs={'class': 'skill-text'})
                            for each_text in skill_texts:
                                skills.append(each_text.text.strip())
    #print(skills)
    skills=list(set(skills))
    links=[]
    links_contents = soup.find_all('div', attrs={'class': 'links-content'})
    for each_content in links_contents:
                        links_sections = each_content.find_all('div', attrs={'id': 'link-items'})
                        for each_section in links_sections:
                            links_texts = each_section.find_all(name='div', attrs={'class': 'link_url'})
                            for each_text in links_texts:
                                links.append(each_text.text.strip())
    #print(links)
    links=list(set(links))
    additional_info=[]
    additionalInfo_contents = soup.find_all('div', attrs={'class': 'additionalInfo-content'})
    for each_content in additionalInfo_contents:
                        additionalinfo_sections = each_content.find_all('div', attrs={'id': 'additionalinfo-section'})
                        for each_section in additionalinfo_sections:
                            additional_info.append(each_section.text.strip())
    #print(additional_info)
    additional_info=list(set(additional_info))

    certifications=[]
    certifications__contents = soup.find_all('div', attrs={'class': 'certification-content'})
    for each_content in certifications__contents:
                        certification_sections = each_content.find_all('div', attrs={'class': 'certification-section'})
                        for each_section in certification_sections:
                            certification = {}
                            titles = each_section.find_all(name='div', attrs={'class': 'certification_title'})
                            for each_title in titles:
                                certification['title'] = each_title.text.strip()
                            certification_date = each_section.find_all(name='div', attrs={'class': 'certification_date'})
                            for each_date in certification_date:
                                certification['date'] = each_date.text.strip()
                            
                            descriptions = each_section.find_all(name='div', attrs={'class': 'certification_description'})
                            for each_description in descriptions:
                                certification['description'] = each_description.text.strip()
                            
                                certifications.append(certification)
    #print(certifications)
    certifications=([dict(t) for t in {tuple(d.items()) for d in certifications}])
    res_summary=[]
    res_summaries = soup.find_all('div', attrs={'id': 'res_summary'})
    for each_summary in res_summaries:
                        res_summary.append(each_summary.text.strip())
    res_summary=list(set(res_summary))
    awards=[]                      
    awards_contents = soup.find_all('div', attrs={'class': 'awards-content'})
    for each_content in awards_contents:
                        awards_sections = each_content.find_all('div', attrs={'class': 'award-section'})
                        for each_section in awards_sections:
                            award_item = {}
                            titles = each_section.find_all(name='div', attrs={'class': 'award_title'})
                            for each_title in titles:
                                award_item['title'] = each_title.text.strip()
                            award_dates = each_section.find_all(name='div', attrs={'class': 'award_date'})
                            for each_date in award_dates:
                                award_item['date'] = each_date.text.strip()
                            descriptions = each_section.find_all(name='div', attrs={'class': 'award_description'})
                            for each_description in descriptions:
                                award_item['description'] = each_description.text.strip()
                            awards.append(award_item)
    #print(awards)
    awards=([dict(t) for t in {tuple(d.items()) for d in awards}])
    publication=[]
    publication_contents = soup.find_all('div', attrs={'class': 'publications-content'})
    publication=[]                      
    publication_sections = soup.find_all('div', attrs={'class': 'publication-section'})
    #print(len(education_contents))
    for each_section in publication_sections:
                            #print(each_section)
                            publication_item = {}
                            titles = each_section.find_all(name='div', attrs={'class': 'publication_title'})
                            for each_title in titles:
                                publication_item['title'] = each_title.text.strip()
                            publication_date = each_section.find_all(name='div', attrs={'class': 'publication_date'})
                            for each_date in publication_date:
                                publication_item['date'] = each_date.text.strip()
                            publication_url = each_section.find_all(name='div', attrs={'class': ' publication_url'})
                            
                            for each_url in  publication_url:
                                
                                publication_item [' publication_url'] = driver.find_elements_by_css_selector("div. publication_url a").get_attribute('href')
                                print(publication_item [' publication_url'])
                            publication.append(publication_item)
                                                
                        
    publication=([dict(t) for t in {tuple(d.items()) for d in publication}]) 
    content={}
    #content['res_summaries'] = res_summaries
    content['res_summary'] = res_summary
    content['education'] = education
    content['work_experience']=work_experience
    content['links']=links
    content['certifications']=certifications
    content['awards']=awards
    content['skills'] = skills
    content['additional_info'] = additional_info
    content['publication'] = publication
    #print(content)
    with open('result.json', 'w') as fp:
            json.dump(content, fp)
    
    def unmangle_utf8(match):
    
        escaped = match.group(0)                   # '\\u00e2\\u0082\\u00ac'
        hexstr = escaped.replace(r'\u', '')      # 'e282ac'
        buffer = codecs.decode(hexstr, "hex")      # b'\xe2\x82\xac'

        try:
            return buffer.decode('utf8')           # '€'
        except UnicodeDecodeError:
            print("Could not decode buffer: %s" % buffer)

    with open('result.json', 'r') as f:
    
      for line in f:
       
       
       line = re.sub(r"(?i)(?:\\u[0-9a-f]{4})+", unmangle_utf8,line)
       line=line.replace("\\","")
       line=line.replace('\\n',"")
       #line=line.replace('\\',"")
       line=re.sub("\s\s+", " ", line)
    with open('result'+str(i)+'.json', 'w') as f:
     json.dump(line,f)
    driver.close()
    
 
  
