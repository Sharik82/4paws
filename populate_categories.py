from app import create_app, db
from app.models import Product, Category

app = create_app()

with app.app_context():
    db.create_all()
    existing = {c.slug: c for c in Category.query.all()}
    for product in Product.query.all():
        slug = (product.sub_category or product.main_category or '').strip()
        if not slug:
            continue
        if slug not in existing:
            cat = Category(name=slug.replace('_', ' ').title(), slug=slug)
            db.session.add(cat)
            db.session.flush()
            existing[slug] = cat
        product.category_id = existing[slug].id
    db.session.commit()
    print(f'Created/linked {len(existing)} categories.')

