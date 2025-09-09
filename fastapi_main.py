from fastapi import BackgroundTasks, FastAPI, File, UploadFile 
from fastapi.responses import JSONResponse, FileResponse 
from fastapi.responses import StreamingResponse 
from fastapi.staticfiles import StaticFiles 
import uvicorn  
import os 
from fastapi.middleware.cors import CORSMiddleware  

 

app = FastAPI() 
app.add_middleware( CORSMiddleware, 
# allow_origins=[ # "http:/ /localhost:3000", 
# "https://yourdomain.com" # ], 
# allow_credentials=True, 
allow_methods=["POST"], 
# allow_headers=[ # "Content-Type", # "Authorization", # "X-Custom-Header" # 
)

@app.get("/") 
async def root(): 
    async_url_fetcher() 

if __name__==" main ": 
    uvicorn.run(app, host="0.0.0.0", port=7000)
