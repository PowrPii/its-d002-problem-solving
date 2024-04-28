from datetime import datetime
from time import sleep

from rich import print
from rich.prompt import Confirm

from classes import Booking, Customer, GroupBooking, IndividualBooking, Tour
from data import booking_data, customer_data, new_customer_data, tour_data
from discount import get_payable_percentage
from menu import Menu
from penalty import get_penalty_percentage
from table import (
    generate_booking_id,
    generate_booking_table,
    generate_customer_table,
    generate_open_tour_table,
    generate_report_table,
    generate_reportable_tour_table,
)
from validation import customer_age_requirement_validation


def get_booked_tour() -> list[Tour]:
    booked_tour = []

    for tour in tour_data:
        if tour.total_seats_booked() > 0:
            booked_tour.append(tour)

    return booked_tour

def get_cost(tour_code, number_of_customer):
    chosen_tour: Tour = None
    for tour in tour_data:
        if tour.tour_code == tour_code:
            chosen_tour = tour
    
    return number_of_customer * chosen_tour.cost_per_pax * get_payable_percentage(number_of_customer)


def update_booking_and_customer_data():
    with open('assets/bookings.txt', 'w') as file:
        data = ""
        for booking in booking_data:
            if isinstance(booking, IndividualBooking):
                data += f"{booking.booking_id}, {datetime.strftime(booking.booking_date, '%d-%b-%Y %H:%M')}, {booking.tour_code}, {booking.customer.passport_number}\n"
                   
                
            elif isinstance(booking, GroupBooking):
                passport_numbers = ""
                for customer in booking.customer_list:
                    passport_numbers += f'{customer.passport_number}/'

                data += f"{booking.booking_id}, {datetime.strftime(booking.booking_date, '%d-%b-%Y %H:%M')}, {booking.tour_code}, {passport_numbers[:-1]}\n"
            
        file.write(data)

    with open('assets/customers.txt', 'w') as file:
        data = ""

        for customer in customer_data:
            data += f"{customer.passport_number}, {customer.name}, {datetime.strftime(customer.date_of_birth, '%Y-%m-%d')}, {customer.contact_number}\n"

        file.write(data)

