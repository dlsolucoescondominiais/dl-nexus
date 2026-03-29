import os
from google import genai
from dotenv import load_dotenv

load_dotenv("/app/execution/.env")
api_key = os.getenv("GEMINI_API_KEY")

try:
    client = genai.Client(api_key=api_key)
    result = client.models.generate_images(
        model='imagen-3.0-generate-001',
        prompt='Um teste de integracao com a api de geracao de imagens do gemini',
        config=dict(
            number_of_images=1,
            output_mime_type="image/jpeg",
        )
    )
    for generated_image in result.generated_images:
        image = generated_image.image
        print(f"Sucesso! Imagem gerada com {len(image.image_bytes)} bytes.")
except Exception as e:
    print(f"Erro: {e}")
