import unittest
from calculateFitScore import calculate_fit_score 
from calculateFitScore import preprocess_text

class TestCalculateFitScore(unittest.TestCase):

    def test_identical_texts(self):
        """
        Test when the resume and job description are identical.
        """
        resume_text = "Python developer with experience in APIs and AWS."
        job_description = "Python developer with experience in APIs and AWS."
        result = calculate_fit_score(resume_text, job_description)
        self.assertEqual(result["fit_score"], 100)
        self.assertEqual(set(result["matched_keywords"]), {"python", "developer", "with", "experience", "in", "apis", "and", "aws"})
        self.assertEqual(len(result["unmatched_critical_keywords"]), 0)

    def test_partial_match(self):
        """
        Test when the resume matches part of the job description.
        """
        resume_text = "Python and Java developer."
        job_description = "Looking for a Python developer with AWS experience."
        result = calculate_fit_score(resume_text, job_description)
        self.assertGreater(result["fit_score"], 0)
        self.assertIn("python", result["matched_keywords"])
        self.assertIn("aws", result["unmatched_critical_keywords"])

    def test_no_match(self):
        """
        Test when the resume and job description have no overlapping keywords.
        """
        resume_text = "hi hello sir"
        job_description = "no man"
        result = calculate_fit_score(resume_text, job_description)
        self.assertEqual(result["fit_score"], 0)  # Ensure score is 0 for no matches


    def test_empty_resume(self):
        """
        Test when the resume is empty.
        """
        resume_text = ""
        job_description = "Looking for a software developer with Python experience."
        result = calculate_fit_score(resume_text, job_description)
        self.assertEqual(result["fit_score"], 0)
        self.assertEqual(len(result["matched_keywords"]), 0)

    def test_empty_job_description(self):
        """
        Test when the job description is empty.
        """
        resume_text = "Experienced Python developer."
        job_description = ""
        result = calculate_fit_score(resume_text, job_description)
        self.assertEqual(result["fit_score"], 0)
        self.assertEqual(len(result["matched_keywords"]), 0)

    def test_empty_both_inputs(self):
        """
        Test when both inputs are empty.
        """
        resume_text = ""
        job_description = ""
        result = calculate_fit_score(resume_text, job_description)
        self.assertEqual(result["fit_score"], 0)
        self.assertEqual(len(result["matched_keywords"]), 0)

    def test_non_string_inputs(self):
        """
        Test when inputs are not strings.
        """
        resume_text = 12345  # Invalid input type
        job_description = ["Python", "developer"]  # Invalid input type
        result = calculate_fit_score(resume_text, job_description)
        self.assertEqual(result["fit_score"], 0)
        self.assertEqual(len(result["matched_keywords"]), 0)

if __name__ == "__main__":
    unittest.main()
