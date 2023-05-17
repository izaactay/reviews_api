import requests
import bs4

def create_url(place_id,token=""):
    url = "https://www.google.com/async/reviewDialog?hl=en_us&async=feature_id:" + place_id + ",next_page_token:" + token + ",sort_by:qualityScore,start_index:,associated_topic:,_fmt:pc"
    return url

def get_site(url):
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.content, 'html.parser')
    return soup



def get_location_info(soup):
    location_info = {}

    for el in soup.select('.lcorif'):
        data_id = soup.select_one('.loris')['data-fid']
        token = soup.select_one('.gws-localreviews__general-reviews-block')['data-next-page-token']
        location_info = {
            'title': soup.select_one('.P5Bobd').text.strip(),
            'address': soup.select_one('.T6pBCe').text.strip(),
            'avgRating': soup.select_one('span.Aq14fc').text.strip(),
            'totalReviews': soup.select_one('span.z5jxId').text.strip()
        }
    return location_info


def get_reviews(soup):
    user = []
    token = ''
    total_reviews = 0
    local_reviews = 0

    for el in soup.select('.gws-localreviews__google-review'):
        total_reviews += 1
        temp_dict = {'name': el.select_one('.TSUbDb').text.strip(),
                     'link': el.select_one('.TSUbDb a')['href'],
                     'rating': el.select_one('.BgXiYe .lTi8oc')['aria-label'],
                     'review': el.select_one('.Jtu6Td').text.strip()}
        full_review_text = el.select_one('.review-full-text')
        if full_review_text == None:
            temp_dict['review'] = el.select_one('.Jtu6Td').text.strip()
            if temp_dict['review'] == '':
                total_reviews-=1
        else:
            temp_dict['review'] = full_review_text.text.strip()
            local_reviews += 1


        user.append(temp_dict)

    return token,total_reviews,local_reviews