import os
import random
from datetime import datetime, timedelta

import pandas as pd


# ============================================================
# CẤU HÌNH
# ============================================================

random.seed(42)

NUM_BRANCHES = 50

OUTPUT_DIR = "../data/raw"

os.makedirs(OUTPUT_DIR, exist_ok=True)


# ============================================================
# DANH SÁCH TỈNH/THÀNH VÀ KHU VỰC
# ============================================================

province_region = {
    "Ha Noi": "North",
    "Hai Phong": "North",
    "Quang Ninh": "North",
    "Bac Ninh": "North",
    "Nam Dinh": "North",

    "Da Nang": "Central",
    "Hue": "Central",
    "Thanh Hoa": "Central",
    "Nghe An": "Central",
    "Khanh Hoa": "Central",

    "Ho Chi Minh City": "South",
    "Can Tho": "South",
    "Dong Nai": "South",
    "Binh Duong": "South",
    "Ba Ria - Vung Tau": "South"
}

provinces = list(province_region.keys())


# ============================================================
# HÀM TẠO NGÀY NGẪU NHIÊN
# ============================================================

def random_date(start_date, end_date):
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    return start_date + timedelta(days=random_days)


# ============================================================
# TẠO 50 CHI NHÁNH
# ============================================================

branches = []

for i in range(1, NUM_BRANCHES + 1):

    province = random.choice(provinces)

    region = province_region[province]

    open_date = random_date(
        datetime(2000, 1, 1),
        datetime(2022, 12, 31)
    ).date()

    branches.append({
        "branch_id": f"BR{i:03d}",
        "branch_name": f"SmartBank {province} Branch {i:02d}",
        "province": province,
        "region": region,
        "open_date": open_date
    })


# ============================================================
# CHUYỂN THÀNH DATAFRAME
# ============================================================

df_branches = pd.DataFrame(branches)


# ============================================================
# LƯU CSV
# ============================================================

file_path = f"{OUTPUT_DIR}/branches.csv"

df_branches.to_csv(
    file_path,
    index=False,
    encoding="utf-8-sig"
)

# ============================================================
# 2. CREATE CUSTOMERS
# ============================================================

from faker import Faker
import numpy as np

fake = Faker("vi_VN")
Faker.seed(42)
np.random.seed(42)

NUM_CUSTOMERS = 10_000

occupations = [
    "Office Staff",
    "Engineer",
    "Teacher",
    "Doctor",
    "Business Owner",
    "Sales",
    "Accountant",
    "IT Specialist",
    "Government Employee",
    "Freelancer",
    "Bank Employee",
    "Student"
]

customer_segments = [
    "Mass",
    "Affluent",
    "Premium"
]

customers = []

today = datetime(2026, 9, 24)

for i in range(1, NUM_CUSTOMERS + 1):

    customer_id = f"C{i:05d}"

    # Giới tính
    gender = random.choices(
        ["Male", "Female", "Other"],
        weights=[49, 50, 1]
    )[0]

    # Tuổi tập trung chủ yếu 25-50
    age = int(
        np.clip(
            np.random.normal(36, 11),
            18,
            70
        )
    )

    date_of_birth = (
        today -
        timedelta(days=age * 365 + random.randint(0, 364))
    ).date()

    province = random.choice(provinces)

    occupation = random.choice(occupations)

    # Phân khúc khách hàng
    customer_segment = random.choices(
        customer_segments,
        weights=[70, 23, 7]
    )[0]

    # ========================================================
    # THU NHẬP PHỤ THUỘC PHÂN KHÚC
    # ========================================================

    if customer_segment == "Mass":

        monthly_income = np.random.lognormal(
            mean=np.log(12_000_000),
            sigma=0.35
        )

        monthly_income = max(
            4_000_000,
            min(monthly_income, 30_000_000)
        )

    elif customer_segment == "Affluent":

        monthly_income = np.random.lognormal(
            mean=np.log(35_000_000),
            sigma=0.30
        )

        monthly_income = max(
            20_000_000,
            min(monthly_income, 80_000_000)
        )

    else:

        monthly_income = np.random.lognormal(
            mean=np.log(100_000_000),
            sigma=0.40
        )

        monthly_income = max(
            60_000_000,
            min(monthly_income, 400_000_000)
        )

    # Ngày bắt đầu trở thành khách hàng
    join_date = random_date(
        datetime(2018, 1, 1),
        datetime(2026, 8, 31)
    ).date()

    customers.append({
        "customer_id": customer_id,
        "full_name": fake.name(),
        "gender": gender,
        "date_of_birth": date_of_birth,
        "province": province,
        "occupation": occupation,
        "monthly_income": round(monthly_income, 2),
        "join_date": join_date,
        "customer_segment": customer_segment
    })


