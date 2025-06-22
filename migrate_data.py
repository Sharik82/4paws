from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker
import os

# 🔵 Старе SQLite підключення (шлях до products.db)
sqlite_engine = create_engine('sqlite:///products.db')

# 🟣 Нове PostgreSQL підключення (онови URI якщо треба)
postgres_engine = create_engine('postgresql://denis@localhost/4paws_db')

# Сесії
SQLiteSession = sessionmaker(bind=sqlite_engine)
PostgresSession = sessionmaker(bind=postgres_engine)

sqlite_session = SQLiteSession()
postgres_session = PostgresSession()

# Завантаження таблиці product з SQLite
sqlite_meta = MetaData(bind=sqlite_engine)
sqlite_meta.reflect()
product_table = Table('product', sqlite_meta, autoload_with=sqlite_engine)

# Завантаження структури у PostgreSQL
postgres_meta = MetaData(bind=postgres_engine)
postgres_meta.reflect()

# Перевірка, чи таблиця існує у PostgreSQL
if 'product' not in postgres_meta.tables:
    print("Таблиця 'product' не знайдена у PostgreSQL. Спочатку виконай міграції.")
    exit()

# Отримуємо всі записи з SQLite
products = sqlite_session.execute(product_table.select()).fetchall()

# Вставляємо у PostgreSQL
product_pg = postgres_meta.tables['product']
for row in products:
    insert_stmt = product_pg.insert().values(**dict(row))
    postgres_session.execute(insert_stmt)

postgres_session.commit()
print(f"✅ Перенесено {len(products)} товарів у PostgreSQL")

# Закриваємо сесії
sqlite_session.close()
postgres_session.close()
