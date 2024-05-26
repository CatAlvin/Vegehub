from fastapi import FastAPI, HTTPException
from typing import List, Dict, Any, Union
# 导入getReviewWordFrequency函数
from fastapi.middleware.cors import CORSMiddleware

from backend import api


app = FastAPI()

# 允许的源列表
origins = [
    "http://127.0.0.1:5500",  # 允许来自这个源的请求
    "http://localhost:5500",
    "http://127.0.0.1:5501",
    "http://localhost:5501"
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
         response_model=Dict[str, List[str]],
         description="Get the reviews of a vegetable",
         response_description="List of reviews",
         tags=["Reviews"]
         )
async def get_review_sentence(vege_id: int):
    try:
        data = api.get_review_sentence(vege_id)
        return data
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/reviews/analyze/{vege_id}",
         response_model=Dict[str, Union[str, Dict[str, float]]],
         description="Get the word frequency of the reviews of a vegetable",
         response_description="Word frequency of reviews",
         tags=["Reviews"]
         )
async def get_review_words(vege_id: int):
    try:
        data = api.get_review_analyze(vege_id)
        return data
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/visualization/{img_name}/{vege_id}",
            response_model=Dict[str, Union[str, None]],
            description="Get the path of the visualization image",
            response_description="Path of the visualization image",
            tags=["Visualization"]
            )
async def get_visualization_img_path(img_name: str, vege_id: int):
    try:
        data = api.get_visualization_img_path(img_name, vege_id)
        return data
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))