# ============================================================
# CHUYỂN CUSTOMER DATA SANG DATAFRAME
# ============================================================

df_customers = pd.DataFrame(customers)


# ============================================================
# LƯU CUSTOMER CSV
# ============================================================

customer_file = f"{OUTPUT_DIR}/customers.csv"

df_customers.to_csv(
    customer_file,
    index=False,
    encoding="utf-8-sig"
)


# ============================================================
# KIỂM TRA KẾT QUẢ
# ============================================================

print("\n")
print("=" * 50)
print("SMARTBANK 360 - CUSTOMER DATA CREATED")
print("=" * 50)

print(f"Total customers: {len(df_customers):,}")

print("\nFirst 10 customers:")
print(df_customers.head(10))

print("\nCustomer segment:")
print(
    df_customers["customer_segment"]
    .value_counts()
)

print("\nAverage income by segment:")
print(
    df_customers
    .groupby("customer_segment")["monthly_income"]
    .mean()
    .round(0)
)

print("\nFile saved at:")
print(customer_file)
# ============================================================
# HIỂN THỊ KẾT QUẢ
# ============================================================

print("=" * 50)
print("SMARTBANK 360 - BRANCH DATA CREATED")
print("=" * 50)

print(f"Total branches: {len(df_branches)}")

print("\nFirst 10 rows:")
print(df_branches.head(10))

print("\nFile saved at:")
print(file_path)    
# ============================================================
# 3. CREATE ACCOUNTS
# ============================================================

NUM_ACCOUNTS = 15_000

accounts = []

# Danh sách customer_id
customer_ids = df_customers["customer_id"].tolist()

# ============================================================
# ĐẢM BẢO MỖI KHÁCH HÀNG CÓ ÍT NHẤT 1 TÀI KHOẢN
# ============================================================

account_customers = customer_ids.copy()

# 10.000 khách hàng đã có 10.000 tài khoản đầu tiên
# Tạo thêm 5.000 tài khoản cho một số khách hàng
remaining_accounts = NUM_ACCOUNTS - NUM_CUSTOMERS

extra_customers = random.choices(
    customer_ids,
    k=remaining_accounts
)

account_customers.extend(extra_customers)

# Trộn danh sách để tài khoản không theo thứ tự customer
random.shuffle(account_customers)


# ============================================================
# TẠO DICTIONARY ĐỂ TRA CUSTOMER NHANH
# ============================================================

customer_lookup = (
    df_customers
    .set_index("customer_id")
    .to_dict("index")
)


# ============================================================
# TẠO DANH SÁCH CHI NHÁNH THEO TỈNH
# ============================================================

branches_by_province = {}

for province in provinces:

    branch_ids = df_branches[
        df_branches["province"] == province
    ]["branch_id"].tolist()

    branches_by_province[province] = branch_ids


# ============================================================
# SINH ACCOUNT
# ============================================================

