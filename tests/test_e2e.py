import unittest
import sys
import os
from playwright.sync_api import sync_playwright, expect

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PageObjects import HomePage, DimensionsPage, ResultsPage, PaintCalculatorApp


class BaseE2ETest(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch(headless=True)
    
    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.playwright.stop()
    
    def setUp(self):
        self.context = self.browser.new_context()
        self.page = self.context.new_page()
        
        self.home_page = HomePage(self.page)
        self.dimensions_page = DimensionsPage(self.page)
        self.results_page = ResultsPage(self.page)
        self.app = PaintCalculatorApp(self.page)
    
    def tearDown(self):
        self.context.close()


class TestE2EBasicFlow(BaseE2ETest):
    
    def test_full_paint_calculator_flow_two_rooms(self):
        room_data = [(10, 10, 8), (12, 15, 9)]
        self.app.complete_calculation_flow(room_data, verify_results=True)
    
    def test_single_room_calculation(self):
        self.app.complete_calculation_same_dimensions(num_rooms=1, length=10, width=10, height=8)
    
    def test_three_rooms_calculation(self):
        self.home_page.navigate()
        self.home_page.submit_room_count(3)
        
        self.dimensions_page.verify_page_loaded()
        row_count = self.dimensions_page.get_table_row_count()
        self.assertEqual(row_count, 4)
        
        room_data = [(10, 10, 8), (12, 15, 9), (20, 20, 10)]
        self.dimensions_page.fill_all_rooms(room_data)
        self.dimensions_page.click_submit()
        
        self.results_page.verify_page_loaded()
    
    def test_five_rooms_calculation(self):
        self.app.complete_calculation_same_dimensions(num_rooms=5, length=10, width=10, height=8)
    
    def test_ten_rooms_calculation(self):
        self.home_page.navigate()
        self.home_page.submit_room_count(10)
        
        self.dimensions_page.verify_page_loaded()
        row_count = self.dimensions_page.get_table_row_count()
        self.assertEqual(row_count, 11)


class TestE2EEdgeCases(BaseE2ETest):
    
    def test_minimum_dimensions(self):
        room_data = [(1, 1, 1)]
        self.app.complete_calculation_flow(room_data, verify_results=False)
    
    def test_large_dimensions(self):
        room_data = [(100, 100, 50)]
        self.app.complete_calculation_flow(room_data, verify_results=False)
    
    def test_mixed_dimension_sizes(self):
        room_data = [(1, 1, 1), (50, 50, 25), (10, 12, 8)]
        self.app.complete_calculation_flow(room_data, verify_results=False)
    
    def test_very_large_number_of_rooms(self):
        self.home_page.navigate()
        self.home_page.submit_room_count(20)
        
        self.dimensions_page.verify_page_loaded()
        row_count = self.dimensions_page.get_table_row_count()
        self.assertEqual(row_count, 21)


class TestE2EModalInteraction(BaseE2ETest):
    
    def test_modal_opens_and_closes(self):
        self.app.complete_calculation_same_dimensions(num_rooms=1)
        
        self.results_page.click_view_results()
        self.results_page.wait_for_modal_visible()
        
        self.results_page.close_modal()
    
    def test_modal_displays_results(self):
        self.app.complete_calculation_same_dimensions(num_rooms=1, length=10, width=10, height=8)
        
        self.results_page.open_results_modal()
        self.results_page.verify_modal_content()
    
    def test_view_results_button_exists(self):
        self.app.complete_calculation_same_dimensions(num_rooms=1)
        self.results_page.verify_view_results_button()


class TestE2EPageElements(BaseE2ETest):
    
    def test_homepage_elements(self):
        self.home_page.navigate()
    
    def test_dimensions_page_table_structure(self):
        self.home_page.navigate()
        self.home_page.submit_room_count(2)
        
        self.dimensions_page.verify_page_loaded()
        header_count = self.dimensions_page.get_table_header_count()
        self.assertEqual(header_count, 4)
    
    def test_dimensions_page_input_fields(self):
        self.home_page.navigate()
        self.home_page.submit_room_count(1)
        
        self.dimensions_page.verify_page_loaded()
        
        length_input = self.dimensions_page.get_length_input(0)
        width_input = self.dimensions_page.get_width_input(0)
        height_input = self.dimensions_page.get_height_input(0)
        
        expect(length_input).to_be_visible()
        expect(width_input).to_be_visible()
        expect(height_input).to_be_visible()
    
    def test_results_page_modal_structure(self):
        self.app.complete_calculation_same_dimensions(num_rooms=1)
        
        self.results_page.open_results_modal()
        self.results_page.verify_modal_content()


class TestE2EDataValidation(BaseE2ETest):
    
    def test_small_room_less_than_one_gallon(self):
        room_data = [(5, 5, 8)]
        self.app.complete_calculation_flow(room_data, verify_results=True)
    
    def test_exact_350_square_feet(self):
        room_data = [(10, 7, 5)]
        self.app.complete_calculation_flow(room_data, verify_results=False)
    
    def test_multiple_rooms_total_calculation(self):
        self.home_page.navigate()
        self.home_page.submit_room_count(4)
        
        self.dimensions_page.verify_page_loaded()
        self.dimensions_page.fill_all_rooms_same_dimensions(4, 10, 10, 8)
        self.dimensions_page.click_submit()
        
        self.results_page.verify_page_loaded()
        self.results_page.open_results_modal()
        self.results_page.verify_total_gallons_visible()


class TestE2EInputValidation(BaseE2ETest):
    
    def test_required_field_validation_on_index(self):
        self.home_page.navigate()
        required_attr = self.home_page.get_rooms_input_attribute('required')
        self.assertIsNotNone(required_attr)
    
    def test_required_fields_on_dimensions_page(self):
        self.home_page.navigate()
        self.home_page.submit_room_count(1)
        
        self.dimensions_page.verify_page_loaded()
        
        length_input = self.dimensions_page.get_length_input(0)
        width_input = self.dimensions_page.get_width_input(0)
        height_input = self.dimensions_page.get_height_input(0)
        
        self.assertIsNotNone(length_input.get_attribute('required'))
        self.assertIsNotNone(width_input.get_attribute('required'))
        self.assertIsNotNone(height_input.get_attribute('required'))
    
    def test_minimum_value_validation(self):
        self.home_page.navigate()
        self.home_page.submit_room_count(1)
        
        self.dimensions_page.verify_page_loaded()
        
        self.dimensions_page.verify_input_attributes(
            room_index=0,
            expected_type='number',
            expected_min='1',
            should_be_required=True
        )
    
    def test_input_type_validation(self):
        self.home_page.navigate()
        rooms_type = self.home_page.get_rooms_input_attribute('type')
        self.assertEqual(rooms_type, 'number')
        
        self.home_page.submit_room_count(1)
        self.dimensions_page.verify_page_loaded()
        
        self.dimensions_page.verify_input_attributes(room_index=0)


if __name__ == '__main__':
    unittest.main()
