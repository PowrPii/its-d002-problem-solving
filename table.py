from classes import Tour, IndividualBooking, GroupBooking, Customer
from rich.table import Table
from datetime import datetime

def generate_tour_table(tour_data: list[Tour]) -> Table:
    table = Table()

    table.add_column("Tour Code", justify="center", style="yellow")
    table.add_column("Tour Name", justify="left", style="cyan")
    table.add_column("Departure Date", justify="center")
    table.add_column("Days", justify="right")
    table.add_column("Nights", justify="right")
    table.add_column("Cost Per Pax", justify="right")
    table.add_column("Capacity", justify="right")
    table.add_column("Seats Booked", justify="right")
    table.add_column("Status", justify="right")

    for tour in tour_data:
        table.add_row(str(tour.tour_code), str(tour.tour_name),
                    tour.departure_date.strftime("%d-%b-%Y %H:%M"),
                    str(tour.days), str(tour.nights), str(tour.cost_per_pax),
                    str(tour.capacity), str(tour.total_seats_booked()), f"[green]{tour.status}[/]" if tour.status == "Open" else f"[red]{tour.status}[/]")

    return table

def generate_open_tour_table(tour_list: list[Tour]) -> Table:
    table = Table()

    table.add_column("Tour Code", justify="center", style="yellow")
    table.add_column("Tour Name", justify="left", style="cyan")
    table.add_column("Departure Date", justify="center")
    table.add_column("Days", justify="right")
    table.add_column("Nights", justify="right")
    table.add_column("Cost Per Pax", justify="right")
    table.add_column("Capacity", justify="right")
    table.add_column("Seats Booked", justify="right")

    for tour in tour_list:
        if tour.status == "Open":
            table.add_row(str(tour.tour_code), str(tour.tour_name),
                        tour.departure_date.strftime("%d-%b-%Y %H:%M"),
                        str(tour.days), str(tour.nights), str(tour.cost_per_pax),
                        str(tour.capacity), str(tour.total_seats_booked()))

    return table

def generate_reportable_tour_table(tour_data) -> Table:
    table = Table()

    table.add_column("Tour Code", justify="center", style="yellow")
    table.add_column("Tour Name", justify="left", style="cyan")
    table.add_column("Departure Date", justify="center")
    table.add_column("Days", justify="right")
    table.add_column("Nights", justify="right")
    table.add_column("Cost Per Pax", justify="right")
    table.add_column("Capacity", justify="right")
    table.add_column("Seats Booked", justify="right")
    
    for tour in tour_data:
        if tour.total_seats_booked() > 0:
            table.add_row(str(tour.tour_code), str(tour.tour_name),
                        tour.departure_date.strftime("%d-%b-%Y %H:%M"),
                        str(tour.days), str(tour.nights), str(tour.cost_per_pax),
                        str(tour.capacity), str(tour.total_seats_booked()))
        
    return table

def generate_report_table(tour: Tour) -> Table:
    table = Table()

    table.add_column("Booking ID", justify="left", style="bright_magenta")
    table.add_column("Passport Number", justify="left", style="cyan")
    table.add_column("Name", justify="left")
    table.add_column("Age", justify="right")
    table.add_column("Contact Number", justify="right")

    for booking in tour.bookings:
        if isinstance(booking, IndividualBooking):
            table.add_row(str(booking.booking_id), str(booking.customer.passport_number),
               str(booking.customer.name), str(booking.customer.get_age()), str(booking.customer.contact_number))
        elif isinstance(booking, GroupBooking):
            for customer in booking.customer_list:
                table.add_row(str(booking.booking_id), str(customer.passport_number),
               str(customer.name), str(customer.get_age()), str(customer.contact_number))
                
    return table

def generate_booking_table(booking_data) -> Table:
    table = Table()

    table.add_column("Booking ID", justify="left", style="cyan")
    table.add_column("Booking Date", justify="left")
    table.add_column("Tour Code", justify="left", style="green")
    table.add_column("Booking Type", justify="right")

    for booking in booking_data:
        booking_type = "Individual Booking" if isinstance(booking, IndividualBooking) else "Group Booking"
        table.add_row(str(booking.booking_id), datetime.strftime(booking.booking_date, "%d-%b-%Y %H:%M"), str(booking.tour_code), booking_type)

    return table

def generate_customer_table(customer_list: list[Customer]) -> Table:
    table = Table()

    table.add_column("Passport Number", justify="left", style="cyan")
    table.add_column("Name", justify="left")
    table.add_column("Age", justify="right")
    table.add_column("Contact Number", justify="right")

    for customer in customer_list:
        table.add_row(str(customer.passport_number), str(customer.name), str(customer.get_age()), str(customer.contact_number))

    return table

def generate_discount_table(discount_scheme: dict[str, float]) -> Table:
    table = Table()

    table.add_column("Number of Customers", justify="center") 
    table.add_column("Discount", justify="right") 

    for number_of_customers, discount in discount_scheme.items(): 
        table.add_row(str(number_of_customers), f"{int(discount * 100)}%")

    return table

def generate_penalty_table(cancellation_penalty: dict[str, float]) -> Table:
    table = Table()

    table.add_column("Number of Days", justify="center") 
    table.add_column("Penalty", justify="right") 

    for number_of_days, penalty in cancellation_penalty.items(): 
        table.add_row(str(number_of_days), f"{int(penalty * 100)}%")

    return table