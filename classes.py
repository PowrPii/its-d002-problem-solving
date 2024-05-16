from dataclasses import dataclass, field
from datetime import datetime
from typing import List


class Customer:
  passport_number: str
  name: str
  date_of_birth: datetime
  contact_number: str

  def __init__(self, passport_number, name, date_of_birth, contact_number):
    self.passport_number = passport_number
    self.name = name
    self.date_of_birth = date_of_birth
    self.contact_number = contact_number

  def get_age(self):
    today = datetime.now()
    age = today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
    return age
  
class Booking:
  booking_id: str
  booking_date: datetime
  tour_code: str

  def __init__(self, booking_id, booking_date, tour_code):
    self.booking_id = booking_id
    self.booking_date = booking_date
    self.tour_code = tour_code

  def total_customer(self) -> int:
    ...

class IndividualBooking(Booking):
  customer: Customer

  def __init__(self, booking_id, booking_date, tour_code, customer):
    self.booking_id = booking_id
    self.booking_date = booking_date
    self.tour_code = tour_code
    self.customer = customer

  def total_customer(self) -> int:
    return 1

class GroupBooking(Booking):
  customer_list: List[Customer]

  def __init__(self, booking_id, booking_date, tour_code, customer_list):
    self.booking_id = booking_id
    self.booking_date = booking_date
    self.tour_code = tour_code
    self.customer = customer_list

  def total_customer(self) -> int:
    return len(self.customer_list)


@dataclass
class Tour:
  tour_code: str
  tour_name: str
  departure_date: datetime
  days: int
  nights: int
  cost_per_pax: int
  capacity: int
  status: str
  bookings: List[Booking] = field(default_factory=list[Booking])

  def __init__(self, tour_code, tour_name, departure_date, days, nights, cost_per_pax, capacity, status, bookings=[]):
    self.tour_code = tour_code
    self.tour_name = tour_name
    self.departure_date = departure_date
    self.days = days
    self.nights = nights
    self.cost_per_pax = cost_per_pax
    self.capacity = capacity
    self.status = status
    self.bookings = bookings 

  def total_seats_booked(self):
    return sum([booking.total_customer() for booking in self.bookings])
  
  def avaliable_seats(self):
    return self.capacity - self.total_seats_booked()
