import uvicorn
import argparse
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from src import TextNormalizer

app = FastAPI()


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
    reqs            = await request.json()
    raw_text        = reqs["text"].split("\n")
    domain          = reqs["domain"] if "domain" in reqs else None

    normalized_text, new_abbs = [], {}
    for line in raw_text:
        if len(line) > 0:
            normalized_line, new_abbs = text_normalizer.normalize(line, domain, new_abbs)
            normalized_text.extend(normalized_line)
    
    print(f"- Domain {domain} | Input lengths: {len(reqs['text'])} -> Output lengths {sum([len(line) for line in normalized_text])}")
    return JSONResponse({
        "status": "OK",
        "result" : normalized_text
    })


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--checkpoint", default="./src/utils/number_classification_model.pt",
                        help="Classify NSWs number types checkpoint")
    parser.add_argument("--vncorenlp", default="src/vncorenlp/VnCoreNLP-1.1.1.jar",
                        help="Path to vncorenlp model")
    parser.add_argument("--port", type=int, default=2000)
    args = parser.parse_args()

    # load models
    text_normalizer = TextNormalizer(args.checkpoint, args.vncorenlp)
    uvicorn.run(app, host="0.0.0.0", port=args.port)
