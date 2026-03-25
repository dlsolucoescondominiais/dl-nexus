import os
import pytest
from unittest.mock import patch, MagicMock

@patch('google.genai.Client')
def test_generate_image(mock_client_class):
    # Set up mock
    mock_client = mock_client_class.return_value
    mock_result = MagicMock()
    mock_image = MagicMock()
    mock_image.image.image_bytes = b"fake_image_bytes"
    mock_result.generated_images = [mock_image]
    mock_client.models.generate_images.return_value = mock_result

    # Execute
    api_key = "fake_api_key_for_test"

    import google.genai as genai
    client = genai.Client(api_key=api_key)
    result = client.models.generate_images(
        model='imagen-3.0-generate-001',
        prompt='Um teste de integracao com a api de geracao de imagens do gemini',
        config=dict(
            number_of_images=1,
            output_mime_type="image/jpeg",
        )
    )

    # Assert
    assert result.generated_images[0].image.image_bytes == b"fake_image_bytes"
    mock_client.models.generate_images.assert_called_once()
