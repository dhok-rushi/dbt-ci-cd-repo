import random
from pathlib import Path

import numpy as np
import pandas as pd
from faker import Faker
import os



# ---------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------

# Reproducible random data
random.seed(42)
np.random.seed(42)
fake = Faker()
Faker.seed(42)

# Output folder
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "dbt_project/data"
DATA_DIR.mkdir(exist_ok=True)

# Row counts
NUM_CUSTOMERS = 750
NUM_DRIVERS = 300
NUM_VEHICLES = 300
NUM_LOCATIONS = 50
NUM_TRIPS = 1000
NUM_PAYMENTS = 1000
NUM_TRIP_EVENTS = 5000
NUM_PROMOTIONS = 25

# Master Data
CITIES = [
    "Mumbai",
    "Pune",
    "Bengaluru",
    "Hyderabad",
    "Delhi",
    "Chennai",
    "Ahmedabad",
    "Kolkata"
]

VEHICLE_TYPES = [
    "Sedan",
    "SUV",
    "Mini",
    "Luxury",
    "Electric"
]

PAYMENT_METHODS = [
    "Credit Card",
    "Debit Card",
    "Cash",
    "Wallet"
]

TRIP_STATUS = [
    "Completed",
    "Cancelled",
    "In Progress"
]

CUSTOMER_STATUS = [
    "Active",
    "Inactive"
]

DRIVER_STATUS = [
    "Active",
    "Inactive"
]

# ----
VEHICLE_MAKES = [
    "Maruti Suzuki",
    "Hyundai",
    "Tata",
    "Mahindra",
    "Honda",
    "Toyota",
    "Kia"
]

VEHICLE_MODELS = [
    "Swift",
    "Baleno",
    "Creta",
    "Nexon",
    "XUV700",
    "City",
    "Innova",
    "Seltos"
]

# ----
LOCATIONS = [
    ("Mumbai Airport", "Mumbai", "Maharashtra"),
    ("BKC", "Mumbai", "Maharashtra"),
    ("Bandra Station", "Mumbai", "Maharashtra"),
    ("Powai", "Mumbai", "Maharashtra"),
    ("Andheri East", "Mumbai", "Maharashtra"),
    ("Pune Railway Station", "Pune", "Maharashtra"),
    ("Hinjewadi Phase 1", "Pune", "Maharashtra"),
    ("Koregaon Park", "Pune", "Maharashtra"),
    ("MG Road", "Bengaluru", "Karnataka"),
    ("Electronic City", "Bengaluru", "Karnataka"),
    ("Whitefield", "Bengaluru", "Karnataka"),
    ("Kempegowda Airport", "Bengaluru", "Karnataka"),
    ("Hitech City", "Hyderabad", "Telangana"),
    ("Gachibowli", "Hyderabad", "Telangana"),
    ("Charminar", "Hyderabad", "Telangana"),
    ("Rajiv Gandhi Airport", "Hyderabad", "Telangana"),
    ("Connaught Place", "Delhi", "Delhi"),
    ("New Delhi Railway Station", "Delhi", "Delhi"),
    ("IGI Airport", "Delhi", "Delhi"),
    ("Saket", "Delhi", "Delhi"),
    ("T Nagar", "Chennai", "Tamil Nadu"),
    ("OMR", "Chennai", "Tamil Nadu"),
    ("Chennai Central", "Chennai", "Tamil Nadu"),
    ("Chennai Airport", "Chennai", "Tamil Nadu"),
    ("SG Highway", "Ahmedabad", "Gujarat"),
    ("Maninagar", "Ahmedabad", "Gujarat"),
    ("Kalupur Station", "Ahmedabad", "Gujarat"),
    ("Ahmedabad Airport", "Ahmedabad", "Gujarat"),
    ("Park Street", "Kolkata", "West Bengal"),
    ("Howrah Station", "Kolkata", "West Bengal"),
    ("Salt Lake", "Kolkata", "West Bengal"),
    ("Kolkata Airport", "Kolkata", "West Bengal")
]


# delibrately keeping this to understand piece of code - 
from datetime import datetime, timedelta
#-------------------------------------------