for i, customer_id in enumerate(account_customers, start=1):

    customer = customer_lookup[customer_id]

    province = customer["province"]
    customer_segment = customer["customer_segment"]
    customer_join_date = pd.to_datetime(
        customer["join_date"]
    )

    # --------------------------------------------------------
    # Chọn chi nhánh
    # Ưu tiên chi nhánh cùng tỉnh với khách hàng
    # --------------------------------------------------------

    available_branches = branches_by_province.get(
        province,
        []
    )

    if available_branches:
        branch_id = random.choice(
            available_branches
        )
    else:
        branch_id = random.choice(
            df_branches["branch_id"].tolist()
        )

    # --------------------------------------------------------
    # Loại tài khoản
    # --------------------------------------------------------

    account_type = random.choices(
        [
            "Savings",
            "Current",
            "Credit"
        ],
        weights=[
            55,
            35,
            10
        ]
    )[0]

    # --------------------------------------------------------
    # Ngày mở tài khoản
    # Không được trước ngày khách hàng gia nhập ngân hàng
    # --------------------------------------------------------

    open_date = random_date(
        customer_join_date,
        datetime(2026, 8, 31)
    ).date()

    # --------------------------------------------------------
    # Số dư phụ thuộc customer segment
    # --------------------------------------------------------

    if customer_segment == "Mass":

        balance = np.random.lognormal(
            mean=np.log(15_000_000),
            sigma=0.8
        )

        balance = max(
            100_000,
            min(balance, 200_000_000)
        )

    elif customer_segment == "Affluent":

        balance = np.random.lognormal(
            mean=np.log(80_000_000),
            sigma=0.7
        )

        balance = max(
            5_000_000,
            min(balance, 800_000_000)
        )

    else:

        balance = np.random.lognormal(
            mean=np.log(350_000_000),
            sigma=0.8
        )

        balance = max(
            30_000_000,
            min(balance, 5_000_000_000)
        )

    # --------------------------------------------------------
    # Trạng thái tài khoản
    # --------------------------------------------------------

    account_status = random.choices(
        [
            "Active",
            "Inactive",
            "Closed"
        ],
        weights=[
            88,
            8,
            4
        ]
    )[0]

    accounts.append({
        "account_id": f"A{i:06d}",
        "customer_id": customer_id,
        "branch_id": branch_id,
        "account_type": account_type,
        "open_date": open_date,
        "current_balance": round(balance, 2),
        "account_status": account_status
    })


# ============================================================
# CHUYỂN SANG DATAFRAME
# ============================================================

df_accounts = pd.DataFrame(accounts)


# ============================================================
# LƯU FILE CSV
# ============================================================

account_file = f"{OUTPUT_DIR}/accounts.csv"

df_accounts.to_csv(
    account_file,
    index=False,
    encoding="utf-8-sig"
)


# ============================================================
# KIỂM TRA KẾT QUẢ
# ============================================================

print("\n")
print("=" * 50)
print("SMARTBANK 360 - ACCOUNT DATA CREATED")
print("=" * 50)

print(
    f"Total accounts: "
    f"{len(df_accounts):,}"
)

print(
    f"Customers with accounts: "
    f"{df_accounts['customer_id'].nunique():,}"
)

print("\nFirst 10 accounts:")
print(
    df_accounts.head(10)
)

print("\nAccount types:")
print(
    df_accounts["account_type"]
    .value_counts()
)

print("\nAccount status:")
print(
    df_accounts["account_status"]
    .value_counts()
)

print("\nAverage balance by customer segment:")

temp_account_analysis = (
    df_accounts
    .merge(
        df_customers[
            [
                "customer_id",
                "customer_segment"
            ]
        ],
        on="customer_id",
        how="left"
    )
)

print(
    temp_account_analysis
    .groupby("customer_segment")[
        "current_balance"
    ]
    .mean()
    .round(0)
)

print("\nFile saved at:")
print(account_file)
# ============================================================
# 4. CREATE TRANSACTIONS
# ============================================================

NUM_TRANSACTIONS = 300_000

print("\n")
print("=" * 60)
print("SMARTBANK 360 - CREATING TRANSACTIONS...")
print("=" * 60)


# ============================================================
# GHÉP ACCOUNT VỚI THÔNG TIN CUSTOMER
# ============================================================

account_info = (
    df_accounts
    .merge(
        df_customers[
            [
                "customer_id",
                "date_of_birth",
                "customer_segment"
            ]
        ],
        on="customer_id",
        how="left"
    )
)

account_records = account_info.to_dict("records")


# ============================================================
# CHIA ACCOUNT THEO TRẠNG THÁI
# ============================================================

active_accounts = [
    x for x in account_records
    if x["account_status"] == "Active"
]

inactive_accounts = [
    x for x in account_records
    if x["account_status"] == "Inactive"
]

closed_accounts = [
    x for x in account_records
    if x["account_status"] == "Closed"
]


# ============================================================
# HÀM TẠO THỜI GIAN GIAO DỊCH
# ============================================================

TRANSACTION_END = datetime(
    2026, 8, 31, 23, 59, 59
)


