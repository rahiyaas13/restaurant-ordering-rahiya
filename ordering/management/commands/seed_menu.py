from decimal import Decimal

from django.core.management.base import BaseCommand

from ordering.models import Category, MenuItem

CATEGORIES = [
    ("Appetizers",        "bi-fire",           1),
    ("Indian Mains",      "bi-egg-fried",      2),
    ("Indian Breads",     "bi-layers",         3),
    ("Italian",           "bi-gem",            4),
    ("Chinese",           "bi-bowl",           5),
    ("Mexican",           "bi-brilliance",     6),
    ("Burgers & Grills",  "bi-cup-hot",        7),
    ("Desserts",          "bi-cake2",          8),
    ("Beverages",         "bi-cup-straw",      9),
]

BASE = "https://images.unsplash.com/photo-"
Q    = "?w=600&q=80&auto=format&fit=crop"

def img(photo_id):
    return f"{BASE}{photo_id}{Q}"

# (category, name, description, price_INR, vegetarian, available, image_url)
ITEMS = [
    # ── Appetizers ────────────────────────────────────────────────────────────
    ("Appetizers", "Paneer Tikka",
     "Cottage cheese cubes marinated in spiced yogurt, charred in the tandoor.",
     "260", True,  True,
     img("1599487488170-d11ec9c172f0")),

    ("Appetizers", "Hara Bhara Kebab",
     "Spinach, peas and potato patties served with mint chutney.",
     "220", True,  True,
     img("1606491956689-2ea866880c84")),

    ("Appetizers", "Veg Spring Rolls",
     "Crisp rolls stuffed with seasoned vegetables, served with chilli sauce.",
     "180", True,  True,
     img("1564834744159-ff0ea41ba4b9")),

    ("Appetizers", "Chicken 65",
     "Spicy deep-fried Hyderabadi-style chicken with curry leaves and yogurt.",
     "280", False, True,
     img("1567188040759-fb8a883dc6d6")),

    ("Appetizers", "Fish Amritsari",
     "Gram-flour battered fish with ajwain and lemon, fried crisp.",
     "340", False, True,
     img("1580822184713-fc5400e7fe10")),

    ("Appetizers", "Stuffed Mushrooms",
     "Button mushrooms filled with herbed cream cheese, baked golden.",
     "240", True,  True,
     img("1552525934-4749c7ff3e74")),

    ("Appetizers", "Seekh Kebab",
     "Minced lamb and herbs grilled on skewers, served with raita.",
     "320", False, True,
     img("1529006557810-274b9b2fc783")),

    ("Appetizers", "Nachos with Salsa",
     "Tortilla chips topped with pico de gallo, jalapeños and sour cream.",
     "210", True,  True,
     img("1513456852971-30c0b8199d4d")),

    # ── Indian Mains ──────────────────────────────────────────────────────────
    ("Indian Mains", "Hyderabadi Chicken Biryani",
     "Dum-cooked basmati layered with marinated chicken, served with raita.",
     "360", False, True,
     img("1563379091339-03b21ab4a4f8")),

    ("Indian Mains", "Veg Dum Biryani",
     "Fragrant basmati with seasonal vegetables and saffron.",
     "290", True,  True,
     img("1596797038530-2c107229654b")),

    ("Indian Mains", "Butter Chicken",
     "Tandoori chicken in a silky tomato-butter gravy.",
     "380", False, True,
     img("1603894584373-5ac82b2ae398")),

    ("Indian Mains", "Paneer Butter Masala",
     "Paneer cubes in a rich tomato and cashew gravy.",
     "320", True,  True,
     img("1631452180519-c014fe946bc7")),

    ("Indian Mains", "Dal Makhani",
     "Black lentils slow-cooked overnight with cream and butter.",
     "260", True,  True,
     img("1546833998-877b37c2e5c6")),

    ("Indian Mains", "Lamb Rogan Josh",
     "Kashmiri-style lamb curry with aromatic whole spices.",
     "450", False, True,
     img("1585937421612-70a008356fbe")),

    ("Indian Mains", "Kadai Chicken",
     "Chicken cooked with capsicum and onion in a spiced tomato base.",
     "370", False, True,
     img("1565557623262-b51c2513a641")),

    ("Indian Mains", "Palak Paneer",
     "Cottage cheese in a smooth spiced spinach gravy.",
     "300", True,  True,
     img("1601050690597-df0568f70950")),

    ("Indian Mains", "Mutton Keema",
     "Minced mutton cooked with peas, tomatoes and whole spices.",
     "420", False, True,
     img("1574894709920-11b28e7367e3")),

    ("Indian Mains", "Prawn Masala",
     "Tiger prawns in a Konkan-style coconut and tomato masala.",
     "480", False, True,
     img("1551504734-5da7e163b1db")),

    ("Indian Mains", "Chole Bhature",
     "Spiced chickpea curry with fluffy deep-fried bread (2 pcs).",
     "220", True,  True,
     img("1626132647523-66c3d2e0ae7c")),

    ("Indian Mains", "Aloo Gobi",
     "Potato and cauliflower stir-fried with turmeric and cumin.",
     "200", True,  True,
     img("1645177628172-a788aa698ce4")),

    # ── Indian Breads ─────────────────────────────────────────────────────────
    ("Indian Breads", "Garlic Naan",
     "Tandoor-baked bread brushed with garlic butter.",
     "60",  True,  True,
     img("1619221882207-a93be3ef5cc5")),

    ("Indian Breads", "Butter Naan",
     "Classic naan brushed generously with butter.",
     "50",  True,  True,
     img("1600628421050-b3a8cda4c5f5")),

    ("Indian Breads", "Tandoori Roti",
     "Whole-wheat bread baked directly in the tandoor.",
     "35",  True,  True,
     img("1606168094192-10ed07adaebe")),

    ("Indian Breads", "Laccha Paratha",
     "Multi-layered flaky whole-wheat bread.",
     "55",  True,  True,
     img("1589301760014-d929f3979dbc")),

    ("Indian Breads", "Stuffed Aloo Paratha",
     "Whole-wheat flatbread stuffed with spiced mashed potatoes, served with butter and pickle.",
     "90",  True,  True,
     img("1612929633738-8fe44f7ec841")),

    # ── Italian ───────────────────────────────────────────────────────────────
    ("Italian", "Margherita Pizza",
     "San Marzano tomato, fresh mozzarella and basil on a thin crust.",
     "380", True,  True,
     img("1565299624946-b28f40a0ae38")),

    ("Italian", "Pepperoni Pizza",
     "Classic tomato base with spicy pepperoni and mozzarella.",
     "460", False, True,
     img("1628840042759-164aac28b09b")),

    ("Italian", "Pasta Arrabiata",
     "Penne in a fiery tomato-garlic-chilli sauce, topped with parmesan.",
     "320", True,  True,
     img("1621996346565-e3dbc646d9a9")),

    ("Italian", "Chicken Alfredo",
     "Fettuccine in a creamy parmesan-butter sauce with grilled chicken.",
     "420", False, True,
     img("1555949258-eb67b1ef0ceb")),

    ("Italian", "Penne Pesto",
     "Penne tossed with basil pesto, cherry tomatoes and pine nuts.",
     "350", True,  True,
     img("1473093226795-af9932fe5856")),

    ("Italian", "Mushroom Risotto",
     "Arborio rice cooked with porcini mushrooms, white wine and parmesan.",
     "390", True,  True,
     img("1476124369491-e7addf5db371")),

    ("Italian", "Bruschetta",
     "Toasted sourdough with diced tomatoes, garlic, basil and olive oil.",
     "180", True,  True,
     img("1572695157366-5e585ab2b69f")),

    ("Italian", "Tiramisu",
     "Classic Italian dessert with espresso-soaked ladyfingers and mascarpone.",
     "220", True,  True,
     img("1571877227200-a0d98ea607e9")),

    # ── Chinese ───────────────────────────────────────────────────────────────
    ("Chinese", "Veg Manchurian",
     "Crispy vegetable dumplings in a tangy manchurian sauce.",
     "220", True,  True,
     img("1563245372-f21724e3856d")),

    ("Chinese", "Chicken Manchurian",
     "Fried chicken in a spiced soy-ginger-garlic manchurian gravy.",
     "280", False, True,
     img("1569050467447-ce54b3bbc37d")),

    ("Chinese", "Hakka Noodles (Veg)",
     "Stir-fried noodles with vegetables in soy and chilli sauce.",
     "200", True,  True,
     img("1612929633738-8fe44f7ec841")),

    ("Chinese", "Chicken Hakka Noodles",
     "Stir-fried noodles with shredded chicken and veggies.",
     "250", False, True,
     img("1569050467447-ce54b3bbc37d")),

    ("Chinese", "Fried Rice (Veg)",
     "Wok-tossed rice with vegetables, soy sauce and sesame oil.",
     "190", True,  True,
     img("1603133872878-684f208fb84b")),

    ("Chinese", "Chilli Chicken (Dry)",
     "Crispy chicken tossed with capsicum, onion and chilli.",
     "300", False, True,
     img("1567188040759-fb8a883dc6d6")),

    ("Chinese", "Hot & Sour Soup",
     "Classic thick soup with vegetables, tofu and a tangy finish.",
     "150", True,  True,
     img("1547592166-23ac45744acd")),

    ("Chinese", "Dim Sum Platter (6 pcs)",
     "Steamed dumplings filled with vegetables and ginger.",
     "260", True,  True,
     img("1563245372-f21724e3856d")),

    # ── Mexican ───────────────────────────────────────────────────────────────
    ("Mexican", "Chicken Tacos (2 pcs)",
     "Soft tortillas with grilled chicken, pico de gallo, avocado and lime crema.",
     "280", False, True,
     img("1565299507177-b0ac66763828")),

    ("Mexican", "Veg Tacos (2 pcs)",
     "Soft tortillas with black beans, corn salsa, guacamole and jalapeños.",
     "240", True,  True,
     img("1565299507177-b0ac66763828")),

    ("Mexican", "Chicken Burrito",
     "Flour tortilla stuffed with grilled chicken, rice, beans, cheese and salsa.",
     "340", False, True,
     img("1626700051175-6818013e1d4f")),

    ("Mexican", "Veg Quesadilla",
     "Grilled flour tortilla filled with cheese, peppers and mushrooms.",
     "260", True,  True,
     img("1618040996337-56904b7850b9")),

    ("Mexican", "Nachos Grande",
     "Loaded tortilla chips with melted cheese, jalapeños, guacamole and sour cream.",
     "310", True,  True,
     img("1513456852971-30c0b8199d4d")),

    ("Mexican", "Churros with Dipping Sauce",
     "Fried dough sticks dusted with cinnamon sugar, served with chocolate sauce.",
     "180", True,  True,
     img("1484723091739-30a097e8f929")),

    # ── Burgers & Grills ──────────────────────────────────────────────────────
    ("Burgers & Grills", "Classic Beef Burger",
     "Juicy beef patty with lettuce, tomato, pickles and special sauce in a brioche bun.",
     "380", False, True,
     img("1568901346375-23c9450c58cd")),

    ("Burgers & Grills", "Crispy Chicken Burger",
     "Fried chicken fillet with coleslaw, cheese and sriracha mayo.",
     "350", False, True,
     img("1606755962773-d324e0a13086")),

    ("Burgers & Grills", "Veg Burger",
     "Grilled vegetable and bean patty with lettuce, tomato and garlic mayo.",
     "280", True,  True,
     img("1550547660-d9450f859349")),

    ("Burgers & Grills", "BBQ Pork Ribs",
     "Slow-cooked pork ribs glazed with smoky BBQ sauce, served with fries.",
     "650", False, True,
     img("1544025162-d76594e48c7f")),

    ("Burgers & Grills", "Grilled Chicken Steak",
     "200g chicken breast marinated and grilled, served with mashed potato and veggies.",
     "460", False, True,
     img("1532550907401-a500c9a57435")),

    ("Burgers & Grills", "Paneer Tikka Burger",
     "Tandoori paneer patty with mint chutney, onion and cheese in a bun.",
     "300", True,  True,
     img("1550547660-d9450f859349")),

    ("Burgers & Grills", "Fish & Chips",
     "Beer-battered fish fillet with crispy fries, tartar sauce and lemon.",
     "420", False, True,
     img("1579208570378-8c970854bc23")),

    # ── Desserts ──────────────────────────────────────────────────────────────
    ("Desserts", "Gulab Jamun",
     "Warm milk-solid dumplings in rose-cardamom syrup (2 pcs).",
     "120", True,  True,
     img("1666195006638-6d6d1b5bab9c")),

    ("Desserts", "Rasmalai",
     "Soft cheese discs soaked in chilled saffron milk.",
     "150", True,  True,
     img("1574701148559-4bdb1a7dab78")),

    ("Desserts", "Double Ka Meetha",
     "Hyderabadi bread pudding with dry fruits and rabri.",
     "140", True,  True,
     img("1586985289688-ca3cf47d3e6e")),

    ("Desserts", "Kulfi Falooda",
     "Pistachio kulfi with vermicelli, basil seeds and rose syrup.",
     "160", True,  True,
     img("1590080875897-c9a6cf4d36d8")),

    ("Desserts", "Chocolate Lava Cake",
     "Warm chocolate cake with a molten centre, served with vanilla ice cream.",
     "220", True,  True,
     img("1563805042-7684c019e1cb")),

    ("Desserts", "New York Cheesecake",
     "Dense and creamy cheesecake on a buttery graham-cracker crust.",
     "240", True,  True,
     img("1533134242443-d4fd215305ad")),

    ("Desserts", "Waffle with Ice Cream",
     "Belgian waffle topped with two scoops of ice cream and berry compote.",
     "200", True,  True,
     img("1568051243851-f9b136146e97")),

    ("Desserts", "Mango Sorbet",
     "Refreshing Alphonso mango sorbet (2 scoops).",
     "130", True,  True,
     img("1590080875897-c9a6cf4d36d8")),

    # ── Beverages ─────────────────────────────────────────────────────────────
    ("Beverages", "Masala Chai",
     "Ginger-cardamom tea brewed with full-cream milk.",
     "50",  True,  True,
     img("1544787219-7f47ccb76574")),

    ("Beverages", "Filter Coffee",
     "South Indian decoction coffee with frothed milk.",
     "70",  True,  True,
     img("1461023058943-07fcbe16d735")),

    ("Beverages", "Fresh Lime Soda",
     "Sweet, salted or mixed — your choice.",
     "80",  True,  True,
     img("1621263764928-df1444c5e859")),

    ("Beverages", "Mango Lassi",
     "Thick yogurt shake blended with Alphonso mango pulp.",
     "110", True,  True,
     img("1571091718767-18b5b1457add")),

    ("Beverages", "Cold Coffee",
     "Chilled coffee blended with ice cream and milk.",
     "130", True,  True,
     img("1461023058943-07fcbe16d735")),

    ("Beverages", "Fresh Orange Juice",
     "Freshly squeezed oranges, served chilled.",
     "120", True,  True,
     img("1589733955941-5eeaf752f6dd")),

    ("Beverages", "Watermelon Cooler",
     "Blended watermelon with mint and a squeeze of lime.",
     "100", True,  True,
     img("1490474418585-ba9bad8fd0ea")),

    ("Beverages", "Classic Mojito (Virgin)",
     "Mint, lime, sugar and sparkling water.",
     "140", True,  True,
     img("1514362545857-3bc16c4c7d1b")),

    ("Beverages", "Blue Lagoon",
     "Blue curacao syrup, lemonade and lime — non-alcoholic.",
     "150", True,  True,
     img("1553361371-9b22f78e8b1d")),

    ("Beverages", "Hot Chocolate",
     "Rich Belgian cocoa with steamed milk and whipped cream.",
     "140", True,  True,
     img("1542990253-0d0f5be5f0eb")),

    ("Beverages", "Diet Coke",
     "Chilled diet coke with lime.",
     "120", True,  True,
     img("1554866585-cd94860890b7")),
]


class Command(BaseCommand):
    help = "Load full Indian + International menu with photos (safe to run repeatedly)."

    def handle(self, *args, **options):
        # Upsert categories
        cats = {}
        for name, icon, order in CATEGORIES:
            cats[name], _ = Category.objects.get_or_create(
                name=name,
                defaults={"icon": icon, "display_order": order},
            )

        created = updated = 0
        for cat, name, desc, price, veg, available, image_url in ITEMS:
            obj, was_created = MenuItem.objects.update_or_create(
                category=cats[cat],
                name=name,
                defaults={
                    "description": desc,
                    "price": Decimal(price),
                    "is_vegetarian": veg,
                    "is_available": available,
                    "image_url": image_url,
                },
            )
            if was_created:
                created += 1
            else:
                updated += 1

        self.stdout.write(self.style.SUCCESS(
            f"Menu ready: {created} new, {updated} updated with photos."
        ))
        self.stdout.write(
            f"Total categories: {len(CATEGORIES)} | Total items: {len(ITEMS)}"
        )
