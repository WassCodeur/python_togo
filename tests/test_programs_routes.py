import unittest

from fastapi.testclient import TestClient

from main import app


class ProgramsRoutesTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_programs_overview_route(self):
        response = self.client.get("/programs")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Python Togo Educational Programs", response.text)

    def test_program_detail_routes(self):
        for path in [
            "/programs/30-days-of-python",
            "/programs/mentorship",
            "/programs/engineering-bootcamp",
            "/education",
            "/certificates",
        ]:
            with self.subTest(path=path):
                response = self.client.get(path)
                self.assertEqual(response.status_code, 200, path)

    def test_navigation_includes_programs(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn('href="/programs"', response.text)

    def test_french_program_pages_are_localized(self):
        checks = [
            ("/programs?lang=fr", "Programmes éducatifs"),
            ("/education?lang=fr", "Éducation à Python Togo"),
            ("/certificates?lang=fr", "Certificats"),
        ]
        for path, expected in checks:
            with self.subTest(path=path):
                response = self.client.get(path)
                self.assertEqual(response.status_code, 200, path)
                self.assertIn(expected, response.text)


if __name__ == "__main__":
    unittest.main()
