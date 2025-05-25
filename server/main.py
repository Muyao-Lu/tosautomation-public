from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated
import sys
import uvicorn, datetime
sys.path.insert(1, "server/")
import ai, convert, scraper


app = FastAPI()

# app.add_middleware(CORSMiddleware,
#                    allow_origins=["https://localhost:63342", "http://localhost:63342"],
#                    allow_credentials=True,
#                    allow_methods=["*"],
#                    allow_headers=["*"])
requests = {}

def check_request_freq(ip):
    last_call = requests[ip]
    time_delta = datetime.datetime.now() - last_call
    return time_delta.seconds >= 10

@app.get("/server/privacy-policy/")
async def root(link: str, ip: str, lang: str = "middle", short: bool = False, modifiers: Annotated[list[str], Query()] = None):
    global requests
    try:
        if check_request_freq(ip):
            pass
        else:
            return "Too many calls. Wait before trying again"
    except KeyError:
        pass

    raw = scraper.scrape(link)
    if len(raw) > 3000:
        text = ai.call_ai(link, "p", lang=lang, mod=modifiers, short=short)
    else:
        text = ai.call_ai(raw, "p", lang=lang, mod=modifiers, short=short)
    requests[ip] = datetime.datetime.now()
    return convert.convert_to_html(text)


@app.get("/server/tos/")
async def root(link: str, ip: str, lang: str = "middle", short: bool = False, modifiers: Annotated[list[str], Query()] = None):
    global requests
    try:

        if check_request_freq(ip):
            pass
        else:
            return "Too many calls. Wait before trying again"
    except KeyError:
        pass

    raw = scraper.scrape(link)
    if len(raw) > 3000:
         text = ai.call_ai(link, "t", lang=lang, mod=modifiers, short=short)
    else:
        text = ai.call_ai(raw, "t", lang=lang, mod=modifiers, short=short)
    
    
    requests[ip] = datetime.datetime.now()
    print(text)
    return convert.convert_to_html(text)


if __name__ == '__main__':
    uvicorn.run(app, port=800)

