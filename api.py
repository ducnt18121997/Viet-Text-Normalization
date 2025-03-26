import os
import uvicorn
import argparse
from datetime import datetime
from loguru import logger
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from src import TextNormalizer
app = FastAPI()
logger.add(os.path.join(os.path.abspath(os.path.dirname(__file__)), "logs/app.log"), rotation="500 MB", level="INFO", format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <level>{message}</level>")


@app.get("/")
async def ping():

    return JSONResponse({
        "status": "OK",
        "message": "Helloooo, this is API Text Normalization!!!"
    })


@app.get("/get_text")
async def get_text(text: str, domain: str=None):

    return JSONResponse({
        "status": "OK",
        "result" : text_normalizer.normalize(text, domain)[0]
    })


@app.post("/get_text")
async def get_text(request: Request):
    reqs     = await request.json()
    raw_text = reqs["text"].split("\n")
    domain   = reqs["domain"] if "domain" in reqs else None

    normalized_text, new_abbs = [], {}
    for line in raw_text:
        if line.strip().startswith(error_cases):
            continue

        if len(line) > 0:
            normalized_line, new_abbs = text_normalizer(line, new_abbs)
            normalized_text.extend([_line for _line in normalized_line if _line not in ["", "."]])
    
    print(f"- Domain {domain} | Input lengths: {len(reqs['text'])} -> Output lengths {sum([len(line) for line in normalized_text])}")
    return JSONResponse({
        "status": "OK",
        "result" : normalized_text
    })


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--vncorenlp", required=True,
                        help="Path to vncorenlp model")
    parser.add_argument("--port", type=int, default=2000)
    args = parser.parse_args()

    # load models
    error_cases = (
        "Ngân hàng              Kỳ hạn 3 tháng              Kỳ hạn 6 tháng              Kỳ hạn 12 tháng              Kỳ hạn 24 tháng",
        "STTTên sản phẩmNhà chế tạoQuốc gia bị ảnh hưởngKhu vực",
        "STT              Tỉnh, thành phố              Tựu trường              Khai giảng"
    )
    text_normalizer = TextNormalizer(args.vncorenlp, logger=logger)
    
    logger.info(f"Logging api [port {args.port}] starting at {datetime.now().strftime('%m/%d/%Y - %H:%M:%S')}")
    uvicorn.run(app, host="0.0.0.0", port=args.port)
