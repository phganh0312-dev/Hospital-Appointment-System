def print_divider():
    print("========================================")

def print_header(title):
    print_divider()
    print(title.center(40))
    print_divider()

def get_input(prompt):
    return input(prompt).strip()

def get_int(prompt):
    while True:
        try:
            return int(input(prompt).strip())
        except ValueError:
            print("Loi: Vui long nhap mot so nguyen hop le.")

def get_float(prompt):
    while True:
        try:
            return float(input(prompt).strip())
        except ValueError:
            print("Loi: Vui long nhap so thap phan hop le.")