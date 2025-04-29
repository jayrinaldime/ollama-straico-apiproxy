from ollama import Client, AsyncClient
import base64

# CONFIGURATION
IMAGE_PATH = "test_img.png"  # Change to your image path
BASE_URL = "http://127.0.0.1:3214"
MODEL = "openai/gpt-4.1"
client = Client(host=BASE_URL)


def encode_image(image_path):
    """Encode image to base64 string."""
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")


def main():
    # You can also pass in base64 encoded image data
    # img = base64.b64encode(Path(path).read_bytes()).decode()
    # or the raw bytes
    # img = Path(path).read_bytes()

    response = client.chat(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": "Describe the content of this image in detail.",
                "images": [IMAGE_PATH],
            }
        ],
    )

    print(response.message.content)


if __name__ == "__main__":
    main()
