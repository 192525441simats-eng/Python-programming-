"""
ASSIGNMENT 3 – Python Solutions Q1 to Q7
Topics: Lists, Tuples, Dictionaries, Sets, Comprehensions, Nested Data,
and Contact Merging.

Run:
    python assignment3.py

The script uses generated/sample data, prints test evidence, and measures
execution times on the computer where it is run. Timings vary by machine.
"""

import copy
import random
import string
import sys
import time
from collections import Counter, defaultdict


# ============================================================
# Q1 – LISTS AND SLICING: DAILY RAINFALL RECORDS
# ============================================================

def moving_average_naive(readings, window=7):
    """Calculate each window by summing its slice."""
    if window <= 0 or len(readings) < window:
        return []
    return [
        sum(readings[i:i + window]) / window
        for i in range(len(readings) - window + 1)
    ]


def moving_average_running(readings, window=7):
    """Calculate moving averages by updating a running total."""
    if window <= 0 or len(readings) < window:
        return []
    current_sum = sum(readings[:window])
    result = [current_sum / window]
    for i in range(window, len(readings)):
        current_sum += readings[i] - readings[i - window]
        result.append(current_sum / window)
    return result


def weekly_totals(readings):
    return [sum(readings[i:i + 7]) for i in range(0, len(readings), 7)]


def time_function(function, *args, repeats=3):
    times = []
    result = None
    for _ in range(repeats):
        start = time.perf_counter()
        result = function(*args)
        times.append(time.perf_counter() - start)
    return result, sum(times) / len(times), times


def q1():
    print("\n" + "=" * 72)
    print("Q1 – LISTS AND SLICING: DAILY RAINFALL RECORDS")
    print("=" * 72)

    random.seed(42)
    readings = [random.randint(0, 30) for _ in range(365)]

    totals = weekly_totals(readings)
    wettest_index = max(range(len(totals)), key=totals.__getitem__)
    driest_index = min(range(len(totals)), key=totals.__getitem__)
    averages = moving_average_running(readings)
    dry_days = [day + 1 for day, value in enumerate(readings) if value == 0]

    print("First 14 rainfall readings:", readings[:14])
    print("First 5 weekly totals:", totals[:5])
    print(f"Wettest week: {wettest_index + 1}, total = {totals[wettest_index]} mm")
    print(f"Driest week: {driest_index + 1}, total = {totals[driest_index]} mm")
    print("First 5 seven-day moving averages:", [round(x, 2) for x in averages[:5]])
    print("Dry-day count:", len(dry_days))
    print("First 15 dry days:", dry_days[:15])

    print("readings[7:14] gives readings at indexes 7 through 13 (7 values).")
    print("readings[-7:] gives the final 7 readings.")
    print("readings[::7] gives every seventh reading, starting at index 0.")
    print("Pseudocode: total = sum(first 7); save average; for each next day,")
    print("add new reading, subtract reading leaving window, save total / 7.")
    print("List costs: append O(1) amortised; insert/pop at front O(n);")
    print("sort O(n log n).")

    print("\nMoving-average experiment (three-run averages):")
    for n in (365, 36_500, 365_000):
        data = [random.randint(0, 30) for _ in range(n)]
        naive_result, naive_time, _ = time_function(moving_average_naive, data)
        fast_result, fast_time, _ = time_function(moving_average_running, data)
        same = len(naive_result) == len(fast_result) and all(
            abs(a - b) < 1e-9 for a, b in zip(naive_result, fast_result)
        )
        additions_naive = max(0, (n - 7 + 1) * 7)
        additions_running = 7 + max(0, n - 7) * 2
        print(f"n={n:,}: same={same}; naive={naive_time:.6f}s; "
              f"running={fast_time:.6f}s")
        print(f"  Approx additions: naive={additions_naive:,}; "
              f"running={additions_running:,}")

    print("Short-list tests:", moving_average_running([], 7),
          moving_average_running([2, 4, 6], 7))
    print("A late reading inserted at its date costs O(n) due to shifting.")
    print("A list remains suitable for a year of readings; for frequent")
    print("late insertions, a date-keyed dictionary or sorted structure may help.")
    print("deque(maxlen=7) supports efficient rolling windows; running sum is O(n)")
    print("time and O(7) window space. Full readings list uses O(n) space.")


