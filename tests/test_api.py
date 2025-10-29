import unittest
import json
from paint_calculator.run import app
from paint_calculator.api import calculate_feet, calculate_gallons_required, sanitize_input


class TestAPI(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_calculate_feet(self):
        data = {'length': '10', 'width': '10', 'height': '8'}
        result = calculate_feet(data)
        self.assertEqual(result, 800)

    def test_calculate_feet_with_different_dimensions(self):
        data = {'length': '12', 'width': '15', 'height': '9'}
        result = calculate_feet(data)
        self.assertEqual(result, 1620)

    def test_calculate_gallons_required(self):
        data = {'ft': 800}
        result = calculate_gallons_required(data)
        self.assertEqual(result, 2)

    def test_calculate_gallons_required_rounds_down(self):
        data = {'ft': 699}
        result = calculate_gallons_required(data)
        self.assertEqual(result, 1)

    def test_sanitize_input_positive(self):
        result = sanitize_input(5)
        self.assertEqual(result, 5)

    def test_sanitize_input_negative(self):
        result = sanitize_input(-5)
        self.assertEqual(result, 5)

    def test_sanitize_input_string(self):
        result = sanitize_input('10')
        self.assertEqual(result, 10)

    def test_calculate_endpoint(self):
        payload = {
            'room-1': {'length': '10', 'width': '10', 'height': '8'},
            'room-2': {'length': '12', 'width': '15', 'height': '9'}
        }
        response = self.app.post('/api/v1/calculate',
                                  data=json.dumps(payload),
                                  content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('room-1', data)
        self.assertIn('room-2', data)
        self.assertIn('total_gallons', data)
        self.assertEqual(data['room-1']['ft'], 800)
        self.assertEqual(data['room-1']['gallons'], 2)
        self.assertEqual(data['room-2']['ft'], 1620)
        self.assertEqual(data['room-2']['gallons'], 4)
        self.assertEqual(data['total_gallons'], 6)

    def test_index_route(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_dimensions_route(self):
        response = self.app.get('/dimensions?rooms=2')
        self.assertEqual(response.status_code, 200)

    def test_results_route(self):
        payload = {
            'length-0': '10',
            'width-0': '10',
            'height-0': '8'
        }
        response = self.app.post('/results', data=payload)
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()