def generate_customers():
    """Generate customer master data."""

    customers = []

    for customer_id in range(1, NUM_CUSTOMERS + 1):

        signup_date = fake.date_between(
            start_date="-3y",
            end_date="-30d"
        )

        updated_at = fake.date_time_between(
            start_date=signup_date,
            end_date="now"
        )

        customers.append({
            "customer_id": customer_id,
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "email": fake.unique.email(),
            "phone": fake.msisdn()[:10],
            "city": random.choice(CITIES),
            "state": "India",
            "signup_date": signup_date,
            "customer_status": random.choices(
                ["Active", "Inactive"],
                weights=[90, 10]
            )[0],
            "updated_at": updated_at
        })

    df = pd.DataFrame(customers)

    df.to_csv(
        DATA_DIR / "customers.csv",
        index=False
    )

    print(f"Generated {len(df)} customers")

def generate_drivers():
    """Generate driver master data."""

    drivers = []

    for driver_id in range(1, NUM_DRIVERS + 1):

        joined_date = fake.date_between(
            start_date="-5y",
            end_date="-60d"
        )

        updated_at = fake.date_time_between(
            start_date=joined_date,
            end_date="now"
        )

        drivers.append({
            "driver_id": driver_id,
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "phone": fake.msisdn()[:10],
            "license_number": f"DL-{100000 + driver_id}",
            "rating": round(random.uniform(3.5, 5.0), 1),
            "city": random.choice(CITIES),
            "driver_status": random.choices(
                ["Active", "Inactive"],
                weights=[95, 5]
            )[0],
            "joined_date": joined_date,
            "updated_at": updated_at
        })

    df = pd.DataFrame(drivers)

    output_file = DATA_DIR / "drivers.csv"

    df.to_csv(output_file, index=False)

    print(f"✅ Generated {len(df)} drivers")
    print(f"✅ File saved to: {output_file}")

def generate_vehicles():
    """Generate vehicle master data."""

    vehicles = []

    for vehicle_id in range(1, NUM_VEHICLES + 1):

        vehicles.append({
            "vehicle_id": vehicle_id,
            "driver_id": vehicle_id,
            "make": random.choice(VEHICLE_MAKES),
            "model": random.choice(VEHICLE_MODELS),
            "year": random.randint(2018, 2025),
            "vehicle_type": random.choice(VEHICLE_TYPES),
            "registration_number": f"MH{random.randint(10,99)}AB{1000+vehicle_id}",
            "updated_at": fake.date_time_between(
                start_date="-2y",
                end_date="now"
            )
        })

    df = pd.DataFrame(vehicles)

    output_file = DATA_DIR / "vehicles.csv"

    df.to_csv(output_file, index=False)

    print(f"✅ Generated {len(df)} vehicles")
    print(f"✅ File saved to: {output_file}")

def generate_locations():
    """Generate pickup and drop-off locations."""

    locations = []

    for location_id, (location_name, city, state) in enumerate(LOCATIONS, start=1):

        locations.append({
            "location_id": location_id,
            "location_name": location_name,
            "city": city,
            "state": state,
            "latitude": round(random.uniform(8.0, 30.0), 6),
            "longitude": round(random.uniform(68.0, 88.0), 6)
        })

    df = pd.DataFrame(locations)

    output_file = DATA_DIR / "locations.csv"

    df.to_csv(output_file, index=False)

    print(f"✅ Generated {len(df)} locations")
    print(f"✅ File saved to: {output_file}")

def generate_promotions():
    """Generate promotion master data."""

    promotions = []

    for promo_id in range(1, NUM_PROMOTIONS + 1):

        start_date = fake.date_between(
            start_date="-2y",
            end_date="-90d"
        )

        end_date = start_date + timedelta(days=random.randint(30, 180))

        promotions.append({
            "promo_id": promo_id,
            "promo_code": f"RIDE{promo_id:03}",
            "discount_percent": random.choice([5, 10, 15, 20, 25, 30]),
            "start_date": start_date,
            "end_date": end_date,
            "is_active": random.choice(["Y", "N"])
        })

    df = pd.DataFrame(promotions)

    output_file = DATA_DIR / "promotions.csv"

    df.to_csv(output_file, index=False)

    print(f"✅ Generated {len(df)} promotions")
    print(f"✅ File saved to: {output_file}")