# ============================================================
# Q2 – TUPLES, MUTABILITY AND COPYING
# ============================================================

def change_first_row(grid):
    grid[0][0] = 99


def q2():
    print("\n" + "=" * 72)
    print("Q2 – TUPLES, MUTABILITY AND COPYING")
    print("=" * 72)

    rows, cols = 3, 4
    bad = [[0] * cols] * rows
    bad[0][1] = 7
    good = [[0 for _ in range(cols)] for _ in range(rows)]
    good[0][1] = 7
    print("bad :", bad)
    print("good:", good)
    print("bad rows same object:", bad[0] is bad[1])
    print("good rows same object:", good[0] is good[1])

    stops = {
        (13.0827, 80.2707): "Chennai Central",
        (13.0418, 80.2341): "T. Nagar",
    }
    print("Stop lookup:", stops[(13.0418, 80.2341)])
    try:
        invalid_key = [13.0418, 80.2341]
        print(stops[invalid_key])
    except TypeError as error:
        print("List dictionary-key error:", error)

    # Unpacking tuples
    for latitude, longitude in stops:
        print("Coordinate:", latitude, longitude)

    original = [[1, 2], [3, 4]]
    alias = original
    shallow_copy = copy.copy(original)
    sliced_copy = original[:]
    deep_copy = copy.deepcopy(original)
    original[0][0] = 100
    print("Aliasing sees change:", alias)
    print("Shallow copy shares inner list:", shallow_copy)
    print("Slice copy shares inner list:", sliced_copy)
    print("Deep copy keeps original nested values:", deep_copy)
    print("Function changes caller list:")
    caller_list = [1, 2]
    change_first_row([caller_list])
    print(caller_list)

    values = list(range(1_000_000))
    tuple_values = tuple(values)
    print("sys.getsizeof list (bytes):", sys.getsizeof(values))
    print("sys.getsizeof tuple (bytes):", sys.getsizeof(tuple_values))

    list_data = list(range(100_000))
    tuple_data = tuple(range(100_000))
    _, list_create_time, _ = time_function(lambda: list(range(100_000)))
    _, tuple_create_time, _ = time_function(lambda: tuple(range(100_000)))
    _, list_index_time, _ = time_function(lambda: list_data[50_000])
    _, tuple_index_time, _ = time_function(lambda: tuple_data[50_000])
    print(f"Creation avg: list={list_create_time:.6f}s, tuple={tuple_create_time:.6f}s")
    print(f"Index avg: list={list_index_time:.8f}s, tuple={tuple_index_time:.8f}s")

    mixed = ("bus stop", [10, 20])
    mixed[1].append(30)
    print("Tuple containing a list after inner-list update:", mixed)
    print("Tuple is immutable, but a mutable object stored inside it can change.")
    print("Tuples are hashable when all their elements are hashable; lists are mutable")
    print("and unhashable. Use tuples for fixed coordinates and lists for changeable data.")
    print("Memory diagram: bad rows -> same inner-list object; good rows ->")
    print("three different inner-list objects.")
    print("Sparse grid alternative: dict[(row, col)] = passenger_count;")
    print("average lookup O(1), space O(non-empty zones), versus full grid O(rows*cols).")


# ============================================================
# Q3 – DICTIONARIES: FARMER HELPLINE COMPLAINT ANALYSIS
# ============================================================

def frequencies(texts, stop):
    counts = {}
    for text in texts:
        cleaned = text.lower()
        for punctuation in string.punctuation:
            cleaned = cleaned.replace(punctuation, " ")
        for word in cleaned.split():
            if word not in stop:
                counts[word] = counts.get(word, 0) + 1
    return counts


def top_words(counts, k):
    return sorted(counts.items(), key=lambda item: (-item[1], item[0]))[:k]


def group_by_district(records):
    grouped = {}
    for district, crop, complaint in records:
        grouped.setdefault(district, []).append((crop, complaint))
    return grouped


