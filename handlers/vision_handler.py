import os
from openai import OpenAI
from dotenv import load_dotenv

# llm_config
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")


class OpenAi_llm:
    def __init__(self) -> None:
        self.openai_client = OpenAI(api_key=api_key)

    def parse_url_to_vision_model(self, urls: list[str]) -> str | None:
        """
        Generates a list of dictionaries where each dictionary contains an 'image_url' key.
        The value of 'image_url' is a dictionary with the 'url' key and its corresponding value from the 'urls' list.
        When unpacked ('*' operator) (e.g., iterating over the list), each dictionary will look like:
        {"type": "image_url", "image_url": {"url": "url1"}}
        {"type": "image_url", "image_url": {"url": "url2"}}
        """
        message = [
            {
                "role": "system",
                "content": "Make use of the context provided and make sure your response is accurate",
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Who was the sixth richest person in 2006?",
                    },
                    *[{"type": "image_url", "image_url": {"url": url}} for url in urls],
                ],
            },
        ]
        response = self.openai_client.chat.completions.create(
            model="gpt-4o", messages=message
        )
        llm_response: str | None = response.choices[0].message.content
        return llm_response
