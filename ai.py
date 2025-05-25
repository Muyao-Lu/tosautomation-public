from openai import OpenAI
from google import genai
from google.genai import types
import json, os


def generate_prompt(policy: str, lang: str, t:str,  mods: list) -> str:
    prompts = json.load(open("prompts.json", "r"))

    content = prompts[t]["normal"]["default-prompts"]["default-prompt-head"]
    content += prompts[t]["normal"]["language-levels"][lang]
    content += prompts[t]["normal"]["default-prompts"]["default-prompt-middle"]
    if mods is not None and t != "t":
        content += prompts[t]["normal"]["additional-prompts"]["additional-prompt-head"]
    
    
        for item in mods:
            try:
                content += prompts[t]["normal"]["additional-prompts"][item]
            except KeyError:
                print("invalid key")
    
    content += prompts[t]["normal"]["default-prompts"]["default-prompt-tail"]
            
    content = content.format(policy=policy)
        
    return content


def generate_short_prompt(policy: str, t: str, lang: str) -> str:
    prompts = json.load(open("prompts.json", "r"))
    content = prompts[t]["short"]["normal"]["short-head"]
    content += prompts[t]["short"]["language-levels"][lang]
    content += prompts[t]["short"]["normal"]["short-tail"]
    content = content.format(policy=policy)
    return content

def call_ai(policy: str, t: str, **kwargs) -> str:# lang: str, mods: list, short: bool) -> str:
    
    token = os.environ["AI_API_KEY"]

    if not kwargs["short"]:
        message = generate_prompt(policy, lang=kwargs["lang"], t=t, mods=kwargs["mod"])
    else:
        message = generate_short_prompt(policy, t=t, lang=kwargs["lang"])

    client = OpenAI(
        base_url="https://models.github.ai/inference",
        api_key=token,
    )
        
    response = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": message,
            }
        ],
        model="openai/gpt-4.1-mini",
    )
        
    return response.choices[0].message.content


def gemini_fallback(policy: str, t: str, **kwargs) -> str:
    client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY"),
    )

    if not kwargs["short"]:
        message = generate_prompt(policy, lang=kwargs["lang"], t=t, mods=kwargs["mod"])
    else:
        message = generate_short_prompt(policy, t=t, lang=kwargs["lang"])

    model = "gemini-2.5-flash-preview-04-17"
    print("model")
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=message),
            ],
        ),
    ]
    print("content successful")
    tools = [
        types.Tool(url_context=types.UrlContext()),
        types.Tool(google_search=types.GoogleSearch()),
    ]
    print("tools successful")
    generate_content_config = types.GenerateContentConfig(
        temperature=0.15,
        top_p=0.7,
        thinking_config = types.ThinkingConfig(
            thinking_budget=0,
        ),
        tools=tools,
        response_mime_type="text/plain",
    )
    print("config successful")
    response = client.models.generate_content(
        model=model,
        contents=contents,
        config=generate_content_config,
    )
    print(response)
    return response
    
    