def q3():
    print("\n" + "=" * 72)
    print("Q3 – DICTIONARIES: FARMER HELPLINE COMPLAINT ANALYSIS")
    print("=" * 72)

    calls = [
        "seeds not received seeds delayed",
        "fertiliser price high",
        "seeds price high subsidy not received",
    ]
    stop = {"not", "high"}
    counts = frequencies(calls, stop)
    print("Word frequencies:", counts)
    print("Top 3:", top_words(counts, 3))
    print("price comes before received because counts tie and alphabetical order")
    print("places 'price' before 'received'.")

    records = [
        ("Salem", "rice", "Seeds delayed"),
        ("Erode", "turmeric", "Fertiliser cost high"),
        ("Salem", "millet", "Water shortage"),
        ("Madurai", "rice", "Pest attack"),
    ]
    print("Complaints grouped by district:", group_by_district(records))
    print("Dictionary keys:", list(counts.keys()))
    print("Dictionary values:", list(counts.values()))
    print("Dictionary items:", list(counts.items()))
    print("Dictionaries preserve insertion order in Python 3.7+.")
    print("Average dictionary lookup/count update is O(1); worst case can be O(n).")

    print("\nDictionary vs list.count() vs Counter experiment:")
    random.seed(7)
    vocabulary = ["seed", "water", "price", "crop", "loan", "pest", "fertiliser"]
    for n in (1_000, 10_000, 100_000):
        texts = [" ".join(random.choices(vocabulary, k=8)) for _ in range(n)]
        words = " ".join(texts).split()
        distinct = set(words)

        def list_count_method():
            return {word: words.count(word) for word in distinct}

        dict_result, dict_time, _ = time_function(
            lambda: frequencies(texts, set()), repeats=3)
        list_result, list_time, _ = time_function(list_count_method, repeats=3)
        counter_result, counter_time, _ = time_function(
            lambda: Counter(words), repeats=3)
        print(f"{n:,} complaints: dict={dict_time:.6f}s; "
              f"list.count={list_time:.6f}s; Counter={counter_time:.6f}s")
        print("  Word totals match:", dict_result == list_result == dict(counter_result))

    print("Empty/case/punctuation test:",
          frequencies(["", "SEEDS, seeds! Seeds."], set()))
    print("Deploy dictionary/Counter for 100,000 complaints: average O(n) counting.")
    print("list.count for every distinct word is O(n*d), where d is distinct words.")
    print("Dictionary and Counter use O(d) count storage.")


# ============================================================
# Q4 – SETS: ELECTIVE REGISTRATION CLASH DETECTION
# ============================================================

def q4():
    print("\n" + "=" * 72)
    print("Q4 – SETS: ELECTIVE REGISTRATION CLASH DETECTION")
    print("=" * 72)

    ai_elective = {"192311001", "192311004", "192311007", "192311009"}
    iot_elective = {"192311002", "192311004", "192311009", "192311010"}
    all_students = {f"1923110{i:02d}" for i in range(1, 11)}

    both = ai_elective & iot_elective
    exactly_one = ai_elective ^ iot_elective
    neither = all_students - (ai_elective | iot_elective)

    print("clash :", sorted(both))
    print("exactly one:", sorted(exactly_one))
    print("neither :", sorted(neither))

    # Repeat using set methods
    both_method = ai_elective.intersection(iot_elective)
    exactly_method = ai_elective.symmetric_difference(iot_elective)
    neither_method = all_students.difference(ai_elective.union(iot_elective))
    print("Method results match:", both == both_method and
          exactly_one == exactly_method and neither == neither_method)

    # Duplicate registrations are removed automatically by sets.
    duplicate_list = ["A101", "A101", "A102", "A103"]
    print("List with duplicates:", duplicate_list)
    print("Converted set:", set(duplicate_list))
    print("Venn explanation: intersection = overlap; symmetric difference =")
    print("non-overlapping parts; difference = students outside both electives.")

    print("\nMembership timing (three-run averages):")
    for n in (10_000, 100_000, 1_000_000):
        data = list(range(n))
        data_set = set(data)
        target = n - 1
        _, list_time, _ = time_function(lambda: target in data, repeats=3)
        _, set_time, _ = time_function(lambda: target in data_set, repeats=3)
        print(f"n={n:,}: list membership={list_time:.6f}s; "
              f"set membership={set_time:.8f}s")

    print("Nested-loop intersection vs set intersection:")
    left = list(range(3000))
    right = list(range(1500, 4500))
    start = time.perf_counter()
    nested = [x for x in left for y in right if x == y]
    nested_time = time.perf_counter() - start
    start = time.perf_counter()
    set_result = set(left) & set(right)
    set_time = time.perf_counter() - start
    print(f"Nested loops={nested_time:.6f}s; set &={set_time:.6f}s; "
          f"same={set(nested) == set_result}")

    print("Empty and identical tests:",
          set() & iot_elective, ai_elective & ai_elective)
    try:
        bad_set = {[1, 2]}
        print(bad_set)
    except TypeError as error:
        print("A set cannot contain a list:", error)
    print("Sets are useful for membership and duplicate removal, but lose order")
    print("and repeated occurrences. Set membership/intersection is O(1) average")
    print("for membership and O(n+m) average for building/intersecting sets.")


