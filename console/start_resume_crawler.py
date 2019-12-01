from src.modules.resume_crawler.ResumeCrawler import ResumeCrawler

if __name__ == '__main__':

    urlpage1 = 'https://resumes.indeed.com/search?l=&lmd=all&q=datascience&searchFields=jt%2Cskills'
    urlpage2 = 'https://resumes.indeed.com/search?l=&lmd=all&q=datascience&searchFields=jt%2Cskills&start=50'
    urls = [urlpage1, urlpage2]
    for url in urls:
        res_crawler = ResumeCrawler(url)
        res_crawler.get_resume_links()
