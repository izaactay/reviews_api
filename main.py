from fastapi import FastAPI
from review_functions import create_url, get_reviews, get_site, get_location_info





#place_id = "0x60188cf2ebd0b05b:0x95294f4eb1559d4e"

app = FastAPI()

@app.get('/{p_id}')
def get_review_score(p_id: str):
    next_page_token = ""
    url = create_url(p_id, next_page_token)
    soup = get_site(url)
    location_info = get_location_info(soup)
    token, total_reviews, local_reviews = get_reviews(soup)
    count = 1
    while token != "" and count < 10:
        url = create_url(p_id, token)
        soup = get_site(url)
        token, temp_total, temp_local = get_reviews(soup)
        total_reviews += temp_total
        local_reviews += temp_local
        count += 1

    print(location_info['title'])
    return (local_reviews/total_reviews)*100




