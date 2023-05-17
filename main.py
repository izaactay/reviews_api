from fastapi import FastAPI
from review_functions import create_url, get_reviews





place_id = "0x60188cf2ebd0b05b:0x95294f4eb1559d4e"

app = FastAPI()

@app.get('/{p_id}')
def get_review_score(p_id: str):
    next_page_token = ""
    url = create_url(place_id, next_page_token)
    token, total_reviews, local_reviews = get_reviews(url, 1)
    count = 1
    while token != "" and count < 10:
        url = create_url(place_id, token)
        token, temp_total, temp_local = get_reviews(url, 2)
        total_reviews += temp_total
        local_reviews += temp_local
        count += 1
    return (local_reviews/total_reviews)*100




