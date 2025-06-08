import json

def generate_book_sql(book):
    def sql_escape(value):
        if value is None or value == "N/A":
            return "NULL"
        return "N'" + value.replace("'", "''") + "'"

    def get_number(value, default="NULL"):
        try:
            return float(value.replace("₼", "").strip())
        except:
            return default

    title = sql_escape(book.get("Title"))
    code = book.get("Kod", "")
    author = book.get("Author", "")
    publisher = sql_escape(book.get("Nəşriyyat", ""))
    category = book.get("Category", "")
    subcategory = book.get("Subcategory", "")
    description = sql_escape(book.get("Description", ""))

    price = get_number(book.get("Price"))
    discount = get_number(book.get("Discount", "").replace("%", ""), default="NULL") if book.get("Discount") else "NULL"
    image = sql_escape(book.get("Image URL", ""))
    cover = sql_escape(book.get("Cild", ""))
    language = sql_escape(book.get("Dil", ""))
    page_count = book.get("Səhifə sayı", "0")
    age = book.get("Yaş", "").replace("+", "").strip() if book.get("Yaş") else "NULL"
    rate = book.get("Rating", "N/A")
    rate = float(rate) if rate != "N/A" else 5
    stock_status = 1  # Or random if needed

    sql = f"""INSERT INTO BOOKS 
([Title],
[UniqueCode],
[AuthorId],
[CategoryId],
[CategoryCode],
[Description],
[Price],
[DiscountPercentage],
[ImageSource],
[Cover],
[Language],
[PageCount],
[Age],
[Rate],
[StockStatus],
[CreatedDate],
[Publisher])
VALUES
({title},
'{code}',
(SELECT ID FROM AUTHORS WHERE FULLNAME = '{author.replace("'", "''")}'),
(SELECT ID FROM CATEGORIES WHERE NAME = '{subcategory}' AND PARENTCATEGORYCODE = (SELECT CODE FROM CATEGORIES WHERE NAME = N'{category}')),
(SELECT CODE FROM CATEGORIES WHERE NAME = '{subcategory}' AND PARENTCATEGORYCODE = (SELECT CODE FROM CATEGORIES WHERE NAME = N'{category}')),
{description},
{price if price != 'N/A' else 'NULL'},
{discount},
{image},
{cover},
{language},
{page_count},
{age},
{rate},
{stock_status},
GETDATE(),
{publisher});"""
    return sql

# Load JSON file with books
with open("libraff_books.json", "r", encoding="utf-8") as f:
    books = json.load(f)

# Generate SQL and write to file
with open("insert_books.sql", "w", encoding="utf-8") as f:
    for book in books:
        sql = generate_book_sql(book)
        f.write(sql + "\n\n")

print("✅ SQL statements saved to insert_books.sql")