def create_transaction_datetime(account_open_date):

    account_open_date = pd.to_datetime(
        account_open_date
    )

    # Chúng ta phân tích dữ liệu từ 2024 trở đi
    project_start = datetime(2024, 1, 1)

    start_date = max(
        account_open_date,
        project_start
    )

    # Nếu tài khoản mở rất muộn
    if start_date >= TRANSACTION_END:
        return TRANSACTION_END

    total_seconds = int(
        (TRANSACTION_END - start_date)
        .total_seconds()
    )

    # Beta distribution:
    # tạo nhiều giao dịch hơn ở giai đoạn gần hiện tại
    position = np.random.beta(
        2.0,
        1.4
    )

    random_seconds = int(
        total_seconds * position
    )

    transaction_time = (
        start_date +
        timedelta(seconds=random_seconds)
    )

    return transaction_time


# ============================================================
# HÀM CHỌN KÊNH GIAO DỊCH
# ============================================================

def choose_transaction_channel(
    transaction_type,
    age,
    transaction_year
):

    channels = [
        "Mobile Banking",
        "Internet Banking",
        "ATM",
        "POS",
        "Branch"
    ]

    # --------------------------------------------------------
    # Kênh phụ thuộc loại giao dịch
    # --------------------------------------------------------

    if transaction_type == "Transfer":

        weights = [
            45,     # Mobile
            25,     # Internet
            5,      # ATM
            0,      # POS
            25      # Branch
        ]

    elif transaction_type == "Deposit":

        weights = [
            8,
            2,
            30,
            0,
            60
        ]

    elif transaction_type == "Withdrawal":

        weights = [
            2,
            0,
            78,
            0,
            20
        ]

    else:  # Payment

        weights = [
            40,
            15,
            1,
            42,
            2
        ]

    weights = [float(x) for x in weights]

    # --------------------------------------------------------
    # Điều chỉnh theo độ tuổi
    # --------------------------------------------------------

    if age <= 35:

        # Người trẻ dùng digital banking nhiều hơn
        weights[0] *= 1.45
        weights[1] *= 1.15

        weights[4] *= 0.55

    elif age >= 51:

        # Khách lớn tuổi sử dụng ATM/Branch nhiều hơn
        weights[0] *= 0.60
        weights[2] *= 1.20
        weights[4] *= 1.50

    # --------------------------------------------------------
    # Digital Banking tăng theo thời gian
    # --------------------------------------------------------

    if transaction_year == 2025:

        weights[0] *= 1.10

    elif transaction_year == 2026:

        weights[0] *= 1.25
        weights[4] *= 0.90

    return random.choices(
        channels,
        weights=weights,
        k=1
    )[0]


# ============================================================
# HÀM TẠO SỐ TIỀN GIAO DỊCH
# ============================================================

def create_transaction_amount(
    transaction_type,
    customer_segment
):

    # --------------------------------------------------------
    # Giá trị cơ bản theo loại giao dịch
    # --------------------------------------------------------

    base_amount = {
        "Payment": 400_000,
        "Withdrawal": 1_500_000,
        "Deposit": 3_000_000,
        "Transfer": 2_000_000
    }

    base = base_amount[
        transaction_type
    ]

    # --------------------------------------------------------
    # Premium thường có giao dịch lớn hơn
    # --------------------------------------------------------

    segment_multiplier = {
        "Mass": 1.0,
        "Affluent": 2.5,
        "Premium": 6.0
    }

    median_amount = (
        base *
        segment_multiplier[
            customer_segment
        ]
    )

    amount = np.random.lognormal(
        mean=np.log(median_amount),
        sigma=0.9
    )

    # Không cho giá trị quá nhỏ/lớn bất thường
    amount = max(
        10_000,
        min(
            amount,
            2_000_000_000
        )
    )

    return round(amount, 2)


# ============================================================
# HÀM TRẠNG THÁI GIAO DỊCH
# ============================================================

def create_transaction_status(channel):

    # Success / Failed / Pending

    status_probabilities = {

        "Mobile Banking":
            [97, 2, 1],

        "Internet Banking":
            [96, 3, 1],

        "ATM":
            [94, 5, 1],

        "POS":
            [95, 4, 1],

        "Branch":
            [98.5, 1, 0.5]
    }

    return random.choices(
        [
            "Success",
            "Failed",
            "Pending"
        ],
        weights=status_probabilities[channel],
        k=1
    )[0]


