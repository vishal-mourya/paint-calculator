import unittest
import json
from paint_calculator.run import app
from paint_calculator.api import calculate_feet, calculate_gallons_required, sanitize_input


class TestCalculateFeet(unittest.TestCase):
    def test_calculate_feet_standard(self):
        data = {'length': '10', 'width': '10', 'height': '8'}
        result = calculate_feet(data)
        self.assertEqual(result, 800)

    def test_calculate_feet_different_dimensions(self):
        data = {'length': '12', 'width': '15', 'height': '9'}
        result = calculate_feet(data)
        self.assertEqual(result, 1620)

    def test_calculate_feet_minimum_values(self):
        data = {'length': '1', 'width': '1', 'height': '1'}
        result = calculate_feet(data)
        self.assertEqual(result, 1)

    def test_calculate_feet_large_values(self):
        data = {'length': '100', 'width': '100', 'height': '50'}
        result = calculate_feet(data)
        self.assertEqual(result, 500000)

    def test_calculate_feet_zero_length(self):
        data = {'length': '0', 'width': '10', 'height': '8'}
        result = calculate_feet(data)
        self.assertEqual(result, 0)

    def test_calculate_feet_zero_width(self):
        data = {'length': '10', 'width': '0', 'height': '8'}
        result = calculate_feet(data)
        self.assertEqual(result, 0)

    def test_calculate_feet_zero_height(self):
        data = {'length': '10', 'width': '10', 'height': '0'}
        result = calculate_feet(data)
        self.assertEqual(result, 0)

    def test_calculate_feet_float_values(self):
        data = {'length': '10.5', 'width': '12.7', 'height': '8.9'}
        result = calculate_feet(data)
        self.assertEqual(result, 10 * 12 * 8)


class TestCalculateGallonsRequired(unittest.TestCase):
    def test_calculate_gallons_required_standard(self):
        data = {'ft': 800}
        result = calculate_gallons_required(data)
        self.assertEqual(result, 2)

    def test_calculate_gallons_required_rounds_down(self):
        data = {'ft': 699}
        result = calculate_gallons_required(data)
        self.assertEqual(result, 1)

    def test_calculate_gallons_required_exact_multiple(self):
        data = {'ft': 700}
        result = calculate_gallons_required(data)
        self.assertEqual(result, 2)

    def test_calculate_gallons_required_exact_350(self):
        data = {'ft': 350}
        result = calculate_gallons_required(data)
        self.assertEqual(result, 1)

    def test_calculate_gallons_required_less_than_350(self):
        data = {'ft': 349}
        result = calculate_gallons_required(data)
        self.assertEqual(result, 0)

    def test_calculate_gallons_required_zero(self):
        data = {'ft': 0}
        result = calculate_gallons_required(data)
        self.assertEqual(result, 0)

    def test_calculate_gallons_required_large_value(self):
        data = {'ft': 500000}
        result = calculate_gallons_required(data)
        self.assertEqual(result, 1428)

    def test_calculate_gallons_required_one_foot(self):
        data = {'ft': 1}
        result = calculate_gallons_required(data)
        self.assertEqual(result, 0)


class TestSanitizeInput(unittest.TestCase):
    def test_sanitize_input_positive(self):
        result = sanitize_input(5)
        self.assertEqual(result, 5)

    def test_sanitize_input_negative(self):
        result = sanitize_input(-5)
        self.assertEqual(result, 5)

    def test_sanitize_input_string(self):
        result = sanitize_input('10')
        self.assertEqual(result, 10)

    def test_sanitize_input_negative_string(self):
        result = sanitize_input('-15')
        self.assertEqual(result, 15)

    def test_sanitize_input_zero(self):
        result = sanitize_input(0)
        self.assertEqual(result, 0)

    def test_sanitize_input_zero_string(self):
        result = sanitize_input('0')
        self.assertEqual(result, 0)

    def test_sanitize_input_float(self):
        result = sanitize_input(5.7)
        self.assertEqual(result, 5)

    def test_sanitize_input_negative_float(self):
        result = sanitize_input(-5.9)
        self.assertEqual(result, 5)

    def test_sanitize_input_float_string(self):
        result = sanitize_input('10.8')
        self.assertEqual(result, 10)

    def test_sanitize_input_large_number(self):
        result = sanitize_input(999999)
        self.assertEqual(result, 999999)


