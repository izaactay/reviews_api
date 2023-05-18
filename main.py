from fastapi import FastAPI, HTTPException
from review_functions import create_url, get_reviews, get_site, get_location_info
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ['*'],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/{p_id}')
def get_review_score(p_id: str):
    if p_id == "favicon.ico":
        raise HTTPException(status_code=404, detail="Place not found")
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
    try:
        print(location_info['title'])
    except:
        print('no title')
    return (local_reviews/total_reviews)*100




