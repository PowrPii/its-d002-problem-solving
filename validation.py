from classes import Tour, IndividualBooking, GroupBooking, Customer
from time import sleep
from datetime import datetime
from rich import print

class ValidationError(Exception):
    ...

def tour_code_validation(data: str, *args) -> str:
    avaliable_tour = ["NMT", "SMG", "WMA", "CMA", "LAD", "KAZ", "KYR", "TAJ"]
    
    if data in avaliable_tour:
        return data
    else:
        print("[red]\n The tour code is not recognised.[/]")
    
    sleep(1.5)
    return None

def departure_date_validation(data: str, *args) -> datetime:
    try:
        departure_date = datetime.strptime(data, '%Y-%m-%d %H:%M')

        if departure_date.date() < datetime.now().date():
            raise ValidationError
        else:
            return departure_date

    except ValueError:
        print(f"[red]\n Please enter datetime in this format: YYYY-MM-DD HH:MM[/]")
    except ValidationError:
        print("[red]\n The date should be at least one day from today[/]")
        
    sleep(1.5)
    return None

def days_validation(data: str, *args) -> int:
    try:
        if int(data) < 1:
            raise ValueError

        return int(data)
    except ValueError:
        print("[red]\n Input is not a positive integer[/]")

    sleep(1.5)
    return None

def nights_validation(data: str, days) -> int:
    try:
        if int(data) < 1:
            raise ValueError

        if abs(int(data) - days) > 2:
            raise ValidationError
        
        return int(data)
    except ValueError:
        print("[red]\n Input is not a positive integer[/]")
    except ValidationError:
        print("[red]\n The number of days and nights should not have difference of more than 2.[/]")

    sleep(1.5)
    return None

def cost_per_pax_validation(data: str, *args) -> int:
    try:
        if int(data) < 1:
            raise ValueError
        
        return int(data)
    except ValueError:
        print("[red]\n The cost per pax should a positive integer[/]")

    sleep(1.5)
    return None

def capicity_validation(data: str, comparable_seats_booked=0) -> int:
    try:
        if int(data) < 1:
            raise ValueError
        
        if int(data) < comparable_seats_booked:
            raise ValidationError
        
        return int(data)
    except ValueError:
       print("[red]\n Input should be a positive integer[/]")  
    except ValidationError:
        print("[red]\n The capacity should be more than the old capacity.[/]")

    sleep(1.5)
    return None

def status_validation(data: str, *args) -> str:
    try:
        if data != "Open" and data != "Closed":
            raise ValidationError
        
        return data     
    except ValidationError:
        print("[red]\n The status should either be Open or Closed.[/]")

    sleep(1.5)
    return None

def passport_validation(data: str, selected_tour: Tour, customer_list: list[Customer]):
    if data == "":
            return ""
        
    data = data.lower().replace(" ", "")

    def is_all_numeric():
        return data.isnumeric()
    
    def is_containing_one_leading_character():
        return data[0].isalpha() and data[1:].isnumeric()
    
    def is_containing_two_leading_character():
        return data[0:2].isalpha() and data[2:].isnumeric()
    
    def is_containing_one_leading_character_and_one_trailing_character():
        return data[0].isalpha() and data[1:len(data) - 1].isnumeric() and data[len(data) - 1].isalpha()
    try:
        if len(data) < 8 or len(data) > 9:
            raise ValidationError
        
        if not is_all_numeric() and not is_containing_one_leading_character() and not is_containing_two_leading_character() and not is_containing_one_leading_character_and_one_trailing_character():
            raise ValidationError
        
        for customer in customer_list:
            if customer.passport_number == data:
                print(f"[not bold red]\n The passport number {data.upper()} has already been entered.[/]")
                sleep(1.5)
                return None
            
        for booking in selected_tour.bookings:
            if isinstance(booking, IndividualBooking):
                if booking.customer.passport_number == data:
                    print(f"[not bold red]\n The passport number {data.upper()} has already been used to book this tour.[/]")
                    sleep(1.5)
                    return None
                
            elif isinstance(booking, GroupBooking):
                for customer in booking.customer_list:
                    if customer.passport_number == data:
                        print(f"[not bold red]\n The passport number {data.upper()} has already been used to book this tour.[/]")
                        sleep(1.5)
                        return None
            
        return data.upper()
    except ValidationError:
        print(f"[not bold red]\n The passport number {data.upper()} is not valid.[/]")

    sleep(1.5)
    return None

