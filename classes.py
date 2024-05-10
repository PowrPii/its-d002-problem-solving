from dataclasses import dataclass, field
from datetime import datetime
from typing import List


@dataclass
class Customer:
  passport_number: str
  name: str
  date_of_birth: datetime
  contact_number: str

  def get_age(self):
    today = datetime.now()
    age = today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
    return age
  
@dataclass
class Booking:
  booking_id: str
  booking_date: datetime
  tour_code: str

  def total_customer(self) -> int:
    ...

@dataclass
class IndividualBooking(Booking):
  customer: Customer

  def total_customer(self) -> int:
    return 1

@dataclass
class GroupBooking(Booking):
  customer_list: List[Customer]

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

  def total_seats_booked(self):
    return sum([booking.total_customer() for booking in self.bookings])
  
  def avaliable_seats(self):
    return self.capacity - self.total_seats_booked()