def load_reference_data():
    """Load all reference datasets required for trip generation."""

    customers_df = pd.read_csv(DATA_DIR / "customers.csv")
    drivers_df = pd.read_csv(DATA_DIR / "drivers.csv")
    vehicles_df = pd.read_csv(DATA_DIR / "vehicles.csv")
    locations_df = pd.read_csv(DATA_DIR / "locations.csv")
    promotions_df = pd.read_csv(DATA_DIR / "promotions.csv")
    # trips_df = pd.read_csv(DATA_DIR / "trips.csv")
    
    # Assign trip frequency weights to customers
    customer_weights = []

    for _ in range(len(customers_df)):
        r = random.random()

        if r < 0.60:
            customer_weights.append(1)   # Occasional rider
        elif r < 0.90:
            customer_weights.append(3)   # Regular rider
        else:
            customer_weights.append(8)   # Frequent rider

    customers_df["trip_weight"] = customer_weights

    # Drivers grouped by city
    drivers_by_city = (
        drivers_df.groupby("city")["driver_id"]
        .apply(list)
        .to_dict()
    )

    # Driver → Vehicle lookup
    vehicle_lookup = (
        vehicles_df.set_index("driver_id")["vehicle_id"]
        .to_dict()
    )

    # Locations grouped by city
    locations_by_city = (
        locations_df.groupby("city")["location_id"]
        .apply(list)
        .to_dict()
    )

    return {
        "customers": customers_df,
        "drivers": drivers_df,
        "vehicles": vehicles_df,
        "locations": locations_df,
        "promotions": promotions_df,
        "drivers_by_city": drivers_by_city,
        "vehicle_lookup": vehicle_lookup,
        "locations_by_city": locations_by_city,
    }

def generate_trips():
    """Generate synthetic trip data."""

    reference_data = load_reference_data()

    customers_df = reference_data["customers"]
    promotions_df = reference_data["promotions"]

    drivers_by_city = reference_data["drivers_by_city"]
    vehicle_lookup = reference_data["vehicle_lookup"]
    locations_by_city = reference_data["locations_by_city"]

    trips = []

    customer_population = customers_df.index.tolist()
    customer_weights = customers_df["trip_weight"].tolist()

    all_cities = list(locations_by_city.keys())

    for trip_id in range(1, NUM_TRIPS + 1):

        # --------------------------------------------------
        # Select Customer (Weighted)
        # --------------------------------------------------
        selected_index = random.choices(
            population=customer_population,
            weights=customer_weights,
            k=1
        )[0]

        customer = customers_df.loc[selected_index]

        # --------------------------------------------------
        # Pickup City
        # --------------------------------------------------
        pickup_city = customer["city"]

        pickup_location_id = random.choice(
            locations_by_city[pickup_city]
        )

        # --------------------------------------------------
        # Drop City
        # 95% within city
        # 5% intercity
        # --------------------------------------------------
        if random.random() < 0.95:
            drop_city = pickup_city
        else:
            other_cities = [
                city for city in all_cities
                if city != pickup_city
            ]
            drop_city = random.choice(other_cities)

        drop_location_id = random.choice(
            locations_by_city[drop_city]
        )

        while drop_location_id == pickup_location_id:
            drop_location_id = random.choice(
                locations_by_city[drop_city]
            )

        # --------------------------------------------------
        # Driver & Vehicle
        # --------------------------------------------------
        driver_id = random.choice(
            drivers_by_city[pickup_city]
        )

        vehicle_id = vehicle_lookup[driver_id]

        # --------------------------------------------------
        # Distance
        # --------------------------------------------------
        if pickup_city == drop_city:
            distance_km = round(
                random.uniform(2, 25),
                2
            )
        else:
            distance_km = round(
                random.uniform(120, 300),
                2
            )

        # --------------------------------------------------
        # Request Timestamp
        # --------------------------------------------------
        request_timestamp = fake.date_time_between(
            start_date="-365d",
            end_date="now"
        )

        pickup_timestamp = request_timestamp + timedelta(
            minutes=random.randint(2, 15)
        )

        # --------------------------------------------------
        # Trip Status
        # --------------------------------------------------
        trip_status = random.choices(
            population=[
                "Completed",
                "Cancelled",
                "In Progress"
            ],
            weights=[92, 6, 2],
            k=1
        )[0]

        # --------------------------------------------------
        # Trip Duration
        # --------------------------------------------------
        average_speed = 30

        trip_duration = max(
            5,
            int((distance_km / average_speed) * 60)
        )

        if trip_status == "Completed":

            dropoff_timestamp = pickup_timestamp + timedelta(
                minutes=trip_duration
            )

        elif trip_status == "Cancelled":

            pickup_timestamp = None
            dropoff_timestamp = None

        else:

            dropoff_timestamp = None

        # --------------------------------------------------
        # Surge
        # --------------------------------------------------
        surge_multiplier = random.choices(
            [1.0, 1.2, 1.5, 2.0],
            weights=[70, 20, 8, 2],
            k=1
        )[0]

        # --------------------------------------------------
        # Fare
        # --------------------------------------------------
        base_fare = 50
        rate_per_km = 18

        fare_amount = round(
            (base_fare + (distance_km * rate_per_km))
            * surge_multiplier,
            2
        )

        # --------------------------------------------------
        # Promotion
        # --------------------------------------------------
        if random.random() < 0.30:
            promo = promotions_df.sample(1).iloc[0]
            promo_id = promo["promo_id"]
        else:
            promo_id = 0

        # --------------------------------------------------
        # Append Trip
        # --------------------------------------------------
        trips.append({
            "trip_id": trip_id,
            "customer_id": customer["customer_id"],
            "driver_id": driver_id,
            "vehicle_id": vehicle_id,
            "pickup_location_id": pickup_location_id,
            "drop_location_id": drop_location_id,
            "request_timestamp": request_timestamp,
            "pickup_timestamp": pickup_timestamp,
            "dropoff_timestamp": dropoff_timestamp,
            "trip_status": trip_status,
            "distance_km": distance_km,
            "fare_amount": fare_amount,
            "surge_multiplier": surge_multiplier,
            "promo_id": promo_id,
            "updated_at": datetime.now()
        })

    trips_df = pd.DataFrame(trips)

    output_file = DATA_DIR / "trips.csv"

    trips_df.to_csv(output_file, index=False)

    print(f"✅ Generated {len(trips_df)} trips")
    print(f"✅ Saved to {output_file}")

