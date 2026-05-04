import datetime
import sys
import unittest
from unittest.mock import MagicMock, patch

# Mock third-party dependencies that might not be installed
mock_modules = {
    'PIL': MagicMock(),
    'PIL.Image': MagicMock(),
    'PIL.ImageDraw': MagicMock(),
    'PIL.ImageFont': MagicMock(),
    'google': MagicMock(),
    'google.oauth2': MagicMock(),
    'google.oauth2.credentials': MagicMock(),
    'google.oauth2.service_account': MagicMock(),
    'google.auth': MagicMock(),
    'google.auth.transport': MagicMock(),
    'google.auth.transport.requests': MagicMock(),
    'google_auth_oauthlib': MagicMock(),
    'google_auth_oauthlib.flow': MagicMock(),
    'googleapiclient': MagicMock(),
    'googleapiclient.discovery': MagicMock(),
    'googleapiclient.http': MagicMock(),
    'google.generativeai': MagicMock(),
    'requests': MagicMock(),
    'imageio_ffmpeg': MagicMock(),
    'moviepy': MagicMock(),
    'moviepy.editor': MagicMock(),
    'dotenv': MagicMock(),
    'vertexai': MagicMock(),
    'vertexai.preview': MagicMock(),
    'vertexai.preview.vision_models': MagicMock(),
}

with patch.dict('sys.modules', mock_modules):
    from execution.agencia_dl import _tema_do_dia, _TEMAS_CICLO, _DATA_REFERENCIA

class TestAgenciaDL(unittest.TestCase):
    def test_tema_do_dia_hoje_padrao(self):
        """Test that _tema_do_dia uses today's date if no date is provided."""
        today = datetime.date.today()
        expected_dia_ciclo = (today - _DATA_REFERENCIA).days % len(_TEMAS_CICLO)
        expected_tema = _TEMAS_CICLO[expected_dia_ciclo]

        self.assertEqual(_tema_do_dia(), expected_tema)

    def test_tema_do_dia_data_especifica(self):
        """Test that _tema_do_dia calculates the correct theme for a specific date."""
        # Using a date exactly 1 day after reference data
        test_date = _DATA_REFERENCIA + datetime.timedelta(days=1)
        # Expected is day 1 index, which is the 2nd item in the list
        self.assertEqual(_tema_do_dia(test_date), _TEMAS_CICLO[1])

        # Test 10 days after, should wrap around (10 % 4 = 2) -> 3rd item
        test_date_10 = _DATA_REFERENCIA + datetime.timedelta(days=10)
        self.assertEqual(_tema_do_dia(test_date_10), _TEMAS_CICLO[2])

    def test_tema_do_dia_marco_zero(self):
        """Test that _tema_do_dia returns the first theme on the reference date."""
        self.assertEqual(_tema_do_dia(_DATA_REFERENCIA), _TEMAS_CICLO[0])

if __name__ == '__main__':
    unittest.main()
