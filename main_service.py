import json
import os
from turtle import heading
from groq import Groq

client = Groq(
    api_key="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",
)

model = "llama3-70b-8192"

def grab_content(what_is_your_startup_called, what_does_your_startup_offer):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a senior Copywriter with 10 years of experience specializing in copywriting content for Startup landing pages.\n" +
                "Your expertise includes making content that's optimized for SEO and making content that converts users to paid users on a very high rate."
            },
            {   
                "role": "system",
                "content": "All the answers should be direct, without any commentary on your part!"
            },
            {
                "role": "system",
                "content": "I have a startup that's called '" + what_is_your_startup_called + "' which offers " + what_does_your_startup_offer,
            },
            {
                "role": "system",
                "content": "I'm going to ask you for different copywriting parts that I need for my landing page that converts well."
            },
            {
                "role": "system",
                "content": "Give me the contents for my landing page in JSON.\n" +
                f" The JSON object must use the schema: {json.dumps({
                    "headline": "Emphasizes value, result or transformation.",
                    "subheadline": "Clearly explains what you provide to get that result.",
                    "CTA": "str",
                    "benefits": "Include 3 things that the user will benefit from the startup, with a title and text to each one.",
                    "reviews": "3 positive reviews' content, Don't include names, or information about who reviewed them!"
                }, indent=2)}",
            },
        ],
        model=model,
        response_format={"type": "json_object"},
        stream=False,
    )

    return chat_completion.choices[0].message.content
