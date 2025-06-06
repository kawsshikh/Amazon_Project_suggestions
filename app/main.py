import asyncio
import sys

if sys.platform == "win32":
    try:
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    except RuntimeError as e:
        print(f"Could not set event loop policy: {e}. This might happen if the loop is already running.")


from app.utils.html_text import *
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from app.services.reinforce import predict_labels, extract_data
from app.services.web_scrape import *

app_result = FastAPI()

@app_result.get("/", response_class=HTMLResponse)
async def get_form():
    return get_html



@app_result.post("/result", response_class=HTMLResponse)
async def handle_question(question: str = Form(...)):
    tokens = question.split()
    predicted = predict_labels(tokens)
    json_query = extract_data(tokens, predicted)
    df = await scrape(json_query)
    df = pd.DataFrame(df)
    df = filter_table(df, json_query)
    return gen_html(df, json_query)

