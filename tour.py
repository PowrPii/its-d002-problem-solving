from classes import Tour
from rich.table import Table
from rich import print
from rich.prompt import Confirm
from menu import Menu
from time import sleep
from data import tour_data, avaliable_tour, new_tour_data
from datetime import datetime
from table import generate_tour_table

def save_tour_data():
    with open('assets/tours.txt', 'w') as file:
        data = ""
        for tour in tour_data:
            data += f"{tour.tour_code}, {tour.tour_name}, {datetime.strftime(tour.departure_date, '%d-%b-%Y %H:%M')}, {tour.days}, {tour.nights}, {tour.cost_per_pax}, {tour.capacity}, {tour.status}\n"
        
        file.write(data)
    
def list_tour() -> str:
    try:
        Menu.refresh()
        print("\n[bold] List of Tour\n[/]", generate_tour_table(tour_data), "[white]\n Press Enter to continue...[/]")
        input(" ")
    except KeyboardInterrupt:
        print("[italic white]\n\n Interrupts occured. Redirecting to the menu...")
        sleep(1.5)
    
    return "tour_admin_menu"

def setup_tour(is_update=False, selected_tour: Tour=None) -> str:
    global tour_data, new_tour_data

    if not is_update:
        avaliable_tour_table = Table()
        avaliable_tour_table.add_column("Tour Code", justify="center", style="yellow")
        avaliable_tour_table.add_column("Tour Name", justify="left", style="cyan")

        for tour_code, tour_name in avaliable_tour.items():
            avaliable_tour_table.add_row(tour_code, tour_name)

    try:
        while new_tour_data["status"]["data"] is None:
            Menu.refresh()
            if not is_update:
                print("[bold]\n Setup Tour\n", avaliable_tour_table, "")
            else:
                print(f"[bold bright_white]\n Update Tour: {selected_tour.tour_code}\n", generate_tour_table([selected_tour]), "")

            for datatype, subdict in new_tour_data.items():
                if datatype == "status" and not is_update:
                    subdict["data"] = "Open"
                    break

                if subdict["data"] is None and not is_update:
                    if datatype == "nights":
                        subdict["data"] = subdict["validation"](input(f' {subdict["prompt"]}: '), new_tour_data["days"]["data"])
                    else:
                        subdict["data"] = subdict["validation"](input(f' {subdict["prompt"]}: '))
                elif subdict["data"] is None and is_update:
                    if datatype == "nights":
                        subdict["data"] = subdict["validation"](input(f' {subdict["prompt"]}: '), new_tour_data["days"]["data"])
                    else:
                        subdict["data"] = subdict["validation"](input(f' {subdict["prompt"]}: '), selected_tour.total_seats_booked())
                else:
                    print(f'[not bold bright_white] {subdict["prompt"]}: {subdict["data"]}' if datatype != "departure_date" else f'[not bold bright_white] {subdict["prompt"]}: {datetime.strftime(subdict["data"], "%Y-%m-%d %H:%M")}')

                if subdict["data"] is None:
                    break

        new_tour = Tour(
            tour_code= new_tour_data["tour_code"]["data"][:3] + "-" + datetime.strftime(new_tour_data["departure_date"]["data"], "%y%m%d"),
            tour_name=avaliable_tour[new_tour_data["tour_code"]["data"][:3]],
            departure_date=new_tour_data["departure_date"]["data"],
            days=new_tour_data["days"]["data"],
            nights=new_tour_data["nights"]["data"],
            cost_per_pax=new_tour_data["cost_per_pax"]["data"],
            capacity=new_tour_data["capacity"]["data"],
            status=new_tour_data["status"]["data"]
        )

        Menu.refresh()
        if not is_update:
            print("[bold]\n Setup Tour Confirmation\n[/]", generate_tour_table([new_tour]), "")
        else:
            print("[bold]\n Update Tour Confirmation\n[/]", "[italic]\n Current Tour Information[/]", generate_tour_table([selected_tour]), "[italic] \n Updated Tour Information[/]", generate_tour_table([new_tour]), "")

        confirmation = Confirm.ask("\n Please confirm your choices [magenta][Y/N][/]", show_choices=False)

        if confirmation and is_update:
            tour_data.remove(selected_tour)

        if confirmation:
            tour_data.append(new_tour)
            save_tour_data()
            print("[white]\n Successful setup. Redirecting to tour menu...[/]" if not is_update else "[white]\n Sucessful update. Redirecting to tour menu... ")

        else:
            print("[white]\n Negative confirmation received. Redirecting to tour menu...[/]")

    except KeyboardInterrupt:
        print("[italic white]\n\n Interrupts occured. Redirecting to the tour menu...")

    for subdict in new_tour_data.values():
        subdict["data"] = None

    if not is_update:
        sleep(1.5)
        return "tour_admin_menu"

def update_tour() -> str:
    global tour_data

    try:
        selected_tour = None
        
        while selected_tour is None:
            Menu.refresh()
            print("\n[bold] Update Tour\n[/]")
            print(generate_tour_table(tour_data))

            tour_code = input("\n Enter Tour Code: ")

            for tour in tour_data:
                if tour.tour_code == tour_code:
                    selected_tour = tour
                    break
            else:
                print("[red]\n No tour with the given code found.[/]")
                sleep(1.5)

        new_tour_data["tour_code"]["data"] = selected_tour.tour_code

        if selected_tour.total_seats_booked() > 0:
            new_tour_data["departure_date"]["data"] = selected_tour.departure_date
            new_tour_data["days"]["data"] = selected_tour.days
            new_tour_data["nights"]["data"] = selected_tour.nights
            new_tour_data["cost_per_pax"]["data"] = selected_tour.cost_per_pax

        setup_tour(is_update=True, selected_tour=selected_tour)

    except KeyboardInterrupt:
        print("[italic white]\n\n Interrupts occured. Redirecting to tour menu...")
    
    sleep(1.5) 
    return "tour_admin_menu"

def delete_tour() -> str:
    global tour_data

    try:
        Menu.refresh()
        print("\n[bold] Delete Tour\n[/]")
        print(generate_tour_table(tour_data))
        tour_code = input("\n Enter Tour Code to Delete: ")

        for tour in tour_data:
            if tour_code == tour.tour_code:
                if tour.total_seats_booked() > 0:
                    print("[red]\n Unable to delete as tour has been booked. Redirecting to tour menu...[/]")
                    sleep(1.5)
                    return "tour_admin_menu"
                
                Menu.refresh()
                print("\n[bold] Delete Tour Selection\n[/]")
                print(generate_tour_table([tour]))
                if Confirm.ask("\n Please confirm your choice [magenta][Y/N][/]", show_choices=False):
                    tour_data.remove(tour)
                    save_tour_data()
                    print(f"[italic not bold white]\n Successful deletion of Tour {tour_code}. Redirecting back...[/]")
                else:
                    print(f"[italic not bold white]\n Unsucessful deletion of tour {tour_code}. Redirecting back...[/]")
                break
        else:
            print(f"[red]\n Tour not found in database. Redirecting to tour menu ...")
    except KeyboardInterrupt:
        print("[italic white]\n\n Interrupts occured. Redirecting to tour menu...")

    sleep(1.5)
    return "tour_admin_menu"

