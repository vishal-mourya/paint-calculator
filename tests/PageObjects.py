from playwright.sync_api import Page, expect
import time


class BasePage:
    
    def __init__(self, page: Page):
        self.page = page
        self.base_url = 'http://localhost:9200'
    
    def navigate_to(self, path: str = '/'):
        self.page.goto(f"{self.base_url}{path}")
    
    def wait_for_load(self, timeout: int = 5000):
        self.page.wait_for_load_state('networkidle', timeout=timeout)


class HomePage(BasePage):
    
    def __init__(self, page: Page):
        super().__init__(page)
        self.rooms_input = page.locator('input[name="rooms"]')
        self.submit_button = page.locator('input[type="submit"]')
    
    def navigate(self):
        self.navigate_to('/')
        self.verify_page_loaded()
    
    def verify_page_loaded(self):
        expect(self.page).to_have_title('Home')
        expect(self.rooms_input).to_be_visible()
        expect(self.submit_button).to_be_visible()
    
    def enter_room_count(self, count: int):
        self.rooms_input.fill(str(count))
    
    def click_submit(self):
        self.submit_button.click()
    
    def submit_room_count(self, count: int):
        self.enter_room_count(count)
        self.click_submit()
    
    def get_rooms_input_attribute(self, attribute: str):
        return self.rooms_input.get_attribute(attribute)


class DimensionsPage(BasePage):
    
    def __init__(self, page: Page):
        super().__init__(page)
        self.dimensions_table = page.locator('table[name="dimensions_table"]')
        self.submit_button = page.locator('input[type="submit"]')
        self.table_headers = page.locator('table[name="dimensions_table"] th')
    
    def verify_page_loaded(self):
        expect(self.page).to_have_title('Dimension Calculation')
        expect(self.dimensions_table).to_be_visible()
    
    def get_length_input(self, room_index: int):
        return self.page.locator(f'input[name="length-{room_index}"]')
    
    def get_width_input(self, room_index: int):
        return self.page.locator(f'input[name="width-{room_index}"]')
    
    def get_height_input(self, room_index: int):
        return self.page.locator(f'input[name="height-{room_index}"]')
    
    def fill_room_dimensions(self, room_index: int, length: int, width: int, height: int):
        self.get_length_input(room_index).fill(str(length))
        self.get_width_input(room_index).fill(str(width))
        self.get_height_input(room_index).fill(str(height))
    
    def fill_all_rooms(self, room_data: list):
        for i, (length, width, height) in enumerate(room_data):
            self.fill_room_dimensions(i, length, width, height)
    
    def fill_all_rooms_same_dimensions(self, num_rooms: int, length: int, width: int, height: int):
        for i in range(num_rooms):
            self.fill_room_dimensions(i, length, width, height)
    
    def click_submit(self):
        self.submit_button.click()
    
    def get_table_row_count(self):
        rows = self.page.locator('table[name="dimensions_table"] tr')
        return rows.count()
    
    def get_table_header_count(self):
        return self.table_headers.count()
    
    def verify_input_attributes(self, room_index: int, expected_type: str = 'number', 
                               expected_min: str = '1', should_be_required: bool = True):
        length_input = self.get_length_input(room_index)
        width_input = self.get_width_input(room_index)
        height_input = self.get_height_input(room_index)
        
        for input_field in [length_input, width_input, height_input]:
            assert input_field.get_attribute('type') == expected_type
            assert input_field.get_attribute('min') == expected_min
            if should_be_required:
                assert input_field.get_attribute('required') is not None


class ResultsPage(BasePage):
    
    def __init__(self, page: Page):
        super().__init__(page)
        self.view_results_button = page.locator('button.btn-success')
        self.modal = page.locator('#resultsModal')
        self.modal_title = page.locator('.modal-title')
        self.total_gallons = page.locator('#sumGallons')
        self.close_button = page.locator('#resultsModal button.close').first
    
    def verify_page_loaded(self):
        expect(self.page).to_have_title('Results!')
        expect(self.view_results_button).to_be_visible()
    
    def verify_view_results_button(self):
        expect(self.view_results_button).to_be_visible()
        expect(self.view_results_button).to_contain_text('View Results')
    
    def click_view_results(self):
        self.view_results_button.click()
    
    def wait_for_modal_visible(self, timeout: int = 10000):
        expect(self.modal).to_be_visible(timeout=timeout)
    
    def open_results_modal(self):
        self.click_view_results()
        self.wait_for_modal_visible()
    
    def verify_modal_content(self):
        expect(self.modal_title).to_contain_text('Paint Calculation Results')
        time.sleep(6)
        expect(self.total_gallons).to_contain_text('Total Gallons Required:')
    
    def close_modal(self):
        self.close_button.click()
        time.sleep(1)
    
    def verify_total_gallons_visible(self):
        expect(self.total_gallons).to_be_visible()


class PaintCalculatorApp:
    
    def __init__(self, page: Page):
        self.page = page
        self.home_page = HomePage(page)
        self.dimensions_page = DimensionsPage(page)
        self.results_page = ResultsPage(page)
    
    def complete_calculation_flow(self, room_data: list, verify_results: bool = True):
        self.home_page.navigate()
        self.home_page.submit_room_count(len(room_data))
        
        self.dimensions_page.verify_page_loaded()
        self.dimensions_page.fill_all_rooms(room_data)
        self.dimensions_page.click_submit()
        
        self.results_page.verify_page_loaded()
        
        if verify_results:
            self.results_page.open_results_modal()
            self.results_page.verify_modal_content()
    
    def complete_calculation_same_dimensions(self, num_rooms: int, length: int = 10, 
                                            width: int = 10, height: int = 8,
                                            verify_results: bool = False):
        self.home_page.navigate()
        self.home_page.submit_room_count(num_rooms)
        
        self.dimensions_page.verify_page_loaded()
        self.dimensions_page.fill_all_rooms_same_dimensions(num_rooms, length, width, height)
        self.dimensions_page.click_submit()
        
        self.results_page.verify_page_loaded()
        
        if verify_results:
            self.results_page.open_results_modal()
