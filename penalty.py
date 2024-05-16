from rich import print
from rich.prompt import Confirm
from menu import Menu
from table import generate_penalty_table
from time import sleep

def get_penalty_percentage(cancellation_penalty, remaining_days):
    for days, percentage in cancellation_penalty.items():
        if remaining_days >= int(days):
            return percentage
    else:
        return 0
    
def save_penalty_data(cancellation_penalty):
    with open('assets/penalties.txt', 'w') as file:
        data = ""
        for days, penalty in cancellation_penalty.items():
            data += f"{days}, {penalty}\n"
        
        file.write(data)

def add_penalty(tour_data, booking_data, customer_data, discount_scheme, cancellation_penalty, available_tour, new_tour_data, new_customer_data, new_discount_data, new_penalty_data, is_update=False, chosen_number_of_days: int=None):
    try:
        while new_penalty_data["penalty"]["data"] is None:
            Menu.refresh()
            if not is_update:
                print("[bold]\n Add New Penalty\n", generate_penalty_table(cancellation_penalty), "")
            else:
                print("[bold bright_white]\n Update Penalty\n", generate_penalty_table(cancellation_penalty), "")

            if is_update:
                new_penalty_data["days"]["data"] = chosen_number_of_days

            for datatype, subdict in new_penalty_data.items():
                if subdict["data"] is None:
                    subdict["data"] = subdict["validation"](input(f' {subdict["prompt"]}: '), cancellation_penalty, new_penalty_data["days"]["data"])
                else:
                    print(f'[not bold bright_white] {subdict["prompt"]}: {subdict["data"]}')

                if subdict["data"] is None:
                    break
            
        if is_update:
            old_penalty_scheme = {
                str(new_penalty_data["days"]["data"]) : cancellation_penalty[str(new_penalty_data["days"]["data"])]
            }

        new_penalty_scheme = {
            str(new_penalty_data["days"]["data"]) : new_penalty_data["penalty"]["data"] / 100
        }

        Menu.refresh()
        if not is_update:
            print("[bold]\n Add Penalty Confirmation\n[/]", generate_penalty_table(new_penalty_scheme), "")
        else:
            print("[bold]\n Update Penalty Confirmation\n[/]", "[italic]\n Current Penalty Information[/]", generate_penalty_table(old_penalty_scheme), "[italic]\n Updated Penalty Information[/]", generate_penalty_table(new_penalty_scheme))

        confirmation = Confirm.ask("\n Please confirm your choices [magenta][Y/N][/]", show_choices=False)

        if confirmation:
            cancellation_penalty[str(new_penalty_data["days"]["data"])] = new_penalty_scheme[str(new_penalty_data["days"]["data"])]
            cancellation_penalty = {k: cancellation_penalty[k] for k in sorted(cancellation_penalty, key=lambda x: int(x), reverse=True)}
            save_penalty_data(cancellation_penalty)
            print("[white]\n Successful setup. Redirecting to discount menu...[/]" if not is_update else "[white]\n Sucessful update. Redirecting to discount menu... ")
        else:
            print("[white]\n Negative confirmation received. Redirecting to discount menu... ")

    except KeyboardInterrupt:
        print("[italic white]\n\n Interrupts occured. Redirecting to the discount menu...")

    for subdict in new_penalty_data.values():
        subdict["data"] = None

    if not is_update:
        sleep(1.5)
        return "cancellation_penalty_menu"

def update_penalty(tour_data, booking_data, customer_data, discount_scheme, cancellation_penalty, available_tour, new_tour_data, new_customer_data, new_discount_data, new_penalty_data):
    chosen_number_of_days = None
    try:
        while chosen_number_of_days is None:
            Menu.refresh()
            print("[bold bright_white]\n Update Penalty\n", generate_penalty_table(cancellation_penalty))
            chosen_number_of_days = input("\n Enter Number Of Days: ")

            if not chosen_number_of_days in cancellation_penalty:
                print("[not bold red]\n The chosen data is not in database. Redirecting to the discount menu...")
                sleep(1.5)
                return "cancellation_penalty_menu"

        add_penalty(tour_data, booking_data, customer_data, discount_scheme, cancellation_penalty, available_tour, new_tour_data, new_customer_data, new_discount_data, new_penalty_data, is_update=True, chosen_number_of_days=int(chosen_number_of_days))
    except KeyboardInterrupt:
        print("[italic white]\n\n Interrupts occured. Redirecting to the discount menu...")

    sleep(1.5)
    return "cancellation_penalty_menu"

def remove_penalty(tour_data, booking_data, customer_data, discount_scheme, cancellation_penalty, available_tour, new_tour_data, new_customer_data, new_discount_data, new_penalty_data):
    chosen_number_of_days = None
    try:
        while chosen_number_of_days is None:
            Menu.refresh()
            print("[bold bright_white]\n Remove Penalty\n", generate_penalty_table(cancellation_penalty), "")
            chosen_number_of_days = input("\n Enter Number Of Days: ")

            if not chosen_number_of_days in cancellation_penalty:
                print("[not bold red]\n The chosen data is not in database. Redirecting to the discount menu...")
                sleep(1.5)
                return "cancellation_penalty_menu"

        chosen_penalty_scheme = {
            chosen_number_of_days : cancellation_penalty[chosen_number_of_days]
        }
        
        Menu.refresh() 
        print("[bold bright_white]\n Remove Penalty\n", generate_penalty_table(chosen_penalty_scheme), "")
        confirmation = Confirm.ask("\n Please confirm your choices [magenta][Y/N][/]", show_choices=False)

        if confirmation:
            del cancellation_penalty[chosen_number_of_days]
            save_penalty_data(cancellation_penalty)
            print("[white]\n Successful deletion. Redirecting to discount menu...[/]")
        else:
            print("Negative confirmation received. Redirecting to discount menu... ")

        
    except KeyboardInterrupt:
        print("[italic white]\n\n Interrupts occured. Redirecting to the discount menu...")

    sleep(1.5)
    return "cancellation_penalty_menu"