def create_booking() -> str:
    global new_customer_data

    try:
        customers_list: list[Customer] = []
        selected_tour: Tour = None

        while selected_tour is None:
            Menu.refresh()
            print("\n[bold] List of Open Tour\n[/]", generate_open_tour_table(tour_data))

            tour_code = input("\n Enter Tour Code: ")

            for tour in tour_data:
                if tour.tour_code == tour_code and tour.status == "Open":
                    selected_tour = tour
                    break
                if tour.tour_code == tour_code and tour.status == "Closed":
                    print("[red]\n The chosen tour is closed for booking. Redirecting to booking menu...[/]")
                    sleep(1.5)
                    return "tour_booking_menu"
            else:
                print("[red]\n No Tour found in the database. Redirecting to booking menu...[/]")
                sleep(1.5)
                return "tour_booking_menu"
            
        for subdict in new_customer_data.values():
            subdict["data"] = None
                
        while new_customer_data["contact_number"]["data"] is None: 
            Menu.refresh()
            print(f"[bold bright_white]\n {selected_tour.tour_name} ({selected_tour.tour_code}) Booking")
            print(f"\n[not bold bright_white] Duration: {selected_tour.days} Days {selected_tour.nights} Nights")
            print(f"[not bold bright_white] Departs on {datetime.strftime(selected_tour.departure_date, '%d %B %Y, %H:%M')}")
            print(f"[not bold bright_white] ${selected_tour.cost_per_pax:.2f} per pax")
            print(f"[not bold bright_white] Capicity: {selected_tour.capacity} Avaliable seats: {selected_tour.avaliable_seats()}\n")
            if len(customers_list) > 0:
                print(generate_customer_table(customers_list) ,"")

            for datatype, subdict in new_customer_data.items():
                if subdict["data"] is None:
                    subdict["data"] = subdict["validation"](input(f' {subdict["prompt"]}: '), selected_tour, customers_list)
                else:
                    print(f'[not bold bright_white] {subdict["prompt"]}: {subdict["data"]}' if datatype != "date_of_birth" else f'[not bold bright_white] {subdict["prompt"]}: {datetime.strftime(subdict["data"], "%Y-%m-%d")}')

                if datatype == "passport_number" and subdict["data"] == "":
                    break

                if subdict["data"] is None:
                    break

                for customer in customer_data:
                    if customer.passport_number == new_customer_data["passport_number"]["data"]:
                        new_customer_data["name"]["data"] = customer.name
                        new_customer_data["date_of_birth"]["data"] = customer.date_of_birth
                        new_customer_data["contact_number"]["data"] = customer.contact_number

            if new_customer_data["passport_number"]["data"] == "":
                break

            if new_customer_data["contact_number"]["data"] is not None:
                customers_list.append(Customer(
                    passport_number=new_customer_data["passport_number"]["data"],
                    name=new_customer_data["name"]["data"],
                    date_of_birth=new_customer_data["date_of_birth"]["data"],
                    contact_number=new_customer_data["contact_number"]["data"]
                ))

                for subdict in new_customer_data.values():
                    subdict["data"] = None
        
        if len(customers_list) == 0:
            print("[white]\n No customer entered. Redirecting to booking menu...")
            sleep(1.5)
            return "tour_booking_menu"
        
        if not customer_age_requirement_validation(customers_list):
            print('[not bold red]\n Customer(s) aged 18 or lower must be accompanied by at least one adult ages 21 or older.\n Redirecting to booking menu...')
            sleep(1.5)
            return "tour_booking_menu"

        Menu.refresh()
        print(f"[bold bright_white]\n {selected_tour.tour_name} ({selected_tour.tour_code}) Booking Confirmation[/]")
        print(f"[not bold bright_white]\n Booking ID: {generate_booking_id()}")
        print(f"[not bold bright_white] Duration: {selected_tour.days} Days {selected_tour.nights} Nights")
        print(f"[not bold bright_white] Departs on {datetime.strftime(selected_tour.departure_date, '%d %B %Y, %H:%M')}")
        print(f"[not bold bright_white] Total Seats: {len(customers_list)}, Total Cost: ${get_cost(selected_tour.tour_code, len(customers_list)):.2f}")
        print(f"[not bold bright_white] Capicity: {selected_tour.capacity}, Avaliable seats: {selected_tour.avaliable_seats()}\n")
        print(generate_customer_table(customers_list))

        confirmation = Confirm.ask("\n Please confirm your choices [magenta][Y/N][/]", 
                                   show_choices=False)

        if confirmation:
            for current_customer in customers_list:
                for customer in customer_data:
                    if current_customer.passport_number == customer.passport_number:
                        break
                else:
                    customer_data.append(current_customer)

            if len(customer_data) == 1:
                booking = IndividualBooking(
                    booking_id=generate_booking_id(),
                    booking_date=datetime.now(),
                    tour_code=selected_tour.tour_code,
                    customer=customers_list[0]
                )
            else:
                booking = GroupBooking(
                    booking_id=generate_booking_id(),
                    booking_date=datetime.now(),
                    tour_code=selected_tour.tour_code,
                    customer_list=customers_list
                )

            booking_data.append(booking)
            selected_tour.bookings.append(booking)

            update_booking_and_customer_data()

            print("[white]\n Successful booking. Redirecting to booking menu...[/]")
        else:
            print("[white]\n Negative confirmation received. Redirecting to booking menu... ")

    except KeyboardInterrupt:
        print("[white]\n\n Interrupts occured. Redirecting to booking menu...")

    sleep(1.5)
    return "tour_booking_menu"