# ============================================================
# MERCHANT CATEGORY
# ============================================================

merchant_categories = [
    "Groceries",
    "Shopping",
    "Food & Beverage",
    "Utilities",
    "Travel",
    "Healthcare",
    "Education",
    "Entertainment",
    "Insurance",
    "Telecommunication"
]


# ============================================================
# TẠO TRANSACTIONS
# ============================================================

transactions = []

today_for_age = datetime(
    2026,
    9,
    24
)


for i in range(
    1,
    NUM_TRANSACTIONS + 1
):

    # --------------------------------------------------------
    # Chọn account
    #
    # Phần lớn giao dịch đến từ Active Account
    # --------------------------------------------------------

    selected_status = random.choices(
        [
            "Active",
            "Inactive",
            "Closed"
        ],
        weights=[
            95,
            4,
            1
        ]
    )[0]

    if selected_status == "Active":

        account = random.choice(
            active_accounts
        )

    elif selected_status == "Inactive":

        account = random.choice(
            inactive_accounts
        )

    else:

        account = random.choice(
            closed_accounts
        )

    account_id = account[
        "account_id"
    ]

    customer_segment = account[
        "customer_segment"
    ]

    # --------------------------------------------------------
    # Tính tuổi
    # --------------------------------------------------------

    dob = pd.to_datetime(
        account["date_of_birth"]
    )

    age = int(
        (
            today_for_age - dob
        ).days / 365.25
    )

    # --------------------------------------------------------
    # Thời gian giao dịch
    # --------------------------------------------------------

    transaction_time = (
        create_transaction_datetime(
            account["open_date"]
        )
    )

    # --------------------------------------------------------
    # Loại giao dịch
    # --------------------------------------------------------

    transaction_type = (
        random.choices(
            [
                "Transfer",
                "Deposit",
                "Withdrawal",
                "Payment"
            ],
            weights=[
                42,
                13,
                15,
                30
            ]
        )[0]
    )

    # --------------------------------------------------------
    # Channel
    # --------------------------------------------------------

    transaction_channel = (
        choose_transaction_channel(
            transaction_type,
            age,
            transaction_time.year
        )
    )

    # --------------------------------------------------------
    # Amount
    # --------------------------------------------------------

    amount = create_transaction_amount(
        transaction_type,
        customer_segment
    )

    # --------------------------------------------------------
    # Status
    # --------------------------------------------------------

    transaction_status = (
        create_transaction_status(
            transaction_channel
        )
    )

    # --------------------------------------------------------
    # Merchant Category
    #
    # Chỉ Payment mới có merchant
    # --------------------------------------------------------

    if transaction_type == "Payment":

        merchant_category = (
            random.choice(
                merchant_categories
            )
        )

    else:

        merchant_category = None

    # --------------------------------------------------------
    # Append
    # --------------------------------------------------------

    transactions.append({

        "transaction_id":
            f"T{i:09d}",

        "account_id":
            account_id,

        "transaction_time":
            transaction_time,

        "transaction_type":
            transaction_type,

        "transaction_channel":
            transaction_channel,

        "amount":
            amount,

        "transaction_status":
            transaction_status,

        "merchant_category":
            merchant_category
    })

    # --------------------------------------------------------
    # Hiển thị tiến độ
    # --------------------------------------------------------

    if i % 50_000 == 0:

        print(
            f"Created "
            f"{i:,} / "
            f"{NUM_TRANSACTIONS:,} "
            f"transactions"
        )


# ============================================================
# DATAFRAME
# ============================================================

df_transactions = pd.DataFrame(
    transactions
)


# ============================================================
# SAVE CSV
# ============================================================

transaction_file = (
    f"{OUTPUT_DIR}/transactions.csv"
)

df_transactions.to_csv(
    transaction_file,
    index=False,
    encoding="utf-8-sig"
)


# ============================================================
# DATA QUALITY CHECK
# ============================================================

print("\n")
print("=" * 60)
print("SMARTBANK 360 - TRANSACTION DATA CREATED")
print("=" * 60)

print(
    f"Total transactions: "
    f"{len(df_transactions):,}"
)

print("\nFirst 5 transactions:")

