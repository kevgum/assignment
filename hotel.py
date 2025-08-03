# hotel.py

def calculate_cost(room_type, days):
    """
    Calculate total cost for a booking based on room type and number of days.
    Feature-X: Added luxury room option with special pricing.
    Feature-Y: Added budget room option and discount functionality.
    Feature-Z: Added premium suite option with enhanced amenities.
    """
    prices = {
        "single": 3000,  # Feature-Z conflict
        "double": 3500,
        "bed_and_breakfast": 4000,
        "with_kitchen": 4500,
        "exclusive": 6000,
        "economy": 1500,
        "luxury": 9500,  # Feature-Z: changed price to cause merge conflict
        "budget": 1000,
        "premium_suite": 10000
    }
    return prices.get(room_type, 0) * days


def print_booking_summary(room_type, days):
    """
    Print a summary of the booking with total cost.
    """
    cost = calculate_cost(room_type, days)
    print(f"You booked a {room_type.replace('_', ' ')} room for {days} day(s). Total: KES {cost}")


def main():
    """
    Main entry point for the application.
    Used by Maven and setuptools entry points.
    """
    import argparse

    parser = argparse.ArgumentParser(description="Hotel Room Booking System")
    parser.add_argument("room_type", choices=["single","double","bed_and_breakfast","with_kitchen","exclusive","economy","luxury","budget","premium_suite"], help="Type of room to book")
    parser.add_argument("days", type=int, help="Number of days to stay")
    args = parser.parse_args()

    print_booking_summary(args.room_type, args.days)


if __name__ == "__main__":
    main()