def cancel_booking():
    try:
        Menu.refresh()
        print("[bold]\n Cancel Booking\n")

        if len(booking_data) == 0:
            print("[white] No booking at the moment. Rediecting to booking menu...")
            sleep(1.5)
            return "tour_booking_menu"
        else:
            print(generate_booking_table())

        booking_id = input("\n Enter Booking ID: ")

        selected_booking: Booking = None
        selected_tour: Tour = None
        for booking in booking_data:
            if booking.booking_id == booking_id:
                print(booking.booking_id)
                selected_booking = booking
                break
        else:
            print("[not bold red]\n No booking found in database, Redirecting to booking menu...")
            sleep(1.5)
            return "tour_booking_menu"
        
        for tour in tour_data:
            if selected_booking.tour_code == tour.tour_code:
                selected_tour = tour
                break
        else:
            print("[not bold red]\n No tour found in database, Redirecting to booking menu...")
            sleep(1.5)
            return "tour_booking_menu"
        
        if tour.departure_date < datetime.now():
            print("[not bold red]\n Booking cannot be cancelled as the the tour has already departed.\n Redirecting to booking menu...")
            sleep(1.5)
            return "tour_booking_menu"
        
        Menu.refresh()
        print(f"[bold bright_white]\n {selected_tour.tour_name} ({selected_tour.tour_code}) Cancellation Confirmation[/]")
        print(f"\n[not bold bright_white] Booking ID: {selected_booking.booking_id}[/]")
        print(f"[not bold bright_white] Duration: {selected_tour.days} Days {selected_tour.nights} Nights")
        print(f"[not bold bright_white] Departs on {datetime.strftime(selected_tour.departure_date, '%d %B %Y, %H:%M')}")
        print(f"[not bold bright_white] Total Seats: {selected_booking.total_customer()}, Total Cost: ${get_cost(selected_tour.tour_code, selected_booking.total_customer()):.2f}\n")
        if isinstance(selected_booking, IndividualBooking):
            print(generate_customer_table([selected_booking.customer]))
        elif isinstance(selected_booking, GroupBooking):
            print(generate_customer_table(selected_booking.customer_list))

        
        
        remaining_days = selected_tour.departure_date.date() - selected_booking.booking_date.date()
        if selected_booking.booking_date.date() == datetime.now().date():
            print(" \n There will be no cancallation penalty.")
        else:
            cancellation_penalty_amount = get_cost(selected_tour.tour_code, selected_booking.total_customer()) * get_penalty_percentage(remaining_days.days)
            print(f"[not bold orange1] \n There will be a cancallation penalty of ${cancellation_penalty_amount:.2f}.")
        
        confirmation = Confirm.ask("\n Please confirm your choices [magenta][Y/N][/]", show_choices=False)

        if confirmation:
            booking_data.remove(booking)
            selected_tour.bookings.remove(booking)

            update_booking_and_customer_data()

            print("[white]\n Successful cancallation. Redirecting to booking menu...[/]")
        else:
            print("[white]\n Negative confirmation received. Redirecting to booking menu... ")
    except KeyboardInterrupt:
        print("[white]\n\n Interrupts occured. Redirecting to booking menu...")

    sleep(1.5)
    return "tour_booking_menu"