# ============================================================
# Q5 – LIST COMPREHENSION: CLEANING SENSOR READINGS
# ============================================================

def clean_loop(readings):
    valid_c = []
    valid_f = []
    for value in readings:
        if -50 <= value <= 50:
            valid_c.append(value)
            valid_f.append(value * 9 / 5 + 32)
    return valid_c, valid_f


def clean_comprehension(readings):
    valid_c = [value for value in readings if -50 <= value <= 50]
    valid_f = [value * 9 / 5 + 32 for value in readings if -50 <= value <= 50]
    return valid_c, valid_f


def clean_map_filter(readings):
    valid = list(filter(lambda value: -50 <= value <= 50, readings))
    fahrenheit = list(map(lambda value: value * 9 / 5 + 32, valid))
    return valid, fahrenheit


def q5():
    print("\n" + "=" * 72)
    print("Q5 – LIST COMPREHENSION: CLEANING SENSOR READINGS")
    print("=" * 72)

    readings = [4, 5, 9, 2, 55, -60, 7, 10, 0, 51, -2]
    loop_c, loop_f = clean_loop(readings)
    comp_c, comp_f = clean_comprehension(readings)
    map_c, map_f = clean_map_filter(readings)
    alarm_minutes = [
        minute for minute, temp in enumerate(readings, start=1)
        if temp < 2 or temp > 8
    ]
    print("Original readings:", readings)
    print("Valid Celsius:", comp_c)
    print("Valid Fahrenheit:", [round(x, 2) for x in comp_f])
    print("Alarm minutes (1-based):", alarm_minutes)
    print("All three versions match:", loop_c == comp_c == map_c and
          loop_f == comp_f == map_f)

    # Dictionary and set comprehensions
    c_to_f = {c: round(c * 9 / 5 + 32, 2) for c in comp_c}
    unique_valid = {c for c in readings if -50 <= c <= 50}
    print("Dictionary comprehension Celsius -> Fahrenheit:", c_to_f)
    print("Set comprehension of unique valid readings:", unique_valid)
    print("Comprehension form: [expression for item in iterable if condition].")
    print("A generator expression produces values lazily; a list comprehension")
    print("stores all results. Use a loop when logic is long or needs several steps.")

    print("\nTiming experiments (three-run averages):")
    random.seed(15)
    for n in (10_000, 100_000, 1_000_000):
        data = [random.randint(-70, 70) for _ in range(n)]
        _, loop_time, _ = time_function(clean_loop, data)
        _, comp_time, _ = time_function(clean_comprehension, data)
        _, map_time, _ = time_function(clean_map_filter, data)
        print(f"n={n:,}: loop={loop_time:.6f}s; "
              f"comprehension={comp_time:.6f}s; map/filter={map_time:.6f}s")

    valid_all = [5] * 20
    invalid_all = [70, -70] * 10
    print("All valid count:", len(clean_comprehension(valid_all)[0]))
    print("All invalid count:", len(clean_comprehension(invalid_all)[0]))

    list_comp = [x * 2 for x in range(1000)]
    generator = (x * 2 for x in range(1000))
    print("List object size:", sys.getsizeof(list_comp))
    print("Generator object size:", sys.getsizeof(generator))
    print("Both approaches take O(n) time; list uses O(n) result memory,")
    print("generator uses O(1) extra iteration memory (excluding consumed output).")


# ============================================================
# Q6 – NESTED DATA: RAILWAY TIMETABLE
# ============================================================

