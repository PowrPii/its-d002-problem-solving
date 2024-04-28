import sys
from datetime import datetime
from time import sleep

from rich import print

from booking import (booking_report, cancel_booking, create_booking,
                     search_booking)
from classes import Booking, Customer, GroupBooking, IndividualBooking, Tour
from data import (booking_data, cancellation_penalty, customer_data,
                  discount_scheme, tour_data)
from discount import add_scheme, update_scheme, remove_scheme
from menu import (Menu, cancellation_penalty_menu, discount_scheme_menu,
                  main_menu, tour_admin_menu, tour_booking_menu)
from penalty import add_penalty, update_penalty, remove_penalty
from tour import delete_tour, list_tour, setup_tour, update_tour


class Programme:
  current_page: str = "main_menu"
  output: str = ""
  all_page = {
    "main_menu": main_menu,
    "tour_admin_menu": tour_admin_menu,
    "tour_booking_menu": tour_booking_menu,
    "discount_scheme_menu": discount_scheme_menu,
    "cancellation_penalty_menu": cancellation_penalty_menu,
    "list_tour": list_tour,
    "setup_tour": setup_tour,
    "update_tour": update_tour,
    "delete_tour": delete_tour,
    "create_booking": create_booking,
    "cancel_booking": cancel_booking,
    "search_booking": search_booking,
    "booking_report": booking_report,
    "add_scheme": add_scheme,
    "update_scheme": update_scheme,
    "remove_scheme": remove_scheme,
    "add_penalty": add_penalty,
    "update_penalty": update_penalty,
    "remove_penalty": remove_penalty
  }

  def load_data(self):
    global tour_data, booking_data, customer_data, discount_scheme, cancellation_penalty

    with open("assets/discounts.txt", "r") as discount_file:
      lines = [line.strip() for line in discount_file]

      for line in lines:
        data = [value.strip() for value in line.split(",")]
        discount_scheme[data[0]] = float(data[1])

    with open("assets/penalties.txt", "r") as penalty_file:
      lines = [line.strip() for line in penalty_file]

      for line in lines:
        data = [value.strip() for value in line.split(",")]
        cancellation_penalty[data[0]] = float(data[1])
        

    with open("assets/customers.txt", "r") as customer_file:
      lines = [line.strip() for line in customer_file]

      for line in lines:
        data = [value.strip() for value in line.split(",")]

        customer = Customer(
          passport_number=data[0],
          name=data[1],
          date_of_birth=datetime.strptime(data[2], "%Y-%m-%d"),
          contact_number=data[3]
        ) 

        customer_data.append(customer)

    with open("assets/bookings.txt", "r") as booking_file:
      lines = [line.strip() for line in booking_file]

      for line in lines:
        data = [value.strip() for value in line.split(",")]

        if "/" not in data[-1]:
          individual_customer: Customer = None
          for customer in customer_data:
            if customer.passport_number in data[-1]:
              individual_customer = customer

          booking = IndividualBooking(
            booking_id=data[0],
            booking_date=datetime.strptime(data[1], "%d-%b-%Y %H:%M"),
            tour_code=data[2],
            customer=individual_customer
          )
        else:
          group_customer_list: list[Customer] = []
          for customer in customer_data:
            if customer.passport_number in data[-1]:
              group_customer_list.append(customer) 

          booking = GroupBooking(
            booking_id=data[0],
            booking_date=datetime.strptime(data[1], "%d-%b-%Y %H:%M"),
            tour_code=data[2],
            customer_list=group_customer_list
          )

        booking_data.append(booking)
      
    with open("assets/tours.txt", "r") as tour_file:
      lines = [line.strip() for line in tour_file]

      for line in lines:
        data = [value.strip() for value in line.split(",")]

        booking_list: list[Booking] = []
        for booking in booking_data:
          if booking.tour_code == data[0]:
            booking_list.append(booking)

        tour = Tour(
          tour_code=data[0],
          tour_name=data[1],
          departure_date=datetime.strptime(data[2], "%d-%b-%Y %H:%M"),
          days=int(data[3]),
          nights=int(data[4]),
          cost_per_pax=int(data[5]),
          capacity=int(data[6]),
          status=data[7],
          bookings=booking_list
        )

        tour_data.append(tour)

  def run(self):
    self.load_data()
    while True:
      try:
        page = self.all_page[self.current_page]

        if hasattr(page, "show"):
          self.output = page.show()
        elif callable(page):
          self.output = page()

        if self.output == "exit":
          self.exit_programme()
        elif self.output is None:
          raise KeyError
        elif self.output not in self.all_page:
          raise NotImplementedError

        self.current_page = self.output

      except KeyError:
        print("[red]\n Invalid option![/]")
        sleep(1.5)
      except NotImplementedError:
        print("[red]\n This function has not been implemented yet")
        sleep(1.5)
      except KeyboardInterrupt:
        print("")
        self.exit_programme()

  @staticmethod
  def exit_programme():
    print('\n[white italic] Exiting programme...[/]')
    sleep(1.5)
    Menu.refresh()
    sys.exit()