print(
    df_transactions.head()
)


# ============================================================
# TRANSACTION TYPE
# ============================================================

print("\nTransaction type:")

print(
    df_transactions[
        "transaction_type"
    ]
    .value_counts()
)


# ============================================================
# CHANNEL
# ============================================================

print("\nTransaction channel:")

print(
    df_transactions[
        "transaction_channel"
    ]
    .value_counts()
)


# ============================================================
# STATUS
# ============================================================

print("\nTransaction status:")

print(
    df_transactions[
        "transaction_status"
    ]
    .value_counts()
)


# ============================================================
# SUCCESS RATE BY CHANNEL
# ============================================================

success_rate = (
    df_transactions
    .assign(
        is_success=
        df_transactions[
            "transaction_status"
        ].eq("Success")
    )
    .groupby(
        "transaction_channel"
    )["is_success"]
    .mean()
    .mul(100)
    .round(2)
)

print(
    "\nSuccess rate by channel (%):"
)

print(success_rate)


# ============================================================
# AVERAGE TRANSACTION BY CUSTOMER SEGMENT
# ============================================================

transaction_segment_analysis = (
    df_transactions
    .merge(
        df_accounts[
            [
                "account_id",
                "customer_id"
            ]
        ],
        on="account_id",
        how="left"
    )
    .merge(
        df_customers[
            [
                "customer_id",
                "customer_segment"
            ]
        ],
        on="customer_id",
        how="left"
    )
)

print(
    "\nAverage transaction amount "
    "by customer segment:"
)

print(
    transaction_segment_analysis
    .groupby(
        "customer_segment"
    )["amount"]
    .mean()
    .round(0)
)


# ============================================================
# TRANSACTIONS BY YEAR
# ============================================================

df_transactions[
    "transaction_year"
] = pd.to_datetime(
    df_transactions[
        "transaction_time"
    ]
).dt.year

print(
    "\nTransactions by year:"
)

print(
    df_transactions[
        "transaction_year"
    ]
    .value_counts()
    .sort_index()
)


# Xóa column dùng để kiểm tra
df_transactions.drop(
    columns=["transaction_year"],
    inplace=True
)


print("\nFile saved at:")
print(transaction_file)
# ============================================================
# 5. CREATE LOANS
# ============================================================

NUM_LOANS = 4_000

print("\n")
print("=" * 60)
print("SMARTBANK 360 - CREATING LOAN DATA...")
print("=" * 60)


# ============================================================
# CHỌN 4.000 KHÁCH HÀNG CÓ KHOẢN VAY
# Mỗi khách hàng hiện tại tối đa 1 khoản vay
# ============================================================

loan_customer_ids = random.sample(
    df_customers["customer_id"].tolist(),
    NUM_LOANS
)

loans = []


# ============================================================
# HÀM XÁC ĐỊNH LOAN TYPE
# ============================================================

def choose_loan_type(occupation):

    if occupation == "Business Owner":
        return random.choices(
            [
                "Business",
                "Mortgage",
                "Personal",
                "Auto"
            ],
            weights=[
                45,
                20,
                20,
                15
            ]
        )[0]

    elif occupation in [
        "Engineer",
        "Doctor",
        "IT Specialist",
        "Bank Employee"
    ]:
        return random.choices(
            [
                "Mortgage",
                "Personal",
                "Auto",
                "Business"
            ],
            weights=[
                35,
                30,
                25,
                10
            ]
        )[0]

    else:
        return random.choices(
            [
                "Mortgage",
                "Personal",
                "Auto",
                "Business"
            ],
            weights=[
                25,
                45,
                20,
                10
            ]
        )[0]


# ============================================================
# HÀM TẠO LOAN AMOUNT
# ============================================================

def create_loan_amount(
    loan_type,
    annual_income
):

    if loan_type == "Mortgage":

        multiplier = random.uniform(
            2.0,
            6.0
        )

    elif loan_type == "Business":

        multiplier = random.uniform(
            1.5,
            5.0
        )

    elif loan_type == "Auto":

        multiplier = random.uniform(
            0.5,
            2.0
        )

    else:  # Personal Loan

        multiplier = random.uniform(
            0.2,
            1.5
        )

    amount = (
        annual_income *
        multiplier
    )

    amount = max(
        10_000_000,
        min(
            amount,
            10_000_000_000
        )
    )

    return round(amount, 2)


