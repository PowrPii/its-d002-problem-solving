from data import discount_scheme, new_discount_data
from rich import print
from rich.prompt import Confirm
from rich.table import Table
from menu import Menu
from table import generate_discount_table
from time import sleep

def get_payable_percentage(total_customer: int):
    for number_of_customer, discount in discount_scheme.items():
        if total_customer >= int(number_of_customer):
            return 1 - discount
    else:
        return 1
    
def save_discount_data():
    with open('assets/discounts.txt', 'w') as file:
        data = ""
        for number_of_customer, discount in discount_scheme.items():
            data += f"{number_of_customer}, {discount}\n"
        
        file.write(data)
    
def add_scheme(is_update=False, chosen_number_of_customer: int=None):
    global discount_scheme

    try:
        while new_discount_data["discount"]["data"] is None:
            Menu.refresh()
            if not is_update:
                print("[bold]\n Add New Scheme\n", generate_discount_table(discount_scheme), "")
            else:
                print("[bold bright_white]\n Update Scheme\n", generate_discount_table(discount_scheme), "")

            if is_update:
                new_discount_data["number_of_customer"]["data"] = chosen_number_of_customer

            for datatype, subdict in new_discount_data.items():
                if subdict["data"] is None:
                    subdict["data"] = subdict["validation"](input(f' {subdict["prompt"]}: '), discount_scheme, new_discount_data["number_of_customer"]["data"])
                else:
                    print(f'[not bold bright_white] {subdict["prompt"]}: {subdict["data"]}')

                if subdict["data"] is None:
                    break
            
        if is_update:
            old_discount_scheme = {
                str(new_discount_data["number_of_customer"]["data"]) : discount_scheme[str(new_discount_data["number_of_customer"]["data"])]
            }

        new_discount_scheme = {
            str(new_discount_data["number_of_customer"]["data"]) : new_discount_data["discount"]["data"] / 100
        }

        Menu.refresh()
        if not is_update:
            print("[bold]\n Add Scheme Confirmation\n[/]", generate_discount_table(new_discount_scheme), "")
        else:
            print("[bold]\n Update Scheme Confirmation\n[/]", "[italic]\n Current Scheme Information[/]", generate_discount_table(old_discount_scheme), "[italic] \n Updated Scheme Information[/]", generate_discount_table(new_discount_scheme))

        confirmation = Confirm.ask("\n Please confirm your choices [magenta][Y/N][/]", show_choices=False)

        if confirmation:
            discount_scheme[str(new_discount_data["number_of_customer"]["data"])] = new_discount_scheme[str(new_discount_data["number_of_customer"]["data"])]
            discount_scheme = {k: discount_scheme[k] for k in sorted(discount_scheme, key=lambda x: int(x), reverse=True)}
            save_discount_data()
            print("[white]\n Successful setup. Redirecting to discount menu...[/]" if not is_update else "[white]\n Sucessful update. Redirecting to discount menu... ")
        else:
            print("[white]\n Negative confirmation received. Redirecting to discount menu... ")

    except KeyboardInterrupt:
        print("[italic white]\n\n Interrupts occured. Redirecting to the discount menu...")

    for subdict in new_discount_data.values():
        subdict["data"] = None

    if not is_update:
        sleep(1.5)
        return "discount_scheme_menu"
    

def update_scheme():
    chosen_number_of_customer = None
    try:
        while chosen_number_of_customer is None:
            Menu.refresh()
            print("[bold bright_white]\n Update Scheme\n", generate_discount_table(discount_scheme))
            chosen_number_of_customer = input("\n Enter Number Of Customer: ")

            if not chosen_number_of_customer in discount_scheme:
                print("[not bold red]\n The chosen data is not in database. Redirecting to the discount menu...")
                sleep(1.5)
                return "discount_scheme_menu"

        add_scheme(is_update=True, chosen_number_of_customer=int(chosen_number_of_customer))
    except KeyboardInterrupt:
        print("[italic white]\n\n Interrupts occured. Redirecting to the discount menu...")

    sleep(1.5)
    return "discount_scheme_menu"

def remove_scheme():
    chosen_number_of_customer = None
    try:
        while chosen_number_of_customer is None:
            Menu.refresh()
            print("[bold bright_white]\n Remove Scheme\n", generate_discount_table(discount_scheme), "")
            chosen_number_of_customer = input("\n Enter Number Of Customer: ")

            if not chosen_number_of_customer in discount_scheme:
                print("[not bold red]\n The chosen data is not in database. Redirecting to the discount menu...")
                sleep(1.5)
                return "discount_scheme_menu"

        chosen_discount_scheme = {
            chosen_number_of_customer : discount_scheme[chosen_number_of_customer]
        }
        
        Menu.refresh() 
        print("[bold bright_white]\n Remove Scheme\n", generate_discount_table(chosen_discount_scheme), "")
        confirmation = Confirm.ask("\n Please confirm your choices [magenta][Y/N][/]", show_choices=False)

        if confirmation:
            del discount_scheme[chosen_number_of_customer]
            save_discount_data()
            print("[white]\n Successful deletion. Redirecting to discount menu...[/]")
        else:
            print("Negative confirmation received. Redirecting to discount menu... ")

        
    except KeyboardInterrupt:
        print("[italic white]\n\n Interrupts occured. Redirecting to the discount menu...")

    sleep(1.5)
    return "discount_scheme_menu"






