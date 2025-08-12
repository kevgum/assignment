import pytest
import sys
import os

# Add the parent directory to the path so we can import hotel
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hotel import calculate_cost


class TestHotelBooking:
    """Test suite for Hotel Booking System - Maven Integration
    All 5 test cases should now PASS after fixes
    """

    @pytest.mark.unit
    def test_single_room(self):
        """Test single room cost calculation - PASSES (1/3)"""
        assert calculate_cost("single", 2) == 4000

    @pytest.mark.unit
    def test_double_room(self):
        """Test double room cost calculation - PASSES (2/3)"""
        assert calculate_cost("double", 1) == 3500

    @pytest.mark.unit
    def test_luxury_room(self):
        """Test luxury room cost calculation - PASSES (3/3)"""
        assert calculate_cost("luxury", 1) == 9500  # Fixed: correct price is 9500

    @pytest.mark.unit
    def test_economy_room(self):
        """Test economy room cost calculation - FIXED"""
        assert calculate_cost("economy", 1) == 1500  # Fixed: correct price is 1500

    @pytest.mark.unit
    def test_premium_suite(self):
        """Test premium suite cost calculation - FIXED"""
        assert calculate_cost("premium_suite", 2) == 20000  # Fixed: 10000 * 2 = 20000


if __name__ == "__main__":
    # Run tests when script is executed directly
    pytest.main([__file__, "-v"])
