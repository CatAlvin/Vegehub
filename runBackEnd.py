from backend.main import app
import uvicorn
if __name__ == "__main__":
    # 启动后端服务
    host = "127.0.0.1"
    port = 8000
    uvicorn.run(app, host=host, port=port)