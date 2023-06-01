import random

# Group Number: 74
# Allocated Tutor Name: Jinx Haung
# Group Members:
# 1. Tan Tao
# 2. Shofi Taneem
# 3. Khanjan Pandya
class Unit:
    # Required variables
    file_path_unit = "data/unit.txt"

    def __init__(self, unit_id: int = 0, unit_code: str = "", unit_name: str = "", unit_capacity: int = 15):
        self.unit_id = unit_id if unit_id != 0 else self.generate_unit_id()
        self.unit_code = unit_code
        self.unit_name = unit_name
        self.unit_capacity = unit_capacity

    def __str__(self):
        return f"{self.unit_id}, {self.unit_code}, {self.unit_name}, {self.unit_capacity}"

    def generate_unit_id(self):
        # Generate a random number between 1000000 and 9999999
        while True:
            unit_id_created = random.randint(1000000, 9999999)
            with open(self.file_path_unit, "r") as file:
                for line in file:
                    if str(unit_id_created) in line:
                        break
                else:
                    return unit_id_created

    def save_unit(self):
        with open(self.file_path_unit, "a") as file:
            file.write(str(self) + "\n")

    def update_unit(self):
        with open(self.file_path_unit, "r") as file:
            lines = file.readlines()
        with open(self.file_path_unit, "w") as file:
            for line in lines:
                if line.strip().split(", ")[0] == str(self.unit_id):
                    file.write(str(self) + "\n")
                else:
                    file.write(line)
