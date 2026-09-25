from pathlib import Path
from getpass import getpass

import psycopg2


# ============================================================
# PATH
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data" / "raw"


# ============================================================
# POSTGRESQL CONFIG
# ============================================================

DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "smartbank360"
DB_USER = "postgres"

DB_PASSWORD = getpass(
    "Nhap mat khau PostgreSQL: "
)


# ============================================================
# TABLE CONFIG
# ============================================================

TABLES = [
    {
        "name": "branches",
        "file": "branches.csv",
        "columns": """
            branch_id,
            branch_name,
            province,
            region,
            open_date
        """,
        "expected": 50
    },

    {
        "name": "customers",
        "file": "customers.csv",
        "columns": """
            customer_id,
            full_name,
            gender,
            date_of_birth,
            province,
            occupation,
            monthly_income,
            join_date,
            customer_segment
        """,
        "expected": 10000
    },

    {
        "name": "accounts",
        "file": "accounts.csv",
        "columns": """
            account_id,
            customer_id,
            branch_id,
            account_type,
            open_date,
            current_balance,
            account_status
        """,
        "expected": 15000
    },

    {
        "name": "transactions",
        "file": "transactions.csv",
        "columns": """
            transaction_id,
            account_id,
            transaction_time,
            transaction_type,
            transaction_channel,
            amount,
            transaction_status,
            merchant_category
        """,
        "expected": 300000
    },

    {
        "name": "loans",
        "file": "loans.csv",
        "columns": """
            loan_id,
            customer_id,
            branch_id,
            loan_type,
            loan_amount,
            interest_rate,
            loan_start_date,
            loan_term_months,
            outstanding_balance,
            payment_status,
            risk_level
        """,
        "expected": 4000
    }
]


# ============================================================
# CONNECT
# ============================================================

print("=" * 60)
print("SMARTBANK 360 - POSTGRESQL IMPORT")
print("=" * 60)

conn = psycopg2.connect(
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD
)

cursor = conn.cursor()

print("\nKet noi PostgreSQL thanh cong.")


# ============================================================
# CHECK DATABASE IS EMPTY
# ============================================================

print("\nKiem tra database...")

has_data = False

for table in TABLES:

    table_name = table["name"]

    cursor.execute(
        f"SELECT COUNT(*) FROM {table_name};"
    )

    count = cursor.fetchone()[0]

    print(
        f"{table_name:<15}: {count:,}"
    )

    if count > 0:
        has_data = True


if has_data:

    print("\nDatabase da co du lieu.")
    print(
        "Dung import de tranh tao ban ghi trung."
    )

    cursor.close()
    conn.close()

    raise SystemExit


# ============================================================
# IMPORT
# ============================================================

try:

    for table in TABLES:

        table_name = table["name"]
        filename = table["file"]
        columns = table["columns"]

        file_path = (
            DATA_DIR / filename
        )

        if not file_path.exists():

            raise FileNotFoundError(
                f"Khong tim thay: {file_path}"
            )

        print(
            f"\nImport {filename} "
            f"-> {table_name} ..."
        )

        sql = f"""
            COPY {table_name}
            (
                {columns}
            )
            FROM STDIN
            WITH
            (
                FORMAT CSV,
                HEADER TRUE
            );
        """

        with open(
            file_path,
            "r",
            encoding="utf-8-sig",
            newline=""
        ) as csv_file:

            cursor.copy_expert(
                sql,
                csv_file
            )

        print("OK")

    conn.commit()

except Exception as error:

    conn.rollback()

    print("\nIMPORT BI LOI!")
    print(error)

    cursor.close()
    conn.close()

    raise


# ============================================================
# VERIFY
# ============================================================

print("\n")
print("=" * 60)
print("KIEM TRA KET QUA")
print("=" * 60)

all_ok = True

for table in TABLES:

    table_name = table["name"]
    expected = table["expected"]

    cursor.execute(
        f"SELECT COUNT(*) FROM {table_name};"
    )

    actual = cursor.fetchone()[0]

    status = (
        "OK"
        if actual == expected
        else "SAI"
    )

    if actual != expected:
        all_ok = False

    print(
        f"{table_name:<15}"
        f"{actual:>12,}"
        f" / "
        f"{expected:>12,}"
        f"   [{status}]"
    )


# ============================================================
# TOTAL
# ============================================================

cursor.execute("""
    SELECT
        (SELECT COUNT(*) FROM branches)
        +
        (SELECT COUNT(*) FROM customers)
        +
        (SELECT COUNT(*) FROM accounts)
        +
        (SELECT COUNT(*) FROM transactions)
        +
        (SELECT COUNT(*) FROM loans);
""")

total = cursor.fetchone()[0]

print("-" * 60)
print(
    f"TOTAL RECORDS: {total:,}"
)

if all_ok:

    print(
        "\nIMPORT SMARTBANK 360 THANH CONG!"
    )

else:

    print(
        "\nCo bang can kiem tra lai."
    )


cursor.close()
conn.close()