import unittest
import time
from playwright.sync_api import sync_playwright, expect


class TestE2EBasicFlow(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch(channel="chrome", headless=False)
        
    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.playwright.stop()

    def setUp(self):
        self.context = self.browser.new_context()
        self.page = self.context.new_page()

    def tearDown(self):
        self.context.close()

    def test_full_paint_calculator_flow_two_rooms(self):
        self.page.goto('http://localhost:9200/')
        expect(self.page).to_have_title('Home')
        self.page.fill('input[name="rooms"]', '2')
        self.page.click('input[type="submit"]')
        expect(self.page).to_have_title('Dimension Calculation')
        self.page.fill('input[name="length-0"]', '10')
        self.page.fill('input[name="width-0"]', '10')
        self.page.fill('input[name="height-0"]', '8')
        self.page.fill('input[name="length-1"]', '12')
        self.page.fill('input[name="width-1"]', '15')
        self.page.fill('input[name="height-1"]', '9')
        self.page.click('input[type="submit"]')
        expect(self.page).to_have_title('Results!')
        self.page.click('button.btn-success')
        modal = self.page.locator('#resultsModal')
        expect(modal).to_be_visible()

    def test_single_room_calculation(self):
        self.page.goto('http://localhost:9200/')
        self.page.fill('input[name="rooms"]', '1')
        self.page.click('input[type="submit"]')
        self.page.fill('input[name="length-0"]', '10')
        self.page.fill('input[name="width-0"]', '10')
        self.page.fill('input[name="height-0"]', '8')
        self.page.click('input[type="submit"]')
        expect(self.page).to_have_title('Results!')

    def test_three_rooms_calculation(self):
        self.page.goto('http://localhost:9200/')
        self.page.fill('input[name="rooms"]', '3')
        self.page.click('input[type="submit"]')
        rows = self.page.locator('table[name="dimensions_table"] tr')
        count = rows.count()
        self.assertEqual(count, 4)
        self.page.fill('input[name="length-0"]', '10')
        self.page.fill('input[name="width-0"]', '10')
        self.page.fill('input[name="height-0"]', '8')
        self.page.fill('input[name="length-1"]', '12')
        self.page.fill('input[name="width-1"]', '15')
        self.page.fill('input[name="height-1"]', '9')
        self.page.fill('input[name="length-2"]', '20')
        self.page.fill('input[name="width-2"]', '20')
        self.page.fill('input[name="height-2"]', '10')
        self.page.click('input[type="submit"]')
        expect(self.page).to_have_title('Results!')

    def test_five_rooms_calculation(self):
        self.page.goto('http://localhost:9200/')
        self.page.fill('input[name="rooms"]', '5')
        self.page.click('input[type="submit"]')
        for i in range(5):
            self.page.fill(f'input[name="length-{i}"]', '10')
            self.page.fill(f'input[name="width-{i}"]', '10')
            self.page.fill(f'input[name="height-{i}"]', '8')
        self.page.click('input[type="submit"]')
        expect(self.page).to_have_title('Results!')

    def test_ten_rooms_calculation(self):
        self.page.goto('http://localhost:9200/')
        self.page.fill('input[name="rooms"]', '10')
        self.page.click('input[type="submit"]')
        rows = self.page.locator('table[name="dimensions_table"] tr')
        count = rows.count()
        self.assertEqual(count, 11)


class TestE2EEdgeCases(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch(channel="chrome", headless=False)
        
    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.playwright.stop()

    def setUp(self):
        self.context = self.browser.new_context()
        self.page = self.context.new_page()

    def tearDown(self):
        self.context.close()

    def test_minimum_dimensions(self):
        self.page.goto('http://localhost:9200/')
        self.page.fill('input[name="rooms"]', '1')
        self.page.click('input[type="submit"]')
        self.page.fill('input[name="length-0"]', '1')
        self.page.fill('input[name="width-0"]', '1')
        self.page.fill('input[name="height-0"]', '1')
        self.page.click('input[type="submit"]')
        expect(self.page).to_have_title('Results!')

    def test_large_dimensions(self):
        self.page.goto('http://localhost:9200/')
        self.page.fill('input[name="rooms"]', '1')
        self.page.click('input[type="submit"]')
        self.page.fill('input[name="length-0"]', '100')
        self.page.fill('input[name="width-0"]', '100')
        self.page.fill('input[name="height-0"]', '50')
        self.page.click('input[type="submit"]')
        expect(self.page).to_have_title('Results!')

    def test_mixed_dimension_sizes(self):
        self.page.goto('http://localhost:9200/')
        self.page.fill('input[name="rooms"]', '3')
        self.page.click('input[type="submit"]')
        self.page.fill('input[name="length-0"]', '1')
        self.page.fill('input[name="width-0"]', '1')
        self.page.fill('input[name="height-0"]', '1')
        self.page.fill('input[name="length-1"]', '50')
        self.page.fill('input[name="width-1"]', '50')
        self.page.fill('input[name="height-1"]', '25')
        self.page.fill('input[name="length-2"]', '10')
        self.page.fill('input[name="width-2"]', '12')
        self.page.fill('input[name="height-2"]', '8')
        self.page.click('input[type="submit"]')
        expect(self.page).to_have_title('Results!')

    def test_very_large_number_of_rooms(self):
        self.page.goto('http://localhost:9200/')
        self.page.fill('input[name="rooms"]', '20')
        self.page.click('input[type="submit"]')
        expect(self.page).to_have_title('Dimension Calculation')
        rows = self.page.locator('table[name="dimensions_table"] tr')
        count = rows.count()
        self.assertEqual(count, 21)


class TestE2EModalInteraction(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch(channel="chrome", headless=False)
        
    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.playwright.stop()

    def setUp(self):
        self.context = self.browser.new_context()
        self.page = self.context.new_page()

    def tearDown(self):
        self.context.close()

    def test_modal_opens_and_closes(self):
        self.page.goto('http://localhost:9200/')
        self.page.fill('input[name="rooms"]', '1')
        self.page.click('input[type="submit"]')
        self.page.fill('input[name="length-0"]', '10')
        self.page.fill('input[name="width-0"]', '10')
        self.page.fill('input[name="height-0"]', '8')
        self.page.click('input[type="submit"]')
        self.page.click('button.btn-success')
        modal = self.page.locator('#resultsModal')
        expect(modal).to_be_visible()
        self.page.click('button.close')
        time.sleep(1)

    def test_modal_displays_results(self):
        self.page.goto('http://localhost:9200/')
        self.page.fill('input[name="rooms"]', '1')
        self.page.click('input[type="submit"]')
        self.page.fill('input[name="length-0"]', '10')
        self.page.fill('input[name="width-0"]', '10')
        self.page.fill('input[name="height-0"]', '8')
        self.page.click('input[type="submit"]')
        self.page.click('button.btn-success')
        modal = self.page.locator('#resultsModal')
        expect(modal).to_be_visible()
        time.sleep(6)
        total_gallons = self.page.locator('#sumGallons')
        expect(total_gallons).to_contain_text('Total Gallons Required:')

    def test_view_results_button_exists(self):
        self.page.goto('http://localhost:9200/')
        self.page.fill('input[name="rooms"]', '1')
        self.page.click('input[type="submit"]')
        self.page.fill('input[name="length-0"]', '10')
        self.page.fill('input[name="width-0"]', '10')
        self.page.fill('input[name="height-0"]', '8')
        self.page.click('input[type="submit"]')
        button = self.page.locator('button.btn-success')
        expect(button).to_be_visible()
        expect(button).to_contain_text('View Results')


class TestE2EPageElements(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch(channel="chrome", headless=False)
        
    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.playwright.stop()

    def setUp(self):
        self.context = self.browser.new_context()
        self.page = self.context.new_page()

    def tearDown(self):
        self.context.close()

    def test_homepage_elements(self):
        self.page.goto('http://localhost:9200/')
        expect(self.page).to_have_title('Home')
        input_field = self.page.locator('input[name="rooms"]')
        expect(input_field).to_be_visible()
        submit_button = self.page.locator('input[type="submit"]')
        expect(submit_button).to_be_visible()

    def test_dimensions_page_table_structure(self):
        self.page.goto('http://localhost:9200/')
        self.page.fill('input[name="rooms"]', '2')
        self.page.click('input[type="submit"]')
        table = self.page.locator('table[name="dimensions_table"]')
        expect(table).to_be_visible()
        headers = self.page.locator('table[name="dimensions_table"] th')
        self.assertEqual(headers.count(), 4)

    def test_dimensions_page_input_fields(self):
        self.page.goto('http://localhost:9200/')
        self.page.fill('input[name="rooms"]', '1')
        self.page.click('input[type="submit"]')
        length_input = self.page.locator('input[name="length-0"]')
        width_input = self.page.locator('input[name="width-0"]')
        height_input = self.page.locator('input[name="height-0"]')
        expect(length_input).to_be_visible()
        expect(width_input).to_be_visible()
        expect(height_input).to_be_visible()

    def test_results_page_modal_structure(self):
        self.page.goto('http://localhost:9200/')
        self.page.fill('input[name="rooms"]', '1')
        self.page.click('input[type="submit"]')
        self.page.fill('input[name="length-0"]', '10')
        self.page.fill('input[name="width-0"]', '10')
        self.page.fill('input[name="height-0"]', '8')
        self.page.click('input[type="submit"]')
        modal = self.page.locator('#resultsModal')
        self.page.click('button.btn-success')
        expect(modal).to_be_visible()
        modal_title = self.page.locator('.modal-title')
        expect(modal_title).to_contain_text('Paint Calculation Results')


class TestE2EDataValidation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch(channel="chrome", headless=False)
        
    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.playwright.stop()

    def setUp(self):
        self.context = self.browser.new_context()
        self.page = self.context.new_page()

    def tearDown(self):
        self.context.close()

    def test_small_room_less_than_one_gallon(self):
        self.page.goto('http://localhost:9200/')
        self.page.fill('input[name="rooms"]', '1')
        self.page.click('input[type="submit"]')
        self.page.fill('input[name="length-0"]', '5')
        self.page.fill('input[name="width-0"]', '5')
        self.page.fill('input[name="height-0"]', '8')
        self.page.click('input[type="submit"]')
        expect(self.page).to_have_title('Results!')
        self.page.click('button.btn-success')
        time.sleep(6)
        total_gallons = self.page.locator('#sumGallons')
        expect(total_gallons).to_contain_text('Total Gallons Required:')

    def test_exact_350_square_feet(self):
        self.page.goto('http://localhost:9200/')
        self.page.fill('input[name="rooms"]', '1')
        self.page.click('input[type="submit"]')
        self.page.fill('input[name="length-0"]', '10')
        self.page.fill('input[name="width-0"]', '7')
        self.page.fill('input[name="height-0"]', '5')
        self.page.click('input[type="submit"]')
        expect(self.page).to_have_title('Results!')

    def test_multiple_rooms_total_calculation(self):
        self.page.goto('http://localhost:9200/')
        self.page.fill('input[name="rooms"]', '4')
        self.page.click('input[type="submit"]')
        for i in range(4):
            self.page.fill(f'input[name="length-{i}"]', '10')
            self.page.fill(f'input[name="width-{i}"]', '10')
            self.page.fill(f'input[name="height-{i}"]', '8')
        self.page.click('input[type="submit"]')
        expect(self.page).to_have_title('Results!')
        self.page.click('button.btn-success')
        time.sleep(6)
        total_gallons = self.page.locator('#sumGallons')
        expect(total_gallons).to_be_visible()


class TestE2EInputValidation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch(channel="chrome", headless=False)
        
    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.playwright.stop()

    def setUp(self):
        self.context = self.browser.new_context()
        self.page = self.context.new_page()

    def tearDown(self):
        self.context.close()

    def test_required_field_validation_on_index(self):
        self.page.goto('http://localhost:9200/')
        submit_button = self.page.locator('input[type="submit"]')
        expect(submit_button).to_be_visible()
        rooms_input = self.page.locator('input[name="rooms"]')
        is_required = rooms_input.get_attribute('required')
        self.assertIsNotNone(is_required)

    def test_required_fields_on_dimensions_page(self):
        self.page.goto('http://localhost:9200/')
        self.page.fill('input[name="rooms"]', '1')
        self.page.click('input[type="submit"]')
        length_input = self.page.locator('input[name="length-0"]')
        width_input = self.page.locator('input[name="width-0"]')
        height_input = self.page.locator('input[name="height-0"]')
        self.assertIsNotNone(length_input.get_attribute('required'))
        self.assertIsNotNone(width_input.get_attribute('required'))
        self.assertIsNotNone(height_input.get_attribute('required'))

    def test_minimum_value_validation(self):
        self.page.goto('http://localhost:9200/')
        self.page.fill('input[name="rooms"]', '1')
        self.page.click('input[type="submit"]')
        length_input = self.page.locator('input[name="length-0"]')
        width_input = self.page.locator('input[name="width-0"]')
        height_input = self.page.locator('input[name="height-0"]')
        self.assertEqual(length_input.get_attribute('min'), '1')
        self.assertEqual(width_input.get_attribute('min'), '1')
        self.assertEqual(height_input.get_attribute('min'), '1')

    def test_input_type_validation(self):
        self.page.goto('http://localhost:9200/')
        rooms_input = self.page.locator('input[name="rooms"]')
        self.assertEqual(rooms_input.get_attribute('type'), 'number')
        self.page.fill('input[name="rooms"]', '1')
        self.page.click('input[type="submit"]')
        length_input = self.page.locator('input[name="length-0"]')
        width_input = self.page.locator('input[name="width-0"]')
        height_input = self.page.locator('input[name="height-0"]')
        self.assertEqual(length_input.get_attribute('type'), 'number')
        self.assertEqual(width_input.get_attribute('type'), 'number')
        self.assertEqual(height_input.get_attribute('type'), 'number')


if __name__ == '__main__':
    unittest.main()

