# Test Coverage Documentation

## Overview

This document describes the comprehensive test coverage for the Paint Calculator application, including both unit tests and end-to-end (E2E) tests.

## Test Summary

- **Total Tests:** 60
- **Unit Tests:** 41
- **E2E Tests:** 19
- **Pass Rate:** 100%

## Unit Tests (41 tests)

### TestCalculateFeet (8 tests)
Tests the calculation of square footage for painting.

- `test_calculate_feet_standard` - Standard dimension calculation
- `test_calculate_feet_different_dimensions` - Various dimension combinations
- `test_calculate_feet_minimum_values` - Minimum values (1x1x1)
- `test_calculate_feet_large_values` - Large dimension values
- `test_calculate_feet_zero_length` - Zero length edge case
- `test_calculate_feet_zero_width` - Zero width edge case
- `test_calculate_feet_zero_height` - Zero height edge case
- `test_calculate_feet_float_values` - Float string handling

### TestCalculateGallonsRequired (8 tests)
Tests gallon calculation based on square footage.

- `test_calculate_gallons_required_standard` - Standard gallon calculation
- `test_calculate_gallons_required_rounds_down` - Rounding down behavior
- `test_calculate_gallons_required_exact_multiple` - Exact multiples of 350
- `test_calculate_gallons_required_exact_350` - Exactly 350 square feet
- `test_calculate_gallons_required_less_than_350` - Less than one gallon needed
- `test_calculate_gallons_required_zero` - Zero square feet
- `test_calculate_gallons_required_large_value` - Large square footage
- `test_calculate_gallons_required_one_foot` - Single square foot

### TestSanitizeInput (10 tests)
Tests input sanitization for negative numbers and type conversion.

- `test_sanitize_input_positive` - Positive integer
- `test_sanitize_input_negative` - Negative integer converted to positive
- `test_sanitize_input_string` - String to integer conversion
- `test_sanitize_input_negative_string` - Negative string conversion
- `test_sanitize_input_zero` - Zero value
- `test_sanitize_input_zero_string` - Zero as string
- `test_sanitize_input_float` - Float to integer
- `test_sanitize_input_negative_float` - Negative float conversion
- `test_sanitize_input_float_string` - Float string conversion
- `test_sanitize_input_large_number` - Large number handling

### TestAPIEndpoint (6 tests)
Tests the REST API endpoint functionality.

- `test_calculate_endpoint_single_room` - Single room calculation via API
- `test_calculate_endpoint_multiple_rooms` - Multiple rooms calculation
- `test_calculate_endpoint_many_rooms` - Five rooms calculation
- `test_calculate_endpoint_zero_dimensions` - Zero dimensions edge case
- `test_calculate_endpoint_small_room` - Small room (less than 1 gallon)
- `test_calculate_endpoint_large_room` - Very large room

### TestFlaskRoutes (9 tests)
Tests Flask application routes and responses.

- `test_index_route` - Homepage loads correctly
- `test_dimensions_route_single_room` - Dimensions page for one room
- `test_dimensions_route_multiple_rooms` - Dimensions page for multiple rooms
- `test_dimensions_route_negative_rooms` - Negative room count handling
- `test_dimensions_route_zero_rooms` - Zero rooms edge case
- `test_dimensions_route_large_number` - Large number of rooms
- `test_results_route_single_room` - Results for single room
- `test_results_route_multiple_rooms` - Results for multiple rooms
- `test_results_route_many_rooms` - Results for 10 rooms

## E2E Tests (19 tests)

### TestE2EBasicFlow (5 tests)
Tests complete user workflows through the application.

- `test_full_paint_calculator_flow_two_rooms` - Complete flow for 2 rooms
- `test_single_room_calculation` - Single room end-to-end
- `test_three_rooms_calculation` - Three rooms with data validation
- `test_five_rooms_calculation` - Five rooms workflow
- `test_ten_rooms_calculation` - Ten rooms table generation

### TestE2EEdgeCases (4 tests)
Tests boundary conditions and edge cases.

- `test_minimum_dimensions` - Minimum dimension values (1x1x1)
- `test_large_dimensions` - Very large dimensions (100x100x50)
- `test_mixed_dimension_sizes` - Mix of small, medium, and large rooms
- `test_very_large_number_of_rooms` - 20 rooms edge case

### TestE2EModalInteraction (3 tests)
Tests modal dialog functionality.

- `test_modal_opens_and_closes` - Modal open/close behavior
- `test_modal_displays_results` - Results displayed in modal
- `test_view_results_button_exists` - Button visibility and text

### TestE2EPageElements (4 tests)
Tests page structure and element presence.

- `test_homepage_elements` - Homepage input fields and buttons
- `test_dimensions_page_table_structure` - Dimensions table structure
- `test_dimensions_page_input_fields` - Input field visibility
- `test_results_page_modal_structure` - Modal structure validation

### TestE2EDataValidation (3 tests)
Tests data accuracy and calculation validation.

- `test_small_room_less_than_one_gallon` - Rooms requiring < 1 gallon
- `test_exact_350_square_feet` - Exact coverage boundary
- `test_multiple_rooms_total_calculation` - Total gallon calculation

## Test Scenarios Covered

### Positive Test Cases (Sunny Day)
- Standard room dimensions and calculations
- Multiple rooms with varying sizes
- Valid data entry and form submission
- Correct calculation results
- Modal interactions
- Page navigation

### Negative Test Cases (Rainy Day)
- Zero dimensions
- Negative numbers (auto-corrected to positive)
- Float values (converted to integers)
- Very large numbers
- Edge case boundaries (350 sq ft threshold)

### Edge Cases
- Minimum values (1x1x1)
- Maximum values (100x100x50)
- Zero rooms
- 20+ rooms
- Exact multiples of paint coverage
- Less than one gallon required

### Boundary Value Testing
- Exactly 350 square feet (1 gallon boundary)
- Just under 350 square feet (0 gallons)
- Just over 350 square feet (1 gallon)
- Zero values
- Very large values

## Bug Fixes

During test implementation, the following bug was discovered and fixed:

**Float String Handling Bug**: The `calculate_feet()` and `sanitize_input()` functions could not handle float strings (e.g., "10.5"). Fixed by converting to float first, then to int:
- Changed: `int(value)` 
- To: `int(float(value))`

## Test Execution

All tests are automated and can be run using pytest:

```bash
# Run all tests
python3 -m pytest tests/ -v

# Run only unit tests
python3 -m pytest tests/test_api.py -v

# Run only E2E tests (requires application to be running)
python3 -m pytest tests/test_e2e.py -v
```

## Test Requirements

- pytest 8.3.3
- playwright 1.48.0
- System Chrome browser (for E2E tests)
- Flask application running on localhost:9200 (for E2E tests)

## Coverage Analysis

The test suite provides comprehensive coverage of:
- ✅ All calculation functions
- ✅ All API endpoints
- ✅ All Flask routes
- ✅ Input validation and sanitization
- ✅ Complete user workflows
- ✅ UI element interactions
- ✅ Edge cases and boundaries
- ✅ Error handling
- ✅ Data accuracy validation