class TestAPIEndpoint(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_calculate_endpoint_single_room(self):
        payload = {
            'room-1': {'length': '10', 'width': '10', 'height': '8'}
        }
        response = self.app.post('/api/v1/calculate',
                                  data=json.dumps(payload),
                                  content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('room-1', data)
        self.assertIn('total_gallons', data)
        self.assertEqual(data['room-1']['ft'], 800)
        self.assertEqual(data['room-1']['gallons'], 2)
        self.assertEqual(data['room-1']['room'], '1')
        self.assertEqual(data['total_gallons'], 2)

    def test_calculate_endpoint_multiple_rooms(self):
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

    def test_calculate_endpoint_many_rooms(self):
        payload = {
            'room-1': {'length': '10', 'width': '10', 'height': '8'},
            'room-2': {'length': '12', 'width': '15', 'height': '9'},
            'room-3': {'length': '20', 'width': '20', 'height': '10'},
            'room-4': {'length': '15', 'width': '15', 'height': '12'},
            'room-5': {'length': '8', 'width': '10', 'height': '9'}
        }
        response = self.app.post('/api/v1/calculate',
                                  data=json.dumps(payload),
                                  content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data) - 1, 5)
        self.assertIn('total_gallons', data)

    def test_calculate_endpoint_zero_dimensions(self):
        payload = {
            'room-1': {'length': '0', 'width': '0', 'height': '0'}
        }
        response = self.app.post('/api/v1/calculate',
                                  data=json.dumps(payload),
                                  content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['room-1']['ft'], 0)
        self.assertEqual(data['room-1']['gallons'], 0)

    def test_calculate_endpoint_small_room(self):
        payload = {
            'room-1': {'length': '5', 'width': '5', 'height': '8'}
        }
        response = self.app.post('/api/v1/calculate',
                                  data=json.dumps(payload),
                                  content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['room-1']['ft'], 200)
        self.assertEqual(data['room-1']['gallons'], 0)

    def test_calculate_endpoint_large_room(self):
        payload = {
            'room-1': {'length': '100', 'width': '100', 'height': '20'}
        }
        response = self.app.post('/api/v1/calculate',
                                  data=json.dumps(payload),
                                  content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['room-1']['ft'], 200000)
        self.assertEqual(data['room-1']['gallons'], 571)


class TestFlaskRoutes(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_index_route(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Enter the number of rooms', response.data)

    def test_dimensions_route_single_room(self):
        response = self.app.get('/dimensions?rooms=1')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Length', response.data)
        self.assertIn(b'Width', response.data)
        self.assertIn(b'Height', response.data)

    def test_dimensions_route_multiple_rooms(self):
        response = self.app.get('/dimensions?rooms=5')
        self.assertEqual(response.status_code, 200)

    def test_dimensions_route_negative_rooms(self):
        response = self.app.get('/dimensions?rooms=-3')
        self.assertEqual(response.status_code, 200)

    def test_dimensions_route_zero_rooms(self):
        response = self.app.get('/dimensions?rooms=0')
        self.assertEqual(response.status_code, 200)

    def test_dimensions_route_large_number(self):
        response = self.app.get('/dimensions?rooms=100')
        self.assertEqual(response.status_code, 200)

    def test_results_route_single_room(self):
        payload = {
            'length-0': '10',
            'width-0': '10',
            'height-0': '8'
        }
        response = self.app.post('/results', data=payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'View Results', response.data)

    def test_results_route_multiple_rooms(self):
        payload = {
            'length-0': '10',
            'width-0': '10',
            'height-0': '8',
            'length-1': '12',
            'width-1': '15',
            'height-1': '9'
        }
        response = self.app.post('/results', data=payload)
        self.assertEqual(response.status_code, 200)

    def test_results_route_many_rooms(self):
        payload = {}
        for i in range(10):
            payload[f'length-{i}'] = '10'
            payload[f'width-{i}'] = '10'
            payload[f'height-{i}'] = '8'
        response = self.app.post('/results', data=payload)
        self.assertEqual(response.status_code, 200)


class TestInputValidation(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_empty_room_input_on_index(self):
        response = self.app.get('/dimensions?rooms=')
        self.assertEqual(response.status_code, 500)

    def test_missing_length_field(self):
        payload = {
            'width-0': '10',
            'height-0': '8'
        }
        response = self.app.post('/results', data=payload)
        self.assertEqual(response.status_code, 500)

    def test_missing_width_field(self):
        payload = {
            'length-0': '10',
            'height-0': '8'
        }
        response = self.app.post('/results', data=payload)
        self.assertEqual(response.status_code, 500)

    def test_missing_height_field(self):
        payload = {
            'length-0': '10',
            'width-0': '10'
        }
        response = self.app.post('/results', data=payload)
        self.assertEqual(response.status_code, 500)

    def test_empty_length_value(self):
        payload = {
            'length-0': '',
            'width-0': '10',
            'height-0': '8'
        }
        response = self.app.post('/results', data=payload)
        self.assertEqual(response.status_code, 500)

    def test_empty_width_value(self):
        payload = {
            'length-0': '10',
            'width-0': '',
            'height-0': '8'
        }
        response = self.app.post('/results', data=payload)
        self.assertEqual(response.status_code, 500)

    def test_empty_height_value(self):
        payload = {
            'length-0': '10',
            'width-0': '10',
            'height-0': ''
        }
        response = self.app.post('/results', data=payload)
        self.assertEqual(response.status_code, 500)

    def test_all_empty_values(self):
        payload = {
            'length-0': '',
            'width-0': '',
            'height-0': ''
        }
        response = self.app.post('/results', data=payload)
        self.assertEqual(response.status_code, 500)

    def test_api_missing_length(self):
        payload = {
            'room-1': {'width': '10', 'height': '8'}
        }
        response = self.app.post('/api/v1/calculate',
                                  data=json.dumps(payload),
                                  content_type='application/json')
        self.assertEqual(response.status_code, 500)

    def test_api_missing_width(self):
        payload = {
            'room-1': {'length': '10', 'height': '8'}
        }
        response = self.app.post('/api/v1/calculate',
                                  data=json.dumps(payload),
                                  content_type='application/json')
        self.assertEqual(response.status_code, 500)

    def test_api_missing_height(self):
        payload = {
            'room-1': {'length': '10', 'width': '10'}
        }
        response = self.app.post('/api/v1/calculate',
                                  data=json.dumps(payload),
                                  content_type='application/json')
        self.assertEqual(response.status_code, 500)

    def test_api_empty_length_value(self):
        payload = {
            'room-1': {'length': '', 'width': '10', 'height': '8'}
        }
        response = self.app.post('/api/v1/calculate',
                                  data=json.dumps(payload),
                                  content_type='application/json')
        self.assertEqual(response.status_code, 500)

    def test_api_empty_width_value(self):
        payload = {
            'room-1': {'length': '10', 'width': '', 'height': '8'}
        }
        response = self.app.post('/api/v1/calculate',
                                  data=json.dumps(payload),
                                  content_type='application/json')
        self.assertEqual(response.status_code, 500)

    def test_api_empty_height_value(self):
        payload = {
            'room-1': {'length': '10', 'width': '10', 'height': ''}
        }
        response = self.app.post('/api/v1/calculate',
                                  data=json.dumps(payload),
                                  content_type='application/json')
        self.assertEqual(response.status_code, 500)

    def test_api_all_empty_values(self):
        payload = {
            'room-1': {'length': '', 'width': '', 'height': ''}
        }
        response = self.app.post('/api/v1/calculate',
                                  data=json.dumps(payload),
                                  content_type='application/json')
        self.assertEqual(response.status_code, 500)

    def test_api_empty_payload(self):
        payload = {}
        response = self.app.post('/api/v1/calculate',
                                  data=json.dumps(payload),
                                  content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_non_numeric_length(self):
        payload = {
            'length-0': 'abc',
            'width-0': '10',
            'height-0': '8'
        }
        response = self.app.post('/results', data=payload)
        self.assertEqual(response.status_code, 500)

    def test_non_numeric_width(self):
        payload = {
            'length-0': '10',
            'width-0': 'xyz',
            'height-0': '8'
        }
        response = self.app.post('/results', data=payload)
        self.assertEqual(response.status_code, 500)

    def test_non_numeric_height(self):
        payload = {
            'length-0': '10',
            'width-0': '10',
            'height-0': 'def'
        }
        response = self.app.post('/results', data=payload)
        self.assertEqual(response.status_code, 500)

    def test_special_characters_in_dimensions(self):
        payload = {
            'length-0': '@#$',
            'width-0': '!%^',
            'height-0': '&*()'
        }
        response = self.app.post('/results', data=payload)
        self.assertEqual(response.status_code, 500)


if __name__ == '__main__':
    unittest.main()

