import heapq
import random
from colorama import Fore, Style, init

init()

# -------- Globals --------
patients = []
beds = 30
icu = 1
oxygen = 20
used_ids = set()

# -------- Severity Color --------
def severity_color(sev):
    if sev == 1: return Fore.GREEN + "GREEN" + Style.RESET_ALL
    elif sev == 2: return Fore.YELLOW + "YELLOW" + Style.RESET_ALL
    elif sev == 3: return Fore.RED + "RED" + Style.RESET_ALL

# -------- Age Factor --------
def age_factor(age):
    if age < 1: return 5
    elif age <= 5: return 4
    elif age <= 10: return 3
    elif age <= 20: return 2
    elif age <= 50: return 1
    else: return 2

# -------- Generate Unique Hex ID --------
def generate_patient_id():
    while True:
        pid = hex(random.randint(0, 0xFFFFFF))[2:].upper()
        if pid not in used_ids:
            used_ids.add(pid)
            return pid

# -------- Priority --------
def priority_score(p):
    return p["severity"]*2 + p["remark"]*3 + age_factor(p["age"])

# -------- Add Patients --------
def add_patient():
    global beds, icu, oxygen

    n = int(input("Number of incoming patients: "))

    for i in range(n):
        if beds <= 0:
            print("No beds available! Remaining patients can't be admitted.")
            break

        print(f"\n--- Enter details for Patient {i+1} ---")

        severity = int(input("Severity (1-Green, 2-Yellow, 3-Red): "))
        age = int(input("Age: "))
        remark = int(input("Remark (1-5): "))

        if severity not in [1,2,3]:
            print("Invalid severity, skipping patient")
            continue

        # 🔴 Critical patients need ICU + Oxygen
        if severity == 3:
            if icu <= 0 or oxygen <= 0:
                print("No ICU/Oxygen available for critical patient!")
                continue
            icu -= 1
            oxygen -= 1

        pid = generate_patient_id()

        p = {"id": pid, "severity": severity, "age": age, "remark": remark}
        p["priority"] = priority_score(p)

        patients.append(p)
        beds -= 1

        print(f"Added ID:{pid} {severity_color(severity)} | Priority:{p['priority']}")

    print("\nRemaining beds:", beds)

# -------- Bed Status --------
def check_beds():
    print("Beds remaining:", beds)

# -------- Resource Check --------
def check_resources():
    print("ICU remaining:", icu)
    print("Oxygen remaining:", oxygen)

# -------- Show Priority --------
def show_patients():
    heap = []
    for p in patients:
        heapq.heappush(heap, (-p["priority"], p["id"], p))

    print("\n--- Priority List ---")
    while heap:
        p = heapq.heappop(heap)[2]
        print(f"ID:{p['id']} {severity_color(p['severity'])} Priority:{p['priority']}")

# -------- Menu --------
while True:
    print("\n1.Add Patient")
    print("2.Check Beds")
    print("3.Resources")
    print("4.Show List")
    print("5.Exit")

    ch = input("Choice: ")

    if ch == '1': add_patient()
    elif ch == '2': check_beds()
    elif ch == '3': check_resources()
    elif ch == '4': show_patients()
    elif ch == '5': break
    else: print("Invalid choice")