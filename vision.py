import os
from openai import OpenAI
from dotenv import load_dotenv

# llm_config
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

from openai import OpenAI

urls = [
    "https://res.cloudinary.com/dxcb59rb3/image/upload/v1728467323/page21.jpg",
    "https://res.cloudinary.com/dxcb59rb3/image/upload/v1728467326/page20.jpg",
    "https://res.cloudinary.com/dxcb59rb3/image/upload/v1728467327/page22.jpg",
    "https://res.cloudinary.com/dxcb59rb3/image/upload/v1728467329/page23.jpg",
    "https://res.cloudinary.com/dxcb59rb3/image/upload/v1728467331/page9.jpg",
    "https://res.cloudinary.com/dxcb59rb3/image/upload/v1728467333/page8.jpg",
    "https://res.cloudinary.com/dxcb59rb3/image/upload/v1728467334/page24.jpg",
    "https://res.cloudinary.com/dxcb59rb3/image/upload/v1728467336/page18.jpg",
    "https://res.cloudinary.com/dxcb59rb3/image/upload/v1728467338/page19.jpg",
    "https://res.cloudinary.com/dxcb59rb3/image/upload/v1728467339/page25.jpg",
    "https://res.cloudinary.com/dxcb59rb3/image/upload/v1728467341/page14.jpg",
    "https://res.cloudinary.com/dxcb59rb3/image/upload/v1728467342/page6.jpg",
    "https://res.cloudinary.com/dxcb59rb3/image/upload/v1728467345/page7.jpg",
    "https://res.cloudinary.com/dxcb59rb3/image/upload/v1728467346/page15.jpg",
    "https://res.cloudinary.com/dxcb59rb3/image/upload/v1728467349/page17.jpg",
    "https://res.cloudinary.com/dxcb59rb3/image/upload/v1728467351/page5.jpg",
    "https://res.cloudinary.com/dxcb59rb3/image/upload/v1728467354/page4.jpg",
    "https://res.cloudinary.com/dxcb59rb3/image/upload/v1728467355/page16.jpg",
    "https://res.cloudinary.com/dxcb59rb3/image/upload/v1728467356/page12.jpg",
    "https://res.cloudinary.com/dxcb59rb3/image/upload/v1728467358/page0.jpg",
    "https://res.cloudinary.com/dxcb59rb3/image/upload/v1728467361/page1.jpg",
    "https://res.cloudinary.com/dxcb59rb3/image/upload/v1728467363/page13.jpg",
    "https://res.cloudinary.com/dxcb59rb3/image/upload/v1728467366/page11.jpg",
    "https://res.cloudinary.com/dxcb59rb3/image/upload/v1728467368/page3.jpg",
    "https://res.cloudinary.com/dxcb59rb3/image/upload/v1728467370/page2.jpg",
    "https://res.cloudinary.com/dxcb59rb3/image/upload/v1728467372/page10.jpg",
]
client = OpenAI()
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "What are in these images? and what is the major summary about them?",
                },
                *[
                    {
                        "type": "image_url",
                        "image_url": {"url": url},
                    }
                    for url in urls
                ],
            ],
        }
    ],
    max_tokens=300,
)
print(response.choices[0].message.content)