def name_validation(data: str, *args) -> str:
    try:
        uncceptable_character = "\|%$^&*()_+=!{[]}<>1234567890?\'\",฿"
        for letter in uncceptable_character:
            if letter in data:
                raise ValidationError
            
        return data.title()
    except ValidationError:
        print("[red]\n The name is not valid.[/]")

    sleep(1.5)
    return None

def date_of_birth_validation(data: str, *args) -> datetime:
    try:
        date_of_birth = datetime.strptime(data, '%Y-%m-%d')

        if date_of_birth >= datetime.now():
            raise ValidationError
        
        return date_of_birth
    except ValueError:
        print("[red]\n Date of birth should be in this format: YYYY-MM-DD.[/]")
    except ValidationError:
        print("[red]\n Date of birth should not be today or in the future.[/]")

    sleep(1.5)
    return None

def contact_number_validation(data: str, *args) -> str:
    try:
        if not data.isnumeric() or len(data) != 8:
            raise ValidationError
            
        return data
    except ValidationError:
        print("[red]\n The contact number should be a Singapore number with 8 digits long.[/]")

    sleep(1.5)
    return None

def customer_age_requirement_validation(customer_list: list[Customer]) -> bool:
    has_minor = False
    for customer in customer_list:
        if customer.get_age() < 18:
            has_minor = True

    if not has_minor:
        return True

    for customer in customer_list:
        if customer.get_age() >= 21:
            return True
        
    return False

def number_of_customer_validation(data: str, discount_scheme: dict[str, float], *args) -> int:
    try:
        number_of_customer = int(data)

        if data in discount_scheme:
            raise ValidationError
        
        return number_of_customer 
    except ValueError:
        print("[red]\n The number of customers must be a positive integer.")
    except ValidationError:
        print("[red]\n The number of customers has already existed.")

    sleep(1.5)
    return None

def discount_validation(data: str, discount_scheme: dict[str, float], chosen_number_of_customer: int) -> int:
    try:
        chosen_discount = int(data)

        if chosen_discount < 0 or chosen_discount > 100:
            raise ValueError
        
        irregular = False
        for number_of_customer, discount in discount_scheme.items():
            customer_difference = int(number_of_customer) - chosen_number_of_customer
            discount_difference = int(discount * 100) - chosen_discount
            if (customer_difference > 0 and discount_difference <= 0) or (customer_difference < 0 and discount_difference >= 0):
                irregular = True
                break
            
        if irregular:
            print("[orange1]\n WARNING: Irregular discount found. Please check your input thoroughly before confirming.")
            sleep(1.5)
        
        return chosen_discount
    except ValueError:
        print("[not bold red]\n The discount must be a positive integer between 0 and 100.")
    except ValidationError:
        print("[red]\n The number of customers has already existed.")

    sleep(1.5)
    return None

def days_penalty_validation(data: str, cancellation_penalty: dict[str, float], *args) -> int:
    try:
        number_of_days = int(data)

        if data in cancellation_penalty:
            raise ValidationError
        
        return number_of_days 
    except ValueError:
        print("[red]\n The number of days must be a positive integer.")
    except ValidationError:
        print("[red]\n The number of days has already existed.")

    sleep(1.5)
    return None

def penalty_validation(data: str, cancellation_penalty: dict[str, float], chosen_number_of_days: int) -> int:
    try:
        chosen_penalty = int(data)

        if chosen_penalty < 0 or chosen_penalty > 100:
            raise ValueError
        
        irregular = False
        for number_of_days, penalty in cancellation_penalty.items():
            days_difference = chosen_number_of_days - int(number_of_days)
            penalty_difference = chosen_penalty - int(penalty * 100) 
            if (days_difference > 0 and penalty_difference >= 0) or (days_difference < 0 and penalty_difference <= 0) or (days_difference > 0 and penalty_difference >= 0):
                irregular = True
                break

        if irregular:
            print("[orange1]\n WARNING: Irregular penalty found. Please check your input thoroughly before confirming.")
            sleep(1.5)
        
        return chosen_penalty
    except ValueError:
        print("[not bold red]\n The penalty must be a positive integer between 0 and 100.")
    except ValidationError:
        print("[red]\n The number of days has already existed.")

    sleep(1.5)
    return None