def make_timetable(number_of_trains):
    timetable = {}
    station_names = ["Chennai", "Katpadi", "Jolarpettai", "Salem",
                     "Erode", "Coimbatore", "Bengaluru"]
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    for i in range(number_of_trains):
        train_no = str(12000 + i)
        start_hour = 5 + (i % 10)
        stops = []
        for j, station in enumerate(station_names):
            hour = (start_hour + j) % 24
            arrival = f"{hour:02d}:{(j * 10) % 60:02d}"
            departure = f"{hour:02d}:{(j * 10 + 5) % 60:02d}"
            stops.append((station, arrival, departure))
        timetable[train_no] = {
            "name": f"Express {i + 1}",
            "stops": stops,
            "days": set(days if i % 4 else days[:5]),
        }
    return timetable


def build_station_index(timetable):
    index = defaultdict(list)
    for train_no, details in timetable.items():
        for station, arrival, departure in details["stops"]:
            index[station].append(train_no)
    return dict(index)


def trains_at_station(timetable, station, day):
    matches = []
    for train_no, details in timetable.items():
        if day not in details["days"]:
            continue
        for stop, arrival, departure in details["stops"]:
            if stop == station:
                matches.append((departure, train_no, details["name"]))
                break
    return sorted(matches, key=lambda item: item[0])


def trains_at_station_indexed(timetable, index, station, day):
    matches = []
    for train_no in index.get(station, []):
        details = timetable[train_no]
        if day not in details["days"]:
            continue
        for stop, arrival, departure in details["stops"]:
            if stop == station:
                matches.append((departure, train_no, details["name"]))
                break
    return sorted(matches, key=lambda item: item[0])


def q6():
    print("\n" + "=" * 72)
    print("Q6 – NESTED DATA: RAILWAY TIMETABLE")
    print("=" * 72)

    timetable = make_timetable(5)
    for train_no, details in timetable.items():
        print(train_no, details["name"], details["stops"][:3], details["days"])

    station = "Salem"
    day = "Mon"
    print(f"Trains stopping at {station} on {day}:",
          trains_at_station(timetable, station, day))
    print("Unknown station:", trains_at_station(timetable, "Unknown", day))
    print("Expression for third station departure:")
    first_train = next(iter(timetable))
    print("timetable[train_no]['stops'][2][2] =",
          timetable[first_train]["stops"][2][2])
    print("Structure: train number -> dictionary -> stop list -> station/time tuple.")
    print("Dictionary gives train lookup; list preserves stop order; tuple keeps")
    print("each stop record together; set stores running days.")

    print("\nStation query experiment:")
    for n in (100, 1_000, 10_000):
        data = make_timetable(n)
        index = build_station_index(data)
        _, scan_time, _ = time_function(
            trains_at_station, data, "Salem", "Mon", repeats=3)
        _, index_time, _ = time_function(
            trains_at_station_indexed, data, index, "Salem", "Mon", repeats=3)
        print(f"{n:,} trains: scan={scan_time:.6f}s; "
              f"indexed={index_time:.6f}s; indexed station entries="
              f"{len(index.get('Salem', []))}")
        print("  Approx index container size:", sys.getsizeof(index))

    print("An index maps station -> list of train numbers. It reduces each query")
    print("to checking trains at that station, at the cost of extra memory and")
    print("update work when the timetable changes.")
    print("Flat-list alternative scans every stop for each query: O(total stops);")
    print("station index query is about O(trains at station), plus sorting results.")


# ============================================================
# Q7 – CONTACT MERGING FROM FIRST PRINCIPLES
# ============================================================

def normalise_phone(phone):
    """Keep digits only and remove India's leading country code 91."""
    digits = "".join(ch for ch in str(phone) if ch.isdigit())
    if len(digits) == 12 and digits.startswith("91"):
        digits = digits[2:]
    return digits


def normalise_name(name):
    return " ".join(str(name or "").lower().replace(".", " ").split())