def generate_payments():
    """Generate payment records from trips."""

    trips_df = pd.read_csv(DATA_DIR / "trips.csv")
    promotions_df = pd.read_csv(DATA_DIR / "promotions.csv")

    # Convert dates
    promotions_df["start_date"] = pd.to_datetime(promotions_df["start_date"])
    promotions_df["end_date"] = pd.to_datetime(promotions_df["end_date"])

    promotion_lookup = (
        promotions_df
        .set_index("promo_id")
        .to_dict("index")
    )

    payments = []

    payment_methods = [
        "UPI",
        "Credit Card",
        "Debit Card",
        "Wallet",
        "Cash"
    ]

    payment_weights = [
        45,
        25,
        15,
        10,
        5
    ]

    for _, trip in trips_df.iterrows():

        gross_amount = float(trip["fare_amount"])
        discount_amount = 0
        tax_amount = 0
        net_amount = 0

        payment_timestamp = None
        payment_method = None

        # -------------------------
        # Payment Status
        # -------------------------
        if trip["trip_status"] == "Completed":

            payment_status = "Success"

            payment_timestamp = (
                pd.to_datetime(trip["dropoff_timestamp"])
                + timedelta(minutes=random.randint(1, 5))
            )

            payment_method = random.choices(
                payment_methods,
                weights=payment_weights,
                k=1
            )[0]

            # -------------------------
            # Promotion
            # -------------------------
            promo_id = int(trip["promo_id"])

            if promo_id != 0 and promo_id in promotion_lookup:

                promo = promotion_lookup[promo_id]

                if promo["is_active"]:

                    discount_amount = round(
                        gross_amount *
                        (promo["discount_percent"] / 100),
                        2
                    )

            subtotal = gross_amount - discount_amount

            tax_amount = round(
                subtotal * 0.05,
                2
            )

            net_amount = round(
                subtotal + tax_amount,
                2
            )

        elif trip["trip_status"] == "Cancelled":

            payment_status = "Cancelled"

        else:

            payment_status = "Pending"

        payments.append({

            "payment_id": len(payments) + 1,

            "trip_id": trip["trip_id"],

            "customer_id": trip["customer_id"],

            "payment_timestamp": payment_timestamp,

            "payment_method": payment_method,

            "payment_status": payment_status,

            "gross_amount": gross_amount,

            "discount_amount": discount_amount,

            "tax_amount": tax_amount,

            "net_amount": net_amount,

            "updated_at": datetime.now()

        })

    payments_df = pd.DataFrame(payments)

    output_file = DATA_DIR / "payments.csv"

    payments_df.to_csv(output_file, index=False)

    print(f"✅ Generated {len(payments_df)} payments")
    print(f"✅ Saved to {output_file}")

