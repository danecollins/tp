from bs4 import BeautifulSoup


class ParsePage:
    menus = {
        u'Add Place': u'/places/add',
        u'Search': u'/places/search',
        u'About': u'/about/',
        u'Blog': u'/blog/archive',
        u'Logout': u'/logout?next=/',
        u'Cities': u'/places/city'
    }

    buttons = {
        u'Login': u'/login',
        u'Register': u'/newuser',
        u'Explore Site': u'/places/city'
    }

    anon_place_fields = [u'City', u'Locale', u'Cuisine',
                         u'Outdoor Seating', u'Dog Friendly']

    user_place_fields = [u'City', u'Locale', u'Cuisine', u'Visit Type',
                         u'Outdoor Seating', u'Dog Friendly', 'Last Visited',
                         u'Rating', u'Good For', u'Comment']

    anon_place_buttons = [u'Open in yelp']

    @classmethod
    def get_title(cls, html):
        soup = BeautifulSoup(html)
        return soup.title.text

    @classmethod
    def get_header(cls, html):
        soup = BeautifulSoup(html)
        # header might be h1 or h3 depending on length
        try:
            head = soup.body.div.h1.text
        except:
            head = soup.body.div.h3.text
        return head

    @classmethod
    def get_menu_links(cls, html):
        soup = BeautifulSoup(html)
        l = {}
        for a in soup.find_all('a', class_="pure-menu-link"):
            l[a.text] = a['href']
        return l

    @classmethod
    def get_button_links(cls, html):
        soup = BeautifulSoup(html)
        l = {}
        for a in soup.find_all('a', class_='pure-button'):
            l[a.text] = a['href']
        return l

    @classmethod
    def get_city_links(cls, html):
        soup = BeautifulSoup(html)
        return soup.find_all('a', class_='city-link')

    @classmethod
    def get_place_fields(cls, html):
        soup = BeautifulSoup(html)
        return [x.text for x in soup.find_all('td', class_='place-field')]

    @classmethod
    def get_place_labels(cls, html):
        soup = BeautifulSoup(html)
        return [x.text for x in soup.find_all('label')]
