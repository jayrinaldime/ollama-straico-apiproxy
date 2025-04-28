from openai import OpenAI, Client
import base64

# Set your OpenAI API key
client = Client(base_url="http://127.0.0.1:3214/v1", api_key="api_key")

def encode_image(image_path):
    """Encode image to base64 string."""
    with open(image_path, 'rb') as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

def describe_image(image_path):
    base64_image = encode_image(image_path)
    response = client.chat.completions.create(
        model="openai/gpt-4.1",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Describe the content of this image in detail."},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        max_tokens=300
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    image_path = "test_img.png"   # Change this to your image filename/path
    description = describe_image(image_path)
    print("Image description:\n", description)