def generate_trip_events():
    """Generate trip lifecycle events."""

    trips_df = pd.read_csv(DATA_DIR / "trips.csv")

    trip_events = []

    event_id = 1

    for _, trip in trips_df.iterrows():

        request_ts = pd.to_datetime(trip["request_timestamp"])

        pickup_ts = (
            pd.to_datetime(trip["pickup_timestamp"])
            if pd.notna(trip["pickup_timestamp"])
            else None
        )

        dropoff_ts = (
            pd.to_datetime(trip["dropoff_timestamp"])
            if pd.notna(trip["dropoff_timestamp"])
            else None
        )

        sequence = 1

        # --------------------------------------------------
        # TRIP_REQUESTED
        # --------------------------------------------------
        trip_events.append({
            "event_id": event_id,
            "trip_id": trip["trip_id"],
            "customer_id": trip["customer_id"],
            "driver_id": trip["driver_id"],
            "event_sequence": sequence,
            "event_type": "TRIP_REQUESTED",
            "event_timestamp": request_ts,
            "updated_at": datetime.now()
        })

        event_id += 1
        sequence += 1

        # --------------------------------------------------
        # CANCELLED
        # --------------------------------------------------
        if trip["trip_status"] == "Cancelled":

            trip_events.append({
                "event_id": event_id,
                "trip_id": trip["trip_id"],
                "customer_id": trip["customer_id"],
                "driver_id": trip["driver_id"],
                "event_sequence": sequence,
                "event_type": "TRIP_CANCELLED",
                "event_timestamp": request_ts + timedelta(
                    minutes=random.randint(1, 5)
                ),
                "updated_at": datetime.now()
            })

            event_id += 1
            continue

        # --------------------------------------------------
        # DRIVER_ASSIGNED
        # --------------------------------------------------
        assigned_ts = request_ts + timedelta(
            seconds=random.randint(20, 90)
        )

        trip_events.append({
            "event_id": event_id,
            "trip_id": trip["trip_id"],
            "customer_id": trip["customer_id"],
            "driver_id": trip["driver_id"],
            "event_sequence": sequence,
            "event_type": "DRIVER_ASSIGNED",
            "event_timestamp": assigned_ts,
            "updated_at": datetime.now()
        })

        event_id += 1
        sequence += 1

        # --------------------------------------------------
        # DRIVER_ARRIVED
        # --------------------------------------------------
        if pickup_ts is not None:

            arrived_ts = pickup_ts - timedelta(
                minutes=random.randint(1, 3)
            )

            trip_events.append({
                "event_id": event_id,
                "trip_id": trip["trip_id"],
                "customer_id": trip["customer_id"],
                "driver_id": trip["driver_id"],
                "event_sequence": sequence,
                "event_type": "DRIVER_ARRIVED",
                "event_timestamp": arrived_ts,
                "updated_at": datetime.now()
            })

            event_id += 1
            sequence += 1

            # ----------------------------------------------
            # TRIP_STARTED
            # ----------------------------------------------
            trip_events.append({
                "event_id": event_id,
                "trip_id": trip["trip_id"],
                "customer_id": trip["customer_id"],
                "driver_id": trip["driver_id"],
                "event_sequence": sequence,
                "event_type": "TRIP_STARTED",
                "event_timestamp": pickup_ts,
                "updated_at": datetime.now()
            })

            event_id += 1
            sequence += 1

        # --------------------------------------------------
        # TRIP_COMPLETED
        # --------------------------------------------------
        if (
            trip["trip_status"] == "Completed"
            and dropoff_ts is not None
        ):

            trip_events.append({
                "event_id": event_id,
                "trip_id": trip["trip_id"],
                "customer_id": trip["customer_id"],
                "driver_id": trip["driver_id"],
                "event_sequence": sequence,
                "event_type": "TRIP_COMPLETED",
                "event_timestamp": dropoff_ts,
                "updated_at": datetime.now()
            })

            event_id += 1

    trip_events_df = pd.DataFrame(trip_events)

    output_file = DATA_DIR / "trip_events.csv"

    trip_events_df.to_csv(output_file, index=False)

    print(f"✅ Generated {len(trip_events_df)} trip events")
    print(f"✅ Saved to {output_file}")

if __name__ == "__main__":
    generate_customers()
    generate_drivers()
    generate_vehicles()
    generate_locations()
    generate_promotions()
    generate_trips()
    generate_payments()
    generate_trip_events()