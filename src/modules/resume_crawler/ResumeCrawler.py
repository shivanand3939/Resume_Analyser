import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver
import time, os
import pandas as pd
import selenium
import requests
import json
import codecs
import re

class ResumeCrawler:

    def __init__(self, urlpage):
        print( selenium.__file__)
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('disable-infobars')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.driver = webdriver.Chrome(executable_path = 'C:/Users/ACER/Downloads/indeed-resume-scraper-master/chromedriver.exe', chrome_options=chrome_options)
        self.driver.get(urlpage)
        time.sleep(8)


    def get_driver_for_single_resume(self, url):
        chrome_options = webdriver.ChromeOptions()
        #chrome_options.add_argument(seleniumproxy)
        chrome_options.add_argument('disable-infobars')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        child_driver = webdriver.Chrome(executable_path = 'C:/Users/ACER/Downloads/indeed-resume-scraper-master/chromedriver.exe', chrome_options=chrome_options)
        child_driver.get(url)
        time.sleep(1)
        p_element = child_driver.page_source
        soup = BeautifulSoup(p_element, 'lxml')
        return soup, child_driver


    def get_education(self, soup):
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
        education = [dict(t) if type(t) == tuple else t for t in {tuple(d.items()) if type(d) == dict else d for d in education }]
        return education


    def get_work_experience(self, soup):
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
        work_experience = [dict(t) if type(t) == tuple else t for t in {tuple(d.items()) if type(d) == dict else d for d in work_experience }]
        return work_experience


    def get_skills(self, soup) :
        skills=[]
        skill_contents = soup.find_all('div', attrs={'class': 'skills-content'})
        for each_content in skill_contents:
            skill_sections = each_content.find_all('div', attrs={'id': 'skills-items'})
            for each_section in skill_sections:
                skill_texts = each_section.find_all(name='span', attrs={'class': 'skill-text'})
                for each_text in skill_texts:
                    skills.append(each_text.text.strip())
        #skills = [ dict(t) if type(t) == tuple else t for t in {tuple(d.items()) if type(d) == dict else d for d in skills }]
        skills=list(set(skills))
        return skills


    def get_links(self, soup):
        links=[]
        links_contents = soup.find_all('div', attrs={'class': 'links-content'})
        for each_content in links_contents:
            links_sections = each_content.find_all('div', attrs={'id': 'link-items'})
            for each_section in links_sections:
                links_texts = each_section.find_all(name='div', attrs={'class': 'link_url'})
                for each_text in links_texts:
                    links.append(each_text.text.strip())
        #links = [dict(t) if type(t) == tuple else t for t in {tuple(d.items())  if type(d) == dict else d for d in links}]
        links=list(set(links))
        return links


    def get_additional_info(self, soup):
        additional_info=[]
        additionalInfo_contents = soup.find_all('div', attrs={'class': 'additionalInfo-content'})
        for each_content in additionalInfo_contents:
            additionalinfo_sections = each_content.find_all('div', attrs={'id': 'additionalinfo-section'})
            for each_section in additionalinfo_sections:
                additional_info.append(each_section.text.strip())
        #print(type(additional_info), additional_info)
        #additional_info = [dict(t) if type(t) == tuple else t for t in {tuple(d.items()) if type(d) == dict else d for d in additional_info }]
        additional_info=list(set(additional_info))
        return additional_info


    def get_certifications(self, soup):
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
        certifications = [dict(t) if type(t) == tuple else t for t in {tuple(d.items())  if type(d) == dict else d for d in certifications}]
        return certifications


    def get_summaries(self, soup):
        #print(certifications)
        summaries = []
        res_summaries = soup.find_all('div', attrs={'id': 'res_summary'})
        for each_summary in res_summaries:
            res_summary = each_summary.text.strip()
            summaries.append(res_summary)
        summaries=list(set( summaries))
        #summaries = [dict(t) if type(t) == tuple else t for t in {tuple(d.items()) if type(d) == dict else d for d in summaries  }]
        return summaries


    def get_awards(self, soup):
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
        awards = [dict(t) if type(t) == tuple else t for t in {tuple(d.items()) if type(d) == dict else d for d in awards }]
        return awards

    def get_publication(self, soup):
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

        
    def initialise_files(self, file_name,contents,i):
        
            with open('C:/Users/ACER/Resume_Analyser/files/result.json', 'w') as fp:
              json.dump(contents, fp)
            def unmangle_utf8(match):
    
                    escaped = match.group(0)                   # '\\u00e2\\u0082\\u00ac'
                    hexstr = escaped.replace(r'\u', '')      # 'e282ac'
                    buffer = codecs.decode(hexstr, "hex")      # b'\xe2\x82\xac'

                    try:
                           return buffer.decode('utf8')           # '€'
                    except UnicodeDecodeError:
                          print("Could not decode buffer: %s" % buffer)


            
            with open('C:/Users/ACER/Resume_Analyser/files/result.json', 'r') as f:
    
                  for line in f:
             
                        line = re.sub(r"(?i)(?:\\u[0-9a-f]{4})+", unmangle_utf8,line)
                        line=line.replace("\\","")
                        line=line.replace('\\n',"")
                        #line=line.replace('\\',"")
                        line=re.sub("\s\s+", " ", line)
            with open('C:/Users/ACER/Resume_Analyser/files/result'+str(i)+'.json', 'w') as f:
                     json.dump(line,f)
                     


    def get_data(self, soup):
        content={}
        content['summaries'] = self.get_summaries(soup)
        content['education'] = self.get_education(soup)
        content['work_experience'] = self.get_work_experience(soup)
        content['skills'] = self.get_skills(soup)
        content['links'] = self.get_links(soup)
        content['additional_info'] = self.get_additional_info(soup)
        content['certifications'] = self.get_certifications(soup)
        content['awards'] = self.get_awards(soup)
        content['publication'] = self.get_awards(soup)

        return content


    def get_resume_links(self):
        count=0
        urllinks=[]
        elements = self.driver.find_elements_by_css_selector("div.rezemp-ResumeSearchCard a")
        for element in elements:
            count+=1
            urllinks.append(element.get_attribute("href"))


        elements = self.driver.find_elements_by_css_selector("div.rezemp-ResumeSummaryCard a")
        for element in elements:
            count+=1
            urllinks.append(element.get_attribute("href"))

        print(len(urllinks))
        #self.driver.close()

        #contents = []
        i=0
        for url in urllinks:
            i+=1
            soup, child_driver = self.get_driver_for_single_resume(url)
            contents=(self.get_data(soup))
            #child_driver.close()

            self.initialise_files('C:/Users/ACER/Resume_Analyser/files/result.json',contents,i)
            child_driver.close()
