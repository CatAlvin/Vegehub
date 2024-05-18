from fastapi import FastAPI, HTTPException
from typing import List, Dict, Any
# 导入getReviewWordFrequency函数
from database import api as db_api
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

# 允许的源列表
origins = [
    "http://127.0.0.1:5500",  # 允许来自这个源的请求
    "http://localhost:5500"
]

# 添加 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/reviews/sentence/{vege_id}",
         response_model=List[Dict[str, Any]],
         description="Get the reviews of a vegetable",
         response_description="List of reviews",
         tags=["Reviews"]
         )
async def get_reviews(vege_id: int):
    try:
        reviews_data = db_api.getVegetableReviews(vege_id)
        return reviews_data
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/reviews/words/{vege_id}",
         response_model=Dict[str, int],
         description="Get the word frequency of the reviews of a vegetable",
         response_description="Word frequency of reviews",
         tags=["Reviews"]
         )
async def get_review_words(vege_id: int):
    try:
        word_freq = db_api.getReviewWordFrequency(vege_id)
        return word_freq
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))
