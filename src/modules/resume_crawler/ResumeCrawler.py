import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pandas as pd
import selenium
import requests
import json

class ResumeCrawler:

    def __init__(self):
        urlpage = 'https://resumes.indeed.com/search?q=datascience&l=&searchFields='
        #urlpage = 'https://resumes.indeed.com/resume/ba0f7ffb7d5bc285?s=l%3D%26q%3Ddatascience%26searchFields%3Djt'
        #print(urlpage)
        print( selenium.__file__)
        chrome_options = webdriver.ChromeOptions()
        #chrome_options.add_argument(seleniumproxy)
        chrome_options.add_argument('disable-infobars')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        driver = webdriver.Chrome(executable_path = 'files/chromedriver', chrome_options=chrome_options)
        driver.get(urlpage)
        p_element = driver.page_source
        self.soup = BeautifulSoup(p_element, 'lxml')


    def get_education(self):
        education=[]
        education_contents = self.soup.find_all('div', attrs={'class': 'education-content'})
        education_sections = self.soup.find_all('div', attrs={'class': 'education-section'})
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
        return education


    def get_work_experience(self):
        work_experience=[]
        work_experience_contents = self.soup.find_all('div', attrs={'class': 'workExperience-content'})
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
        return work_experience


    def get_skills(self) :
        skills=[]
        skill_contents = self.soup.find_all('div', attrs={'class': 'skills-content'})
        for each_content in skill_contents:
            skill_sections = each_content.find_all('div', attrs={'id': 'skills-items'})
            for each_section in skill_sections:
                skill_texts = each_section.find_all(name='span', attrs={'class': 'skill-text'})
                for each_text in skill_texts:
                    skills.append(each_text.text.strip())
        return skills


    def get_links(self):
        links=[]
        links_contents = self.soup.find_all('div', attrs={'class': 'links-content'})
        for each_content in links_contents:
            links_sections = each_content.find_all('div', attrs={'id': 'link-items'})
            for each_section in links_sections:
                links_texts = each_section.find_all(name='div', attrs={'class': 'link_url'})
                for each_text in links_texts:
                    links.append(each_text.text.strip())
        return links


    def get_additional_info(self):
        additional_info=[]
        additionalInfo_contents = self.soup.find_all('div', attrs={'class': 'additionalInfo-content'})
        for each_content in additionalInfo_contents:
            additionalinfo_sections = each_content.find_all('div', attrs={'id': 'additionalinfo-section'})
            for each_section in additionalinfo_sections:
                additional_info = each_section.text.strip()
        return additional_info


    def get_certifications(self):
        certifications=[]
        certifications__contents = self.soup.find_all('div', attrs={'class': 'certification-content'})
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
        return certifications


    def get_summaries(self):
        #print(certifications)
        summaries = []
        res_summaries = self.soup.find_all('div', attrs={'id': 'res_summary'})
        for each_summary in res_summaries:
            res_summary = each_summary.text.strip()
            summaries.append(res_summary)
        return summaries


    def get_awards(self):
        awards=[]
        awards_contents = self.soup.find_all('div', attrs={'class': 'awards-content'})
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
        return awards


    def get_data(self):
        content={}
        content['education'] = self.get_education()
        content['work_experience'] = self.get_work_experience()
        content['skills'] = self.get_skills()
        content['links'] = self.get_links()
        content['additional_info'] = self.get_additional_info()
        content['certifications'] = self.get_certifications()
        content['summaries'] = self.get_summaries()
        content['awards'] = self.get_awards()


        with open('files/result.json', 'w') as fp:
            json.dump(content, fp)
