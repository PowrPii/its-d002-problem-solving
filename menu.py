import os

from rich import print


class Menu:
  header: str
  options: dict
  input: str

  def __init__(self, header: str, options: dict):
    self.header = header
    self.options = options

  @staticmethod
  def refresh():
    os.system('cls' if os.name == 'nt' else 'clear')

  def render(self):
    print(f'\n [bold]{self.header}[/]\n')
    for choice, decription in self.options.items():
      print(f'   [bright_cyan]{choice}.[/] {decription["name"]}')

  def get_input(self):
    self.input = input("\n Enter option: ")

  def validate_input(self):
    return self.options[self.input]["direct"] if self.input in self.options else None

  def show(self):
    self.refresh()
    self.render()
    self.get_input()

    return self.validate_input()


main_menu = Menu(
    header="BESG Main Menu",
    options={
        "1": {
            "name": "Tour Admin",
            "direct": "tour_admin_menu"
        },
        "2": {
            "name": "Tour Booking",
            "direct": "tour_booking_menu"
        },
        "3": {
        "name": "Discount Schemes Setup",
        "direct": "discount_scheme_menu"
        },
        "4": {
        "name": "Cancellation Penalties Setup",
        "direct": "cancellation_penalty_menu"
        },
        "0": {
            "name": "Exit",
            "direct": "exit"
        }
})

tour_admin_menu = Menu(
    header="Tour Admin Menu",
    options={
        "a": {
            "name": "List Tour",
            "direct": "list_tour"
        },
        "b": {
            "name": "Setup Tour",
            "direct": "setup_tour"
        },
        "c": {
            "name": "Update Tour",
            "direct": "update_tour"
        },
        "d": {
            "name": "Delete Tour",
            "direct": "delete_tour"
        },
        "m": {
            "name": "Back to Main Menu",
            "direct": "main_menu"
        }
    })

tour_booking_menu = Menu(
    header="Tour Booking Menu",
    options={
        "a": {
            "name": "Create Booking",
            "direct": "create_booking"
        },
        "b": {
            "name": "Cancel Booking",
            "direct": "cancel_booking"
        },
        "c": {
            "name": "Search Booking",
            "direct": "search_booking"
        },
        "d": {
            "name": "Booking Report",
            "direct": "booking_report"
        },
        "m": {
            "name": "Back to Main Menu",
            "direct": "main_menu"
        }
})

discount_scheme_menu = Menu(
    header="Discount Schemes Menu",
    options={
        "a": {
            "name": "Add New Line",
            "direct": "add_scheme"
        },
        "b": {
            "name": "Update Line",
            "direct": "update_scheme"
        },
        "c": {
            "name": "Remove line",
            "direct": "remove_scheme"
        },
        "m": {
            "name": "Back to Main Menu",
            "direct": "main_menu"
        }
})

cancellation_penalty_menu = Menu(
    header="Cancellation Penalties Menu",
    options={
        "a": {
            "name": "Add New Line",
            "direct": "add_penalty"
        },
        "b": {
            "name": "Update Line",
            "direct": "update_penalty"
        },
        "c": {
            "name": "Remove line",
            "direct": "remove_penalty"
        },
        "m": {
            "name": "Back to Main Menu",
            "direct": "main_menu"
        }
})