def search_booking():
    try:
        Menu.refresh()
        print("[bold]\n Search Booking\n")

        if len(booking_data) == 0:
            print("[white] No booking at the moment. Rediecting to booking menu...")
            sleep(1.5)
            return "tour_booking_menu"
        else:
            print(generate_booking_table())

        booking_id = input("\n Enter Booking ID: ")

        selected_booking: Booking = None
        for booking in booking_data:
            if booking.booking_id == booking_id:
                print(booking.booking_id)
                selected_booking = booking
                break
        else:
            print("[not bold red]\n No booking found in database, Redirecting to booking menu...")
            sleep(1.5)
            return "tour_booking_menu"
            
        for tour in tour_data:
            if selected_booking.tour_code == tour.tour_code:
                selected_tour = tour
                break
        else:
            print("[not bold red]\n No tour found in database, Redirecting to booking menu...")
            sleep(1.5)
            return "tour_booking_menu"

        Menu.refresh()
        print(f"[bold bright_white]\n {selected_tour.tour_name} ({selected_tour.tour_code}) Booking")
        print(f"\n[not bold bright_white] Booking ID: {selected_booking.booking_id}[/]")
        print(f"[not bold bright_white] Duration: {selected_tour.days} Days {selected_tour.nights} Nights")
        print(f"[not bold bright_white] Departs on {datetime.strftime(selected_tour.departure_date, '%d %B %Y, %H:%M')}")
        print(f"[not bold bright_white] Total Seats: {selected_booking.total_customer()}, Total Cost: ${get_cost(selected_tour.tour_code, selected_booking.total_customer()):.2f}")
        print(f"[not bold bright_white] Capicity: {selected_tour.capacity}, Avaliable seats: {selected_tour.avaliable_seats()}\n")
        if isinstance(selected_booking, IndividualBooking):
            print(generate_customer_table([selected_booking.customer]))
        elif isinstance(selected_booking, GroupBooking):
            print(generate_customer_table(selected_booking.customer_list))
        print("[not bold white]\n Press Enter the Continue...")
        input(" ")
    except KeyboardInterrupt:
        print("[white]\n\n Interrupts occured. Redirecting to booking menu...")

    sleep(1.5)
    return "tour_booking_menu"

def booking_report():
    try:
        Menu.refresh()
        print("[bold]\n Booking Report\n")
        print(generate_reportable_tour_table(), "[italic] Only Tours with bookings can generate thier report")
        tour_code = input("\n Enter Tour Code: ")
        tours = tour_code.split(",")

        chosen_tours: list[Tour] = []
        for tour in tours:
            for avaliable_tour in tour_data:
                if avaliable_tour.tour_code == tour.strip():
                    chosen_tours.append(avaliable_tour)
                    break
            else:
                print(f"[not bold red]\n Tour Code {tour} does not exist. Make sure all tours code are valid.\n Redirecting to booking menu...")
                sleep(1.5)
                return "tour_booking_menu"

        ungeneratable_tours: list[Tour] = []
        generatable_tours: list[Tour] = []
        for chosen_tour in chosen_tours:
            for tour in get_booked_tour():
                if chosen_tour.tour_code == tour.tour_code:
                    generatable_tours.append(tour)
                    break
            else:
                ungeneratable_tours.append(tour)
        
        if len(ungeneratable_tours) != 0:
            for tour in ungeneratable_tours:
                print(f"[not bold orange1]\n Tour Code {tour.tour_code}'s report cannot be generated as there is no booking for this tour.")
            sleep(1.5)

        if len(generatable_tours) == 0:
            print("[red]\n No generatable tours. Redirecting to booking menu...")
            sleep(1.5)
            return "tour_booking_menu"

        Menu.refresh()
        print("[bold bright_white]\n Booking Report")
        for tour in generatable_tours:
            print(f"[bold italic bright_white]\n {tour.tour_name} ({tour.tour_code})")
            print(f"\n[not bold bright_white] Duration: {tour.days} Days {tour.nights} Nights")
            print(f"[not bold bright_white] Departs on {datetime.strftime(tour.departure_date, '%d %B %Y, %H:%M')}")
            print(f"[not bold bright_white] ${tour.cost_per_pax:.2f} per pax")
            print(f"[not bold bright_white] Capicity: {tour.capacity} Avaliable seats: {tour.avaliable_seats()}\n")
            print(generate_report_table(tour))
        print("[not bold white]\n Press Enter the Continue...")
        input(" ")
        
    except KeyboardInterrupt:
        print("[white]\n\n Interrupts occured. Redirecting to booking menu...")

    sleep(1.5)
    return "tour_booking_menu"

        
