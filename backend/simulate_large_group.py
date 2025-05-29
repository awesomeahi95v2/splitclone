import requests
import random
import time

BASE_URL = "http://splitclone-alb-905942501.us-east-1.elb.amazonaws.com"

NUM_USERS = 10
NUM_EXPENSES = 50
PASSWORD = "test123"

# STEP 1: Sign up users
print("Signing up users...")
users = []
for i in range(NUM_USERS):
    email = f"user{i}@example.com"
    res = requests.post(f"{BASE_URL}/signup", json={"email": email, "password": PASSWORD})
    user_id = res.json()["id"]
    users.append({"id": user_id, "email": email})
    time.sleep(0.2)

# STEP 2: Create a group by user 0
print("Creating group...")
res = requests.post(f"{BASE_URL}/groups/create", json={
    "name": "Large Group Test",
    "user_id": users[0]["id"]
})
group_id = res.json()["id"]
time.sleep(0.2)

# STEP 3: Invite and accept other users
print("Inviting and accepting users...")
for user in users[1:]:
    requests.post(f"{BASE_URL}/groups/{group_id}/invite", json={"email": user["email"]})
    requests.post(f"{BASE_URL}/groups/{group_id}/respond", json={"user_id": user["id"], "accept": True})
    time.sleep(0.2)

# STEP 4: Create 50 random expenses
print("Creating expenses...")
for _ in range(NUM_EXPENSES):
    paid_by = random.choice(users)["id"]
    created_by = paid_by  # Simulate the payer as creator
    amount = round(random.uniform(10, 300), 2)
    description = random.choice(["Dinner", "Drinks", "Hotel", "Taxi", "Museum"])
    payload = {
        "description": description,
        "amount": amount,
        "currency": "GBP",
        "paid_by": paid_by,
        "created_by_user_id": created_by
    }
    res = requests.post(f"{BASE_URL}/groups/{group_id}/expenses", json=payload)
    time.sleep(0.1)
    
# STEP 4: Create 50 random expenses with random involved users
print("Creating expenses...")
for _ in range(NUM_EXPENSES):
    paid_by = random.choice(users)["id"]
    created_by = paid_by
    amount = round(random.uniform(10, 300), 2)
    description = random.choice(["Dinner", "Drinks", "Hotel", "Taxi", "Museum"])

    # Select 2 to all users to split the expense with
    involved_users = random.sample(users, k=random.randint(2, NUM_USERS))
    involved_user_ids = [user["id"] for user in involved_users]

    payload = {
        "description": description,
        "amount": amount,
        "currency": "GBP",
        "paid_by": paid_by,
        "created_by_user_id": created_by,
        "involved_user_ids": involved_user_ids
    }

    res = requests.post(f"{BASE_URL}/groups/{group_id}/expenses", json=payload)
    time.sleep(0.1)

# STEP 5: Call settle-up
print("Calling settle-up...")
res = requests.get(f"{BASE_URL}/groups/{group_id}/settle-up")
transactions = res.json()
print(f"\nSettlement for Group {group_id}:")
for t in transactions:
    print(f"{t['from']} → {t['to']}: £{t['amount']}")