# ============================================================
# HÀM XÁC ĐỊNH RỦI RO
# ============================================================

def determine_risk_level(
    loan_to_income,
    customer_segment
):

    # Loan lớn hơn nhiều so với thu nhập
    if loan_to_income >= 4.5:

        probabilities = [
            10,  # Low
            35,  # Medium
            55   # High
        ]

    elif loan_to_income >= 2.5:

        probabilities = [
            30,
            50,
            20
        ]

    else:

        probabilities = [
            70,
            25,
            5
        ]

    # Premium giảm nhẹ nguy cơ
    if customer_segment == "Premium":

        probabilities[0] += 10
        probabilities[2] -= 5

    # Mass tăng nhẹ nguy cơ
    elif customer_segment == "Mass":

        probabilities[0] -= 5
        probabilities[2] += 5

    # Đảm bảo không có probability âm
    probabilities = [
        max(0, x)
        for x in probabilities
    ]

    return random.choices(
        [
            "Low",
            "Medium",
            "High"
        ],
        weights=probabilities,
        k=1
    )[0]


# ============================================================
# PAYMENT STATUS PHỤ THUỘC RISK
# ============================================================

def determine_payment_status(
    risk_level
):

    if risk_level == "High":

        return random.choices(
            [
                "Current",
                "Late",
                "Default"
            ],
            weights=[
                45,
                35,
                20
            ]
        )[0]

    elif risk_level == "Medium":

        return random.choices(
            [
                "Current",
                "Late",
                "Default"
            ],
            weights=[
                78,
                18,
                4
            ]
        )[0]

    else:

        return random.choices(
            [
                "Current",
                "Late",
                "Default"
            ],
            weights=[
                95,
                4,
                1
            ]
        )[0]


# ============================================================
# TERM CỦA TỪNG LOẠI VAY
# ============================================================

loan_terms = {

    "Mortgage":
        [120, 180, 240, 300],

    "Personal":
        [12, 24, 36, 48, 60],

    "Auto":
        [36, 48, 60, 72],

    "Business":
        [12, 24, 36, 60, 84]
}


# ============================================================
# INTEREST RATE RANGE
# ============================================================

interest_rate_range = {

    "Mortgage":
        (5.5, 10.5),

    "Personal":
        (10.0, 18.0),

    "Auto":
        (7.0, 12.5),

    "Business":
        (7.5, 15.0)
}


# ============================================================
# TẠO LOANS
# ============================================================

