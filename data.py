from classes import Booking, Customer, Tour
from validation import (capicity_validation, contact_number_validation,
                        cost_per_pax_validation, date_of_birth_validation,
                        days_penalty_validation, days_validation,
                        departure_date_validation, discount_validation,
                        name_validation, nights_validation,
                        number_of_customer_validation, passport_validation,
                        penalty_validation, status_validation,
                        tour_code_validation)

tour_data: list[Tour] = []
booking_data: list[Booking] = []
customer_data: list[Customer] = []
discount_scheme: dict[str, float] = {}
cancellation_penalty: dict[str, float] = {}

avaliable_tour = {
    "NMT": "North Mongolia Taiga",
    "SMG": "South Mongolia Gobi",
    "WMA": "West Mongolia Altai",
    "CMA": "Central Mongolia",
    "LAD": "Ladakh India",
    "KAZ": "Kazakhstan",
    "KYR": "Kyrgyzstan",
    "TAJ": "Tajikistan"
}

new_tour_data = {
    "tour_code" : {
        "prompt": "Enter Tour Code",
        "data": None,
        "validation": tour_code_validation
    }, 
    "departure_date" : {
        "prompt": "Enter Departure Date (YYYY-MM-DD HH:MM)",
        "data": None,
        "validation": departure_date_validation
    }, 
    "days": {
        "prompt": "Enter No. of Days",
        "data": None,
        "validation": days_validation
    },
    "nights": {
        "prompt": "Enter No. of Nights",
        "data": None,
        "validation": nights_validation
    }, 
    "cost_per_pax": {
        "prompt": "Enter Cost Per Pax",
        "data": None,
        "validation": cost_per_pax_validation
    }, 
    "capacity": {
        "prompt": "Enter Capacity",
        "data": None,
        "validation": capicity_validation
    },
    "status": {
        "prompt": "Enter Status",
        "data": None,
        "validation": status_validation
    }
}

new_customer_data = {
    "passport_number" : {
        "prompt": "Enter Passport Number",
        "data": None,
        "validation": passport_validation
    },
    "name" : {
        "prompt": "Enter Name",
        "data": None,
        "validation": name_validation
    },
    "date_of_birth" : {
        "prompt": "Enter Date Of Birth (YYYY-MM-DD)",
        "data": None,
        "validation": date_of_birth_validation
    },
    "contact_number" : {
        "prompt": "Enter Contact Number",
        "data": None,
        "validation": contact_number_validation
    }
}

new_discount_data = {
    "number_of_customer" : {
        "prompt": "Enter Number of Customer",
        "data": None,
        "validation": number_of_customer_validation
    },
    "discount" : {
        "prompt": "Enter Discount (%)",
        "data": None,
        "validation": discount_validation
    }
}

new_penalty_data = {
    "days" : {
        "prompt": "Enter Number of Days",
        "data": None,
        "validation": days_penalty_validation
    },
    "penalty" : {
        "prompt": "Enter Penalty (%)",
        "data": None,
        "validation": penalty_validation
    }
}