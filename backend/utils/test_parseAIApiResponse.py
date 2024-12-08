import unittest
from parseAIApiResponse import parse_ai_api_response  # Replace 'your_module' with the actual module name.

class TestParseAiApiResponse(unittest.TestCase):

    def test_valid_response(self):
        """
        Test parsing of a valid API response.
        """
        api_response = {
            "results": [
                {
                    "fit_score": 0.85,
                    "feedback": [
                        "Add skills related to project management.",
                        "Improve your summary section to include specific achievements."
                    ]
                }
            ]
        }
        result = parse_ai_api_response(api_response)
        self.assertEqual(result["fit_score"], 85)
        self.assertEqual(len(result["feedback"]), 2)

    def test_empty_results(self):
        """
        Test handling of a response with empty results.
        """
        api_response = {"results": []}
        result = parse_ai_api_response(api_response)
        self.assertIn("error", result)

    def test_missing_results_field(self):
        """
        Test handling of a response missing the 'results' field.
        """
        api_response = {}
        result = parse_ai_api_response(api_response)
        self.assertIn("error", result)

    def test_missing_fit_score(self):
        """
        Test handling of a response missing 'fit_score'.
        """
        api_response = {
            "results": [
                {
                    "feedback": ["Add more skills."]
                }
            ]
        }
        result = parse_ai_api_response(api_response)
        self.assertEqual(result["fit_score"], 0)

    def test_invalid_response_format(self):
        """
        Test handling of a completely invalid response format.
        """
        api_response = "invalid data"
        result = parse_ai_api_response(api_response)
        self.assertIn("error", result)

if __name__ == "__main__":
    unittest.main()