for i, customer_id in enumerate(
    loan_customer_ids,
    start=1
):

    customer = customer_lookup[
        customer_id
    ]

    occupation = customer[
        "occupation"
    ]

    province = customer[
        "province"
    ]

    customer_segment = customer[
        "customer_segment"
    ]

    monthly_income = float(
        customer[
            "monthly_income"
        ]
    )

    annual_income = (
        monthly_income * 12
    )

    # --------------------------------------------------------
    # Branch cùng tỉnh khách hàng
    # --------------------------------------------------------

    available_branches = (
        branches_by_province.get(
            province,
            []
        )
    )

    if available_branches:

        branch_id = random.choice(
            available_branches
        )

    else:

        branch_id = random.choice(
            df_branches[
                "branch_id"
            ].tolist()
        )

    # --------------------------------------------------------
    # Loan Type
    # --------------------------------------------------------

    loan_type = choose_loan_type(
        occupation
    )

    # --------------------------------------------------------
    # Loan Amount
    # --------------------------------------------------------

    loan_amount = create_loan_amount(
        loan_type,
        annual_income
    )

    # --------------------------------------------------------
    # Loan-to-Income
    # --------------------------------------------------------

    loan_to_income = (
        loan_amount /
        annual_income
    )

    # --------------------------------------------------------
    # Interest Rate
    # --------------------------------------------------------

    min_rate, max_rate = (
        interest_rate_range[
            loan_type
        ]
    )

    interest_rate = round(
        random.uniform(
            min_rate,
            max_rate
        ),
        2
    )

    # --------------------------------------------------------
    # Loan Start Date
    # --------------------------------------------------------

    customer_join_date = (
        pd.to_datetime(
            customer[
                "join_date"
            ]
        )
    )

    earliest_loan_date = max(
        customer_join_date,
        datetime(2020, 1, 1)
    )

    loan_start_date = random_date(
        earliest_loan_date,
        datetime(2026, 8, 31)
    ).date()

    # --------------------------------------------------------
    # Loan Term
    # --------------------------------------------------------

    loan_term_months = (
        random.choice(
            loan_terms[
                loan_type
            ]
        )
    )

    # --------------------------------------------------------
    # Risk Level
    # --------------------------------------------------------

    risk_level = (
        determine_risk_level(
            loan_to_income,
            customer_segment
        )
    )

    # --------------------------------------------------------
    # Payment Status
    # --------------------------------------------------------

    payment_status = (
        determine_payment_status(
            risk_level
        )
    )

    # --------------------------------------------------------
    # OUTSTANDING BALANCE
    # --------------------------------------------------------

    # Default thường còn dư nợ nhiều
    if payment_status == "Default":

        paid_ratio = random.uniform(
            0.05,
            0.35
        )

    elif payment_status == "Late":

        paid_ratio = random.uniform(
            0.15,
            0.60
        )

    else:

        paid_ratio = random.uniform(
            0.20,
            0.90
        )

    outstanding_balance = (
        loan_amount *
        (1 - paid_ratio)
    )

    outstanding_balance = max(
        0,
        min(
            outstanding_balance,
            loan_amount
        )
    )

    # --------------------------------------------------------
    # ADD ROW
    # --------------------------------------------------------

    loans.append({

        "loan_id":
            f"L{i:06d}",

        "customer_id":
            customer_id,

        "branch_id":
            branch_id,

        "loan_type":
            loan_type,

        "loan_amount":
            loan_amount,

        "interest_rate":
            interest_rate,

        "loan_start_date":
            loan_start_date,

        "loan_term_months":
            loan_term_months,

        "outstanding_balance":
            round(
                outstanding_balance,
                2
            ),

        "payment_status":
            payment_status,

        "risk_level":
            risk_level
    })


# ============================================================
# DATAFRAME
# ============================================================

df_loans = pd.DataFrame(
    loans
)


# ============================================================
# SAVE CSV
# ============================================================

loan_file = (
    f"{OUTPUT_DIR}/loans.csv"
)

df_loans.to_csv(
    loan_file,
    index=False,
    encoding="utf-8-sig"
)


# ============================================================
# KIỂM TRA DATA
# ============================================================

print("\n")
print("=" * 60)
print("SMARTBANK 360 - LOAN DATA CREATED")
print("=" * 60)

print(
    f"Total loans: "
    f"{len(df_loans):,}"
)

print("\nFirst 5 loans:")

print(
    df_loans.head()
)


# ============================================================
# LOAN TYPE
# ============================================================

print("\nLoan type:")

print(
    df_loans[
        "loan_type"
    ]
    .value_counts()
)


# ============================================================
# RISK LEVEL
# ============================================================

print("\nRisk level:")

print(
    df_loans[
        "risk_level"
    ]
    .value_counts()
)


# ============================================================
# PAYMENT STATUS
# ============================================================

print("\nPayment status:")

print(
    df_loans[
        "payment_status"
    ]
    .value_counts()
)


# ============================================================
# DEFAULT RATE
# ============================================================

default_rate = (
    (
        df_loans[
            "payment_status"
        ]
        == "Default"
    )
    .mean()
    * 100
)

print(
    f"\nOverall default rate: "
    f"{default_rate:.2f}%"
)


# ============================================================
# DEFAULT RATE BY RISK
# ============================================================

loan_risk_analysis = (
    df_loans
    .assign(
        is_default=
        df_loans[
            "payment_status"
        ].eq("Default")
    )
    .groupby(
        "risk_level"
    )["is_default"]
    .mean()
    .mul(100)
    .round(2)
)

print(
    "\nDefault rate by risk level (%):"
)

print(
    loan_risk_analysis
)


# ============================================================
# AVERAGE LOAN AMOUNT BY TYPE
# ============================================================

print(
    "\nAverage loan amount by loan type:"
)

print(
    df_loans
    .groupby(
        "loan_type"
    )["loan_amount"]
    .mean()
    .round(0)
)


print("\nFile saved at:")
print(loan_file)