from bs4 import BeautifulSoup

from db.postgre import Postgre
from web.curl_call import CurlCall


class ScrapPage:
    def __init__(self, url):
        self.url = url
        self.res = self.get_page()

    def get_page(self, url=None):
        curl = CurlCall()
        if url is None:
            url = self.url
        res = curl.curl_call(url, payload=None, headers=None, display_result=False)
        return res

    def get_beauty_page(self, res=None):
        if res is None:
            res = self.res.content
        html = BeautifulSoup(res, 'html.parser')
        return html

    @staticmethod
    def find_counties_locations():
        scrap_page = ScrapPage("https://www.worldatlas.com/webimage/countrys/namerica/us.htm")
        html = scrap_page.get_beauty_page()
        page_hrefs = list()
        for a in html.select('a'):
            href: str = a["href"]
            if "/webimage/countrys/namerica/usstates/" in href and "https://www.worldatlas.com/" not in href:
                href = href.replace(".htm", "latlog.htm")
                page_hrefs.append(f"https://www.worldatlas.com{href}")
        return page_hrefs

    def get_counties_locations(self):
        location_hrefs = ScrapPage.find_counties_locations()
        sql_file = "/Volumes/LaCie/ProjectSup/PythonTools/resources/sqls/states_location.sql"
        postgre = Postgre("localhost", "county", "postgres", "")
        postgre.remove_file(sql_file)
        location_hrefs = list(set(location_hrefs))
        for i, location_href in enumerate(location_hrefs):
            print(f"{location_href} => {i} of {len(location_hrefs)}")
            try:
                res = self.get_page(location_href)
                page = self.get_beauty_page(res.content)
                sections = page.find_all("section", class_="mapContLv2-left")
                for section in sections:
                    try:
                        print("----------section-----------")
                        section.find("ul").clear()
                        clear_section = section.text.replace("LATITUDE & LONGITUDE:", "").replace(
                            "RELATIVE LOCATION:", "").lstrip()
                        state: str = clear_section.rpartition(' Location of')[0]
                        description = clear_section.split("Location of")[1].lstrip()
                        description: str = description.replace("'", "''").replace("hemispheres", "")
                        sql = f"INSERT INTO states_location(state, description, url) VALUES ('{state.lower()}', '{description}', '{location_href}') ON CONFLICT DO NOTHING;"
                        print(sql)
                        postgre.save_to_sql(sql_file, sql + "\n")
                        print("----------------------------")
                    except Exception as e:
                        print(f"error in exception handler {e}")
            except Exception as e:
                print(f"error while scrapping, {e}")
