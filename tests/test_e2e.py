import unittest
from playwright.sync_api import sync_playwright, expect


class TestE2E(unittest.TestCase):
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

    def test_full_paint_calculator_flow(self):
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

    def test_multiple_rooms_navigation(self):
        self.page.goto('http://localhost:9200/')
        self.page.fill('input[name="rooms"]', '3')
        self.page.click('input[type="submit"]')
        rows = self.page.locator('table[name="dimensions_table"] tr')
        count = rows.count()
        self.assertEqual(count, 4)


if __name__ == '__main__':
    unittest.main()

