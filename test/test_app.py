from unittest import TestCase
from unittest.mock import patch

from app import app, create_request_body, create_response_body


class TestApp(TestCase):
    def setUp(self) -> None:
        self.test_client = app.test_client()

    @staticmethod
    def mock_rates():
        return {
            "CHF": 0.8,
            "EUR": 1,
            "USD": 2.0,
            "ZWL": 365.45011
        }

    def assert_api_response_is_expected(self, expected, response_data):
        self.assertEqual(expected["currency"], response_data["currency"])
        self.assertEqual(expected["amount"], response_data["amount"])
        self.assertEqual(expected["target_currency"], response_data["target_currency"])
        self.assertEqual(expected["target_amount"], response_data["target_amount"])

    def test_home_is_running(self):
        response = self.test_client.get('/')
        self.assertEqual(200, response.status_code)

    def test_empty_request_gives_warning(self):
        # GIVEN
        request_body = {}

        # WHEN
        response = self.test_client.post('/convert', json=request_body)
        response_data = response.json

        # THEN
        expected = {"warning": "No body was sent."}
        self.assertEqual(expected, response_data)

    @patch("converter.Converter.get_change_rates")
    def test_user_convert_5_eur_is_10_dollars(self, converter):
        # GIVEN
        converter.return_value = TestApp.mock_rates()
        request_body = create_request_body("EUR", 5, "USD")

        # WHEN
        response = self.test_client.post('/convert', json=request_body)
        response_data = response.json

        # THEN
        expected = create_response_body("EUR", 5.0, "USD", 10.0)
        self.assert_api_response_is_expected(expected, response_data)

    @patch("converter.Converter.get_change_rates")
    def test_user_convert_6_eur_is_12_dollars(self, converter):
        # GIVEN
        converter.return_value = TestApp.mock_rates()
        request_body = create_request_body("EUR", 6, "USD")

        # WHEN
        response = self.test_client.post('/convert', json=request_body)
        response_data = response.json

        # THEN
        expected = create_response_body("EUR", 6.0, "USD", 12.0)
        self.assert_api_response_is_expected(expected, response_data)

    @patch("converter.Converter.get_change_rates")
    def test_user_convert_0_eur_is_0_dollars(self, converter):
        # GIVEN
        converter.return_value = TestApp.mock_rates()
        request_body = create_request_body("EUR", 0, "USD")

        # WHEN
        response = self.test_client.post('/convert', json=request_body)
        response_data = response.json

        # THEN
        expected = create_response_body("EUR", 0.0, "USD", 0.0)
        self.assert_api_response_is_expected(expected, response_data)

    @patch("converter.Converter.get_change_rates")
    def test_user_convert_0_chf_is_0_eur(self, converter):
        # GIVEN
        converter.return_value = TestApp.mock_rates()
        request_body = create_request_body("CHF", 0, "EUR")

        # WHEN
        response = self.test_client.post('/convert', json=request_body)
        response_data = response.json

        # THEN
        expected = create_response_body("CHF", 0.0, "EUR", 0.0)
        self.assert_api_response_is_expected(expected, response_data)

    @patch("converter.Converter.get_change_rates")
    def test_user_convert_8_chf_is_10_eur(self, converter):
        # GIVEN
        converter.return_value = TestApp.mock_rates()
        request_body = create_request_body("CHF", 8, "EUR")

        # WHEN
        response = self.test_client.post('/convert', json=request_body)
        response_data = response.json

        # THEN
        expected = create_response_body("CHF", 8.0, "EUR", 10.0)
        self.assert_api_response_is_expected(expected, response_data)

    @patch("converter.Converter.get_change_rates")
    def test_user_convert_8_chf_is_20_usd(self, converter):
        # GIVEN
        converter.return_value = TestApp.mock_rates()
        request_body = create_request_body("CHF", 8, "USD")

        # WHEN
        response = self.test_client.post('/convert', json=request_body)
        response_data = response.json

        # THEN
        expected = create_response_body("CHF", 8.0, "USD", 20.0)
        self.assert_api_response_is_expected(expected, response_data)

    @patch("converter.Converter.get_change_rates")
    def test_user_convert_unknown_currency_gets_error(self, converter):
        # GIVEN
        converter.return_value = TestApp.mock_rates()
        request_body = create_request_body("NOT_VALID_CURRENCY", 8, "USD")

        # WHEN
        response = self.test_client.post('/convert', json=request_body)
        response_data = response.json

        # THEN
        self.assertIsNotNone(response_data.get("error"))
        self.assertEqual(400, response.status_code)

    @patch("converter.Converter.get_change_rates")
    def test_user_convert_unknown_target_currency_gets_error(self, converter):
        # GIVEN
        converter.return_value = TestApp.mock_rates()
        request_body = create_request_body("USD", 8, "NOT_VALID_CURRENCY")

        # WHEN
        response = self.test_client.post('/convert', json=request_body)
        response_data = response.json

        # THEN
        self.assertIsNotNone(response_data.get("error"))
        self.assertEqual(400, response.status_code)
