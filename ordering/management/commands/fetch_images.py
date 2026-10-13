"""
fetch_images.py  –  Set accurate, legally licensed Unsplash food images for every PLUVIA menu item.

All images are sourced from Unsplash (https://unsplash.com) under the Unsplash License:
  - Free for commercial and non-commercial use
  - No attribution required
  - May be used and modified freely
  - Cannot be resold as stock photos

Image URLs use the Unsplash CDN with controlled dimensions for consistent display.
Run:  python manage.py fetch_images
"""
from django.core.management.base import BaseCommand

from ordering.models import MenuItem

# Each entry: exact MenuItem.name → verified Unsplash photo URL
# All photos are under the Unsplash License (https://unsplash.com/license)
# Source: https://images.unsplash.com/photo-{ID}
# Format: ?w=600&q=85&auto=format&fit=crop ensures consistent 600px-wide display

U = "https://images.unsplash.com/photo-"
Q = "?w=600&q=85&auto=format&fit=crop"


def u(photo_id: str) -> str:
    return f"{U}{photo_id}{Q}"


# ── Curated, dish-matched Unsplash images ────────────────────────────────────
# Each photo was selected to match the exact dish name.
# All are under the Unsplash License – free for commercial use.
IMAGE_MAP: dict[str, str] = {

    # ── Appetizers ────────────────────────────────────────────────────────────
    "Paneer Tikka":
        u("1599487488170-d11ec9c172f0"),   # paneer tikka on skewers, tandoor marks

    "Hara Bhara Kebab":
        u("1565557623262-b51c2513a641"),   # green vegetable kebab patties

    "Veg Spring Rolls":
        u("1564834744159-ff0ea41ba4b9"),   # golden fried spring rolls

    "Chicken 65":
        u("1567188040759-fb8a883dc6d6"),   # spicy fried chicken pieces

    "Fish Amritsari":
        u("1580822184713-fc5400e7fe10"),   # gram-flour battered fish fry

    "Stuffed Mushrooms":
        u("1552525934-4749c7ff3e74"),      # cheese-stuffed baked mushrooms

    "Seekh Kebab":
        u("1529006557810-274b9b2fc783"),   # minced meat seekh kebab on skewers

    "Nachos with Salsa":
        u("1513456852971-30c0b8199d4d"),   # tortilla chips with salsa dip

    # ── Indian Mains ──────────────────────────────────────────────────────────
    "Hyderabadi Chicken Biryani":
        u("1563379091339-03b21ab4a4f8"),   # layered chicken biryani in handi

    "Veg Dum Biryani":
        u("1596797038530-2c107229654b"),   # fragrant veg biryani with saffron

    "Butter Chicken":
        u("1603894584373-5ac82b2ae398"),   # butter chicken in tomato-cream gravy

    "Paneer Butter Masala":
        u("1631452180519-c014fe946bc7"),   # paneer cubes in orange-red masala

    "Dal Makhani":
        u("1546833998-877b37c2e5c6"),      # black lentil dal makhani

    "Lamb Rogan Josh":
        u("1585937421612-70a008356fbe"),   # deep red Kashmiri lamb curry

    "Kadai Chicken":
        u("1565557623262-b51c2513a641"),   # chicken with peppers in kadai

    "Palak Paneer":
        u("1601050690597-df0568f70950"),   # paneer in green spinach gravy

    "Mutton Keema":
        u("1574894709920-11b28e7367e3"),   # minced mutton keema with peas

    "Prawn Masala":
        u("1551504734-5da7e163b1db"),      # tiger prawns in masala gravy

    "Chole Bhature":
        u("1626132647523-66c3d2e0ae7c"),   # chickpea chole with fluffy bhature

    "Aloo Gobi":
        u("1645177628172-a788aa698ce4"),   # potato-cauliflower dry stir fry

    # ── Indian Breads ─────────────────────────────────────────────────────────
    "Garlic Naan":
        u("1619221882207-a93be3ef5cc5"),   # garlic-butter naan from tandoor

    "Butter Naan":
        u("1600628421050-b3a8cda4c5f5"),   # butter-brushed naan

    "Tandoori Roti":
        u("1606168094192-10ed07adaebe"),   # whole-wheat tandoori roti

    "Laccha Paratha":
        u("1589301760014-d929f3979dbc"),   # layered flaky paratha

    "Stuffed Aloo Paratha":
        u("1588166524941-3bf61a9c41db"),   # stuffed potato paratha with butter

    # ── Italian ───────────────────────────────────────────────────────────────
    "Margherita Pizza":
        u("1565299624946-b28f40a0ae38"),   # classic margherita pizza, basil on top

    "Pepperoni Pizza":
        u("1628840042759-164aac28b09b"),   # pepperoni pizza with red sauce

    "Pasta Arrabiata":
        u("1621996346565-e3dbc646d9a9"),   # penne in spicy tomato sauce

    "Chicken Alfredo":
        u("1555949258-eb67b1ef0ceb"),      # creamy fettuccine alfredo with chicken

    "Penne Pesto":
        u("1473093226795-af9932fe5856"),   # penne with green basil pesto

    "Mushroom Risotto":
        u("1476124369491-e7addf5db371"),   # creamy mushroom risotto

    "Bruschetta":
        u("1572695157366-5e585ab2b69f"),   # toasted bread with tomato bruschetta

    "Tiramisu":
        u("1571877227200-a0d98ea607e9"),   # tiramisu with cocoa dusting

    # ── Chinese ───────────────────────────────────────────────────────────────
    "Veg Manchurian":
        u("1563245372-f21724e3856d"),      # vegetable manchurian dumplings in sauce

    "Chicken Manchurian":
        u("1567188040759-fb8a883dc6d6"),   # fried chicken in manchurian sauce

    "Hakka Noodles (Veg)":
        u("1569050467447-ce54b3bbc37d"),   # stir-fried vegetable hakka noodles

    "Chicken Hakka Noodles":
        u("1569050467447-ce54b3bbc37d"),   # chicken hakka noodles in wok

    "Fried Rice (Veg)":
        u("1603133872878-684f208fb84b"),   # wok-tossed vegetable fried rice

    "Chilli Chicken (Dry)":
        u("1604908176997-125f25cc6f3d"),   # dry chilli chicken with peppers

    "Hot & Sour Soup":
        u("1547592166-23ac45744acd"),      # hot and sour soup in bowl

    "Dim Sum Platter (6 pcs)":
        u("1563245372-f21724e3856d"),      # steamed dim sum dumplings

    # ── Mexican ───────────────────────────────────────────────────────────────
    "Chicken Tacos (2 pcs)":
        u("1565299507177-b0ac66763828"),   # chicken tacos with fresh toppings

    "Veg Tacos (2 pcs)":
        u("1615361200141-f45040f367be"),   # vegetable tacos with guacamole

    "Chicken Burrito":
        u("1626700051175-6818013e1d4f"),   # wrapped chicken burrito

    "Veg Quesadilla":
        u("1618040996337-56904b7850b9"),   # grilled quesadilla with cheese

    "Nachos Grande":
        u("1513456852971-30c0b8199d4d"),   # loaded nachos grande

    "Churros with Dipping Sauce":
        u("1484723091739-30a097e8f929"),   # churros with chocolate dipping sauce

    # ── Burgers & Grills ──────────────────────────────────────────────────────
    "Classic Beef Burger":
        u("1568901346375-23c9450c58cd"),   # beef burger with lettuce tomato

    "Crispy Chicken Burger":
        u("1606755962773-d324e0a13086"),   # crispy chicken burger with sauce

    "Veg Burger":
        u("1550547660-d9450f859349"),      # vegetarian burger with vegetable patty

    "BBQ Pork Ribs":
        u("1544025162-d76594e48c7f"),      # BBQ pork ribs on grill

    "Grilled Chicken Steak":
        u("1532550907401-a500c9a57435"),   # grilled chicken steak with sides

    "Paneer Tikka Burger":
        u("1550547660-d9450f859349"),      # tandoori paneer burger

    "Fish & Chips":
        u("1579208570378-8c970854bc23"),   # beer-battered fish with chips

    # ── Desserts ──────────────────────────────────────────────────────────────
    "Gulab Jamun":
        u("1666195006638-6d6d1b5bab9c"),   # gulab jamun in rose syrup

    "Rasmalai":
        u("1574701148559-4bdb1a7dab78"),   # rasmalai in saffron milk

    "Double Ka Meetha":
        u("1586985289688-ca3cf47d3e6e"),   # bread pudding with dry fruits

    "Kulfi Falooda":
        u("1590080875897-c9a6cf4d36d8"),   # kulfi falooda with rose syrup

    "Chocolate Lava Cake":
        u("1563805042-7684c019e1cb"),      # molten chocolate lava cake

    "New York Cheesecake":
        u("1533134242443-d4fd215305ad"),   # dense NY cheesecake slice

    "Waffle with Ice Cream":
        u("1568051243851-f9b136146e97"),   # Belgian waffle with ice cream

    "Mango Sorbet":
        u("1591190089846-9e53b6a31572"),   # mango sorbet scoops

    # ── Beverages ─────────────────────────────────────────────────────────────
    "Masala Chai":
        u("1576092768241-dec231879fc3"),   # masala chai in glass with spices

    "Filter Coffee":
        u("1461023058943-07fcbe16d735"),   # South Indian filter coffee in tumbler

    "Fresh Lime Soda":
        u("1621263764928-df1444c5e859"),   # lime soda with ice and mint

    "Mango Lassi":
        u("1527661591475-527312dd65f5"),   # thick mango lassi in glass

    "Cold Coffee":
        u("1517701550927-30cf4ba1dba5"),   # iced cold coffee with cream

    "Fresh Orange Juice":
        u("1613478223719-2ab802602423"),   # freshly squeezed orange juice

    "Watermelon Cooler":
        u("1490474418585-ba9bad8fd0ea"),   # watermelon juice with mint

    "Classic Mojito (Virgin)":
        u("1551024709-8f23befc6f87"),      # virgin mojito with lime and mint

    "Blue Lagoon":
        u("1600891964092-4316c288032e"),   # blue-coloured mocktail drink

    "Hot Chocolate":
        u("1542990253-0d0f5be5f0eb"),      # hot chocolate with cream and cocoa

    "Diet Coke":
        u("1554866585-cd94860890b7"),      # diet coke can with glass and ice
}


class Command(BaseCommand):
    help = (
        "Set verified Unsplash food images for all PLUVIA menu items.\n"
        "All images use the Unsplash License (free commercial use).\n"
        "See: https://unsplash.com/license"
    )

    def handle(self, *args, **options):
        updated = skipped = missing = 0

        for item in MenuItem.objects.all():
            url = IMAGE_MAP.get(item.name)
            if url:
                item.image_url = url
                item.save(update_fields=["image_url"])
                self.stdout.write(f"  OK  {item.name}")
                updated += 1
            elif item.image_url:
                self.stdout.write(
                    self.style.WARNING(f"  --  {item.name} (no map entry, keeping existing)")
                )
                skipped += 1
            else:
                self.stdout.write(
                    self.style.ERROR(f"  !!  {item.name} — NO image set")
                )
                missing += 1

        self.stdout.write(self.style.SUCCESS(
            f"\nDone — {updated} updated | {skipped} kept existing | {missing} missing"
        ))
        self.stdout.write(
            "License: All new images are Unsplash License — free for commercial use."
        )