def merge_contacts(contacts):
    """
    Group contacts by normalised phone number.
    Each merged record stores a set of phone numbers and e-mail addresses.
    """
    merged = {}
    for contact in contacts:
        raw_phone = contact.get("phone", "")
        phone = normalise_phone(raw_phone)
        if not phone:
            # Contacts without a usable phone cannot safely be matched by number.
            # Keep each such contact as a separate record.
            key = "NO_PHONE_" + str(len(merged))
        else:
            key = phone

        if key not in merged:
            merged[key] = {
                "name": contact.get("name", "").strip() or "Unknown",
                "normalised_name": normalise_name(contact.get("name", "")),
                "phones": set(),
                "emails": set(),
            }

        if raw_phone:
            merged[key]["phones"].add(str(raw_phone).strip())
        email = contact.get("email", "").strip().lower()
        if email:
            merged[key]["emails"].add(email)

        # Keep the longer supplied name as a simple display-name choice.
        new_name = contact.get("name", "").strip()
        if len(new_name) > len(merged[key]["name"]):
            merged[key]["name"] = new_name

    return list(merged.values())


def pairwise_merge_contacts(contacts):
    """Simple O(n^2) comparison version for performance comparison."""
    groups = []
    for contact in contacts:
        phone = normalise_phone(contact.get("phone", ""))
        found = False
        if phone:
            for group in groups:
                group_phone = normalise_phone(next(iter(group["phones"]), ""))
                if group_phone == phone:
                    if contact.get("phone"):
                        group["phones"].add(contact["phone"])
                    if contact.get("email"):
                        group["emails"].add(contact["email"].lower())
                    found = True
                    break
        if not found:
            groups.append({
                "name": contact.get("name", "").strip() or "Unknown",
                "phones": {contact["phone"]} if contact.get("phone") else set(),
                "emails": {contact["email"].lower()} if contact.get("email") else set(),
            })
    return groups


def generate_contacts(n):
    contacts = []
    for i in range(n):
        person = i // 2  # each pair intentionally shares a number
        phone = f"+91 98400 {person % 100000:05d}"
        if i % 2:
            phone = phone.replace(" ", "")
        contacts.append({
            "name": f"Person {person}",
            "phone": phone,
            "email": f"person{person}@example.com" if i % 3 else "",
        })
    return contacts


def q7():
    print("\n" + "=" * 72)
    print("Q7 – CONTACT MERGING FROM FIRST PRINCIPLES")
    print("=" * 72)

    contacts = [
        {"name": "Dr. Ravi", "phone": "+91 98400 12345", "email": "RAVI@MAIL.COM"},
        {"name": "ravi kumar", "phone": "9840012345", "email": "ravi.work@mail.com"},
        {"name": "Anu", "phone": "9876543210", "email": "anu@mail.com"},
        {"name": "Anu", "phone": "", "email": "anu2@mail.com"},
        {"name": "Unknown", "phone": "9000011111", "email": ""},
    ]
    print("Input contacts:", contacts)
    merged = merge_contacts(contacts)
    print("Merged contacts:")
    for person in merged:
        print(person)

    print("Requirements: one merged record per normalised phone number; preserve")
    print("all supplied phone formats and unique e-mail addresses.")
    print("Design pseudocode: normalise phone; use it as dictionary key; create")
    print("record if absent; add phone/email to sets; update display name.")
    print("A dictionary avoids comparing every contact with every other contact.")
    print("Two people with the same name but different phone numbers remain separate.")
    print("Limitation: contacts with missing phone numbers cannot be confidently")
    print("matched; this example keeps them separate.")

    print("\nContact merge timing:")
    for n in (1_000, 100_000):
        data = generate_contacts(n)
        _, dictionary_time, _ = time_function(merge_contacts, data, repeats=3)
        # Pairwise comparison is deliberately capped to keep runtime practical.
        if n <= 1_000:
            _, pair_time, _ = time_function(pairwise_merge_contacts, data, repeats=3)
            pair_text = f"{pair_time:.6f}s"
        else:
            pair_text = "not run at 100,000 (quadratic comparison is very slow)"
        print(f"{n:,} contacts: dictionary={dictionary_time:.6f}s; "
              f"pairwise={pair_text}; merged={len(merge_contacts(data))}")

    print("Dictionary grouping is O(n) average time and O(n) space.")
    print("Pairwise comparison is O(n^2) time and O(n) output/group storage.")
    print("Dictionary keys are based on phone number, not name, so shared names")
    print("do not incorrectly merge different people.")


# ============================================================
# MAIN – RUN ALL QUESTIONS
# ============================================================

def main():
    q1()
    q2()
    q3()
    q4()
    q5()
    q6()
    q7()
    print("\nAssignment 3 – all Q1 to Q7 demonstrations completed.")


if __name__ == "__main__":
    main()
