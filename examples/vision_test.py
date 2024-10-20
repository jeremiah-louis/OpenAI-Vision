import os
from openai import OpenAI
from dotenv import load_dotenv

# llm_config
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

urls: list[str] = [
    "https://res.cloudinary.com/dxcb59rb3/image/upload/v1729348325/page21.jpg",
    "https://res.cloudinary.com/dxcb59rb3/image/upload/v1729348327/page20.jpg",
    "https://res.cloudinary.com/dxcb59rb3/image/upload/v1729348328/page22.jpg",
    "https://res.cloudinary.com/dxcb59rb3/image/upload/v1729348330/page23.jpg",
    "https://res.cloudinary.com/dxcb59rb3/image/upload/v1729348332/page27.jpg",
    "https://res.cloudinary.com/dxcb59rb3/image/upload/v1729348334/page9.jpg",
    "https://res.cloudinary.com/dxcb59rb3/image/upload/v1729348337/page8.jpg",
    "https://res.cloudinary.com/dxcb59rb3/image/upload/v1729348339/page26.jpg",
    "https://res.cloudinary.com/dxcb59rb3/image/upload/v1729348340/page32.jpg",
    "https://res.cloudinary.com/dxcb59rb3/image/upload/v1729348342/page24.jpg",
    "https://res.cloudinary.com/dxcb59rb3/image/upload/v1729348344/page30.jpg",
    "https://res.cloudinary.com/dxcb59rb3/image/upload/v1729348346/page18.jpg",
    "https://res.cloudinary.com/dxcb59rb3/image/upload/v1729348348/page19.jpg",
    "https://res.cloudinary.com/dxcb59rb3/image/upload/v1729348350/page31.jpg",
    "https://res.cloudinary.com/dxcb59rb3/image/upload/v1729348352/page25.jpg",
    "https://res.cloudinary.com/dxcb59rb3/image/upload/v1729348354/page28.jpg",
    "https://res.cloudinary.com/dxcb59rb3/image/upload/v1729348356/page14.jpg",
    "https://res.cloudinary.com/dxcb59rb3/image/upload/v1729348358/page6.jpg",
    "https://res.cloudinary.com/dxcb59rb3/image/upload/v1729348360/page7.jpg",
    "https://res.cloudinary.com/dxcb59rb3/image/upload/v1729348361/page15.jpg",
    "https://res.cloudinary.com/dxcb59rb3/image/upload/v1729348364/page29.jpg",
    "https://res.cloudinary.com/dxcb59rb3/image/upload/v1729348366/page17.jpg",
    "https://res.cloudinary.com/dxcb59rb3/image/upload/v1729348368/page5.jpg",
    "https://res.cloudinary.com/dxcb59rb3/image/upload/v1729348370/page4.jpg",
    "https://res.cloudinary.com/dxcb59rb3/image/upload/v1729348371/page16.jpg",
    "https://res.cloudinary.com/dxcb59rb3/image/upload/v1729348373/page12.jpg",
    "https://res.cloudinary.com/dxcb59rb3/image/upload/v1729348375/page0.jpg",
    "https://res.cloudinary.com/dxcb59rb3/image/upload/v1729348376/page1.jpg",
    "https://res.cloudinary.com/dxcb59rb3/image/upload/v1729348378/page13.jpg",
    "https://res.cloudinary.com/dxcb59rb3/image/upload/v1729348380/page11.jpg",
    "https://res.cloudinary.com/dxcb59rb3/image/upload/v1729348382/page3.jpg",
    "https://res.cloudinary.com/dxcb59rb3/image/upload/v1729348383/page2.jpg",
    "https://res.cloudinary.com/dxcb59rb3/image/upload/v1729348385/page10.jpg",
]

message = [
    {
        "role": "system",
        "content": "You are a highly accurate AI assistant equipped with vision capabilities to analyse and extract information from images. Before answering, first look for any contextual information in headers or text that applies. dont hallucinate",
    },
    {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": "Who was the sixth richest person in 2008, their networth and their nationality?",
            },
            *[{"type": "image_url", "image_url": {"url": url}} for url in urls],
        ],
    },
]
response = client.chat.completions.create(
    model="gpt-4o",
    messages=message,
    top_p=0.1,
)
llm_response = response.choices[0].message.content
print(llm_response)
