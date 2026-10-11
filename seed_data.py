# seed_data.py
"""
Realistic sample data for FlockIQ (Philippine broiler farm).

Usage:
    python seed_data.py            # seed only if the database has no Manager yet
    python seed_data.py --reset    # DROP every table, recreate, then seed

Everything is derived from the same records, so the dashboards agree with each other:
  - per-bird feed intake and weight curves drive daily records, feed kg and feed cost
  - each harvested batch's expenses / revenue / profit are summed from its own rows
  - HarvestHistory.expenses = sum of that batch's expense rows
  - HarvestHistory.loss_gain = that batch's sales - that batch's expenses

All prices below are ASSUMPTIONS for sample data. Edit the constants to match what your
farm actually pays and earns.
"""
import random
import sys
from datetime import date, datetime, timedelta

random.seed(2026)  # same sample data every run; change or remove for variety

# ───────────────────────── Assumptions (edit freely) ─────────────────────────
WEIGHT_CURVE = [(0, 42), (7, 175), (14, 440), (21, 850), (28, 1400), (35, 1950), (42, 2550)]  # avg g/bird
INTAKE_CURVE = [(1, 14), (7, 27), (14, 62), (21, 100), (28, 140), (35, 170), (42, 190)]       # g/bird/day

FEED_DEFS = [
    # category,          name,                    CP,   fat, fiber, moist, Ca,   P,    P/kg, stock kg, shelf days, share of batch feed
    ("Chick Booster",   "B-MEG Broiler Booster",  22.0, 5.0, 4.0,   12.0,  1.00, 0.45, 40.0, 3500.0,   75,         0.14),
    ("Grower Pellets",  "B-MEG Broiler Grower",   20.0, 5.0, 4.5,   12.0,  0.90, 0.42, 38.0, 5000.0,   90,         0.31),
    ("Finisher Pellets", "B-MEG Broiler Finisher", 18.0, 5.5, 5.0,   12.0,  0.85, 0.40, 37.0, 6000.0,   90,         0.55),
]

VACCINE_DEFS = [
    # name,                                              type,  mL/bottle, bottles, cost/bottle
    # 30 mL per bottle and 0.03 mL per bird = 1,000 doses per bottle.
    ("Newcastle Disease + Infectious Bronchitis (ND-IB)", "Live", 30.0, 20.0, 450.0),
    ("Infectious Bursal Disease (Gumboro / IBD)",         "Live", 30.0, 20.0, 420.0),
    ("Newcastle Disease (LaSota)",                        "Live", 30.0, 20.0, 380.0),
]
DOSE_PER_BIRD_ML = 0.03

VITAMIN_DEFS = [
    # name,                          type,            qty,  unit, cost/unit
    ("Electrolytes (Anti-Stress)",   "Water-soluble",  10.0, "kg", 280.0),
    ("Vitamin C (Ascorbic Acid)",    "Water-soluble",   5.0, "kg", 650.0),
    ("Vitamin B-Complex",            "Water-soluble",   6.0, "L",  480.0),
    ("Vitamin AD3E",                 "Fat-soluble",     6.0, "L",  520.0),
]

MEDICINE_DEFS = [
    # name,          type,         qty,  unit
    ("Amoxicillin", "Antibiotic",  500.0, "g"),
    ("Tylosin",     "Antibiotic",  500.0, "g"),
    ("Amprolium",   "Anticoccidial", 300.0, "g"),
]

CHICK_PRICE_RANGE = (38.0, 46.0)      # P per day-old chick
FARMGATE_PRICE_RANGE = (92.0, 112.0)  # P per kg live weight (farm-gate, not retail)
HARVESTED_BATCH_COUNT = 12            # the sales forecast needs at least 10
ACTIVE_BATCH_AGE_DAYS = 20
BUYERS = ["San Roque Market", "Balagtas Trading", "Meycauayan Buyer"]


# ───────────────────────── Pure helpers (no database) ─────────────────────────
def interp(table, x):
    if x <= table[0][0]:
        return table[0][1]
    for (x0, y0), (x1, y1) in zip(table, table[1:]):
        if x <= x1:
            return y0 + (y1 - y0) * (x - x0) / (x1 - x0)
    return table[-1][1]


def season_for(d):
    """Philippine dry season is roughly Dec-May; wet season Jun-Nov."""
    return "Dry" if d.month in (12, 1, 2, 3, 4, 5) else "Wet"


def feed_category_for_age(age_days):
    if age_days <= 14:
        return "Chick Booster"
    if age_days <= 28:
        return "Grower Pellets"
    return "Finisher Pellets"


def simulate_harvested_batch(start, age, mort_pct=None, fcr=None, price=None, initial=None):
    """Return the headline numbers for one finished batch. Everything else is derived from these.
    Optional overrides (mort_pct, fcr, price, initial) let callers force a good or bad batch."""
    season = season_for(start)
    initial = initial or random.randrange(4500, 5501, 100)
    if mort_pct is None:
        mort_pct = random.uniform(3.0, 6.0) + (1.0 if season == "Wet" else 0.0)
    deaths = int(initial * mort_pct / 100)
    harvest_count = initial - deaths
    lw = interp(WEIGHT_CURVE, age) * random.uniform(0.95, 1.07) * (0.97 if season == "Dry" else 1.0)
    if fcr is None:
        fcr = random.uniform(1.55, 1.80) + (0.04 if season == "Dry" else 0.0)
    live_kg = harvest_count * lw / 1000.0
    return {
        "season": season, "initial": initial, "deaths": deaths, "harvest_count": harvest_count,
        "lw": round(lw, 1), "fcr_target": fcr, "live_kg": live_kg, "total_feed_kg": fcr * live_kg,
        "chick_price": round(random.uniform(*CHICK_PRICE_RANGE), 2),
        "sale_price": price if price is not None else random.uniform(*FARMGATE_PRICE_RANGE),
    }


def split_amount(total, parts):
    weights = [random.uniform(0.8, 1.2) for _ in range(parts)]
    s = sum(weights)
    amounts = [round(total * w / s, 2) for w in weights]
    amounts[-1] = round(total - sum(amounts[:-1]), 2)
    return amounts


# ───────────────────────── Database seeding ─────────────────────────
def seed(reset=False):
    from run import app, ensure_owner
    from db_ext import db
    from flock_models import (
        User, FlockBatch, Vaccine, VaccinationRecord, MedicationSchedule,
        Vitamin, VitaminSchedule, Medicine, FeedRecord, DailyFeedRecord, MarketPrice, ExpenseCategory,
        WaterExpense, ElectricityExpense, LpgExpense, LaborExpense, OtherExpense,
        HarvestHistory, HarvestSale, DailyRecordSubmission,
        VaccineExpense, FeedExpense, ChickExpense,
    )
    from flock_routes import record_growth_data
    from sqlalchemy import func
    from werkzeug.security import generate_password_hash

    with app.app_context():
        if reset:
            print("Dropping all tables...")
            db.drop_all()
            db.create_all()
            ensure_owner()

        if User.query.filter_by(role="Manager").first():
            print("Sample data already present. Run `python seed_data.py --reset` to start fresh.")
            return
        owner = User.query.filter_by(username="owner").first()
        assert owner, "Run run.py once so the owner account exists."

        today = date.today()

        def new_user(**kw):
            u = User(**kw)
            db.session.add(u)
            db.session.flush()
            return u

        manager = new_user(
            username="manager1", password_hash=generate_password_hash("manager123"),
            role="Manager", first_name="Maria", middle_name="Santos", last_name="Reyes",
            phone_num="09171234567", email="maria.reyes@flockiq.ph",
            address="Meycauayan, Bulacan", bday=date(1990, 5, 14), is_active=True)
        workers = []
        for uname, fn, mn, ln, phone in [
            ("worker1", "Juan", "Dela", "Cruz", "09181112222"),
            ("worker2", "Pedro", "Ramos", "Lim", "09182223333"),
            ("worker3", "Ana", "Garcia", "Tan", "09183334444")]:
            workers.append(new_user(
                username=uname, password_hash=generate_password_hash("worker123"),
                role="Worker", first_name=fn, middle_name=mn, last_name=ln,
                phone_num=phone, email=f"{uname}@flockiq.ph", address="Meycauayan, Bulacan",
                bday=date(1998, random.randint(1, 12), random.randint(1, 28)), is_active=True))

        # Expense categories (Chicks/Feed/Vaccine have their own tables and need none)
        cats = {}
        for n in ["Water", "Electricity", "LPG", "Labor", "Supplies", "Miscellaneous"]:
            c = ExpenseCategory.query.filter_by(category_name=n).first()
            if not c:
                c = ExpenseCategory(user_id=owner.user_id, category_name=n)
                db.session.add(c)
            cats[n] = c
        db.session.flush()

        # Feeds
        feeds, feed_share, feed_stock, feed_price = {}, {}, {}, {}
        for cat, name, cp, fat, fib, moist, ca, ph, price, stock, shelf, share in FEED_DEFS:
            f = FeedRecord(
                user_id=manager.user_id, feed_name=name, feed_category=cat,
                expiration_date=today + timedelta(days=shelf),
                crude_protein=cp, crude_fat=fat, crude_fiber=fib,
                moisture=moist, calcium=ca, phosphorus=ph,
                remaining_quantity=stock)
            db.session.add(f)
            feeds[cat], feed_share[cat], feed_stock[cat] = f, share, stock
            feed_price[cat] = price  # sample purchase price, only used to generate expense amounts
        db.session.flush()

        # Vaccines and vitamins
        vaccines, vaccine_cost = [], {}
        for name, typ, ml, stock, cost in VACCINE_DEFS:
            v = Vaccine(user_id=manager.user_id, vaccine_name=name, vaccine_type=typ,
                        vaccine_exp_date=today + timedelta(days=365),
                        milliliters_per_bottle=ml, remaining_quantity=stock)
            db.session.add(v)
            vaccines.append(v)
            vaccine_cost[name] = cost  # sample price, only used to generate expense amounts
        vitamins = []
        for name, typ, qty, unit, cost in VITAMIN_DEFS:
            v = Vitamin(user_id=manager.user_id, vitamin_name=name, vitamin_type=typ,
                        vitamin_exp_date=today + timedelta(days=365),
                        quantity=qty, unit=unit)
            db.session.add(v)
            vitamins.append(v)
        for name, typ, qty, unit in MEDICINE_DEFS:
            db.session.add(Medicine(user_id=manager.user_id, medicine_name=name, medicine_type=typ,
                                    medicine_exp_date=today + timedelta(days=365), quantity=qty, unit=unit))
        db.session.flush()

        # ── Timeline: one batch at a time, ~8-14 days of downtime between cycles ──
        active_start = today - timedelta(days=ACTIVE_BATCH_AGE_DAYS)
        plan, prev_end = [], active_start - timedelta(days=random.randint(8, 14))
        for _ in range(HARVESTED_BATCH_COUNT):
            age = random.randint(33, 37)
            start = prev_end - timedelta(days=age)
            plan.append((start, age))
            prev_end = start - timedelta(days=random.randint(8, 14))
        plan.reverse()  # oldest first

        year_counter = {}

        def next_name(start):
            idx = year_counter.get(start.year, 0)
            year_counter[start.year] = idx + 1
            return f"Batch-{start.year}-{chr(65 + idx)}"

        # ── Harvested batches (expenses, sales and history all derived consistently) ──
        summary_rows = []
        for start, age in plan:
            sim = simulate_harvested_batch(start, age)
            end = start + timedelta(days=age)
            name = next_name(start)
            b = FlockBatch(
                user_id=owner.user_id, batch_name=name, start_date=start, target_harvest_date=end,
                initial_bird_count=sim["initial"], current_bird_count=sim["harvest_count"],
                season=sim["season"], flock_status="Harvested")
            db.session.add(b)
            db.session.flush()
            bid = b.batch_id
            total_expenses = 0.0

            def d_at(frac):
                return start + timedelta(days=int(age * frac))

            # Chicks
            chick_total = round(sim["initial"] * sim["chick_price"], 2)
            db.session.add(ChickExpense(
                batch_id=bid, quantity=sim["initial"],
                chick_expense_amount=chick_total, chick_expense_status="Paid", expense_date=start,
                description=f"Day-old chicks - {sim['initial']} heads @ P{sim['chick_price']:.2f}"))
            total_expenses += chick_total

            # Feed: three stage entries
            stage_dates = {"Chick Booster": 0.2, "Grower Pellets": 0.5, "Finisher Pellets": 0.85}
            for cat, share in feed_share.items():
                kg = round(sim["total_feed_kg"] * share, 1)
                cost = round(kg * feed_price[cat], 2)
                db.session.add(FeedExpense(
                    feed_record_id=feeds[cat].feed_record_id, batch_id=bid,
                    feed_expense_amount=cost, feed_expense_status="Paid",
                    expense_date=d_at(stage_dates[cat]), description=f"Feed {feeds[cat].feed_name} - {kg}kg"))
                total_expenses += cost

            # Vaccines: bottles = (dose * birds) / mL per bottle
            for v, frac in zip(vaccines, (0.2, 0.4, 0.6)):
                bottles = DOSE_PER_BIRD_ML * sim["initial"] / v.milliliters_per_bottle
                cost = round(bottles * vaccine_cost[v.vaccine_name], 2)
                db.session.add(VaccineExpense(
                    vaccine_id=v.vaccine_id, batch_id=bid, vaccine_expense_amount=cost,
                    vaccine_expense_status="Paid", expense_date=d_at(frac),
                    description=f"{v.vaccine_name} - {round(bottles, 2)} bottle(s)"))
                total_expenses += cost

            # Utilities, labor, supplies
            for amt, frac in zip(split_amount(random.uniform(5000, 8000), 2), (0.3, 0.8)):
                db.session.add(WaterExpense(expense_category_id=cats["Water"].expense_category_id, batch_id=bid,
                                            water_expense_amount=amt, water_expense_status="Paid", expense_date=d_at(frac)))
                total_expenses += amt
            for amt, frac in zip(split_amount(random.uniform(10000, 14000), 2), (0.3, 0.8)):
                db.session.add(ElectricityExpense(expense_category_id=cats["Electricity"].expense_category_id, batch_id=bid,
                                                  electricity_expense_amount=amt, electricity_expense_status="Paid", expense_date=d_at(frac)))
                total_expenses += amt
            for amt, prov, frac in zip(split_amount(random.uniform(4000, 6000), 2), ("Petron Gasul", "Solane"), (0.05, 0.25)):
                db.session.add(LpgExpense(expense_category_id=cats["LPG"].expense_category_id, batch_id=bid,
                                          lpg_expense_amount=amt, lpg_provider=prov, lpg_expense_status="Paid", expense_date=d_at(frac)))
                total_expenses += amt
            for amt, frac in zip(split_amount(random.uniform(30000, 34000), 2), (0.45, 0.95)):
                db.session.add(LaborExpense(expense_category_id=cats["Labor"].expense_category_id, batch_id=bid,
                                            labor_expense_amount=amt, labor_expense_status="Paid", expense_date=d_at(frac)))
                total_expenses += amt
            for cname, lo, hi, frac in (("Supplies", 5000, 8000, 0.0), ("Miscellaneous", 4000, 9000, 0.6)):
                amt = round(random.uniform(lo, hi), 2)
                db.session.add(OtherExpense(user_id=owner.user_id, expense_category_id=cats[cname].expense_category_id,
                                            batch_id=bid, other_expense_amount=amt, other_expense_status="Paid", expense_date=d_at(frac)))
                total_expenses += amt
            total_expenses = round(total_expenses, 2)

            # Sales: 1-3 loads over the first days after harvest, small shrink vs. live weight
            sold_kg_total = sim["live_kg"] * random.uniform(0.975, 0.995)
            n_sales = random.randint(1, 3)
            revenue = 0.0
            for i, kg in enumerate(split_amount(sold_kg_total, n_sales)):
                price = round(sim["sale_price"] + random.uniform(-2.5, 2.5), 2)
                amount = round(kg * price, 2)
                revenue += amount
                db.session.add(HarvestSale(
                    batch_id=bid, user_id=manager.user_id, sale_date=end + timedelta(days=i),
                    kg_sold=round(kg, 1), price_per_kg=price, total_amount=amount,
                    buyer=random.choice(BUYERS), remarks="Live weight sale."))
            revenue = round(revenue, 2)

            # History row: derived from the rows above, so profit = sales - expenses exactly
            live_kg = sim["harvest_count"] * sim["lw"] / 1000.0
            db.session.add(HarvestHistory(
                batch_name=name, start_date=start, end_date=end, age=age,
                initial_count=sim["initial"], harvest_count=sim["harvest_count"],
                mortality_pct=round(sim["deaths"] / sim["initial"] * 100, 2),
                total_deaths=sim["deaths"], culled=0,
                adg=round((sim["lw"] - WEIGHT_CURVE[0][1]) / age, 2),
                fcr=round(sim["total_feed_kg"] / live_kg, 2),
                lw=sim["lw"], expenses=total_expenses, season=sim["season"],
                chick_booster=feeds["Chick Booster"].feed_name,
                grower_pellets=feeds["Grower Pellets"].feed_name,
                finisher_pellets=feeds["Finisher Pellets"].feed_name,
                vaccine_day_12=vaccines[0].vaccine_name, vaccine_day_16=vaccines[1].vaccine_name,
                medicines="Amoxicillin (day 3), Tylosin (day 17)",
                loss_gain=round(revenue - total_expenses, 2),
                remarks="Sample harvested batch.",
                created_at=datetime.combine(end, datetime.min.time()) + timedelta(hours=17)))
            summary_rows.append((name, sim["harvest_count"], total_expenses, revenue, sim["lw"], live_kg))
        db.session.commit()

        # ── Active batch ──
        active = FlockBatch(
            user_id=owner.user_id, batch_name=next_name(active_start), start_date=active_start,
            target_harvest_date=active_start + timedelta(days=35),
            initial_bird_count=5000, current_bird_count=5000,
            season=season_for(active_start), flock_status="Active")
        db.session.add(active)
        db.session.flush()

        chick_price = round(random.uniform(*CHICK_PRICE_RANGE), 2)
        db.session.add(ChickExpense(
            batch_id=active.batch_id, quantity=5000,
            chick_expense_amount=round(5000 * chick_price, 2), chick_expense_status="Paid",
            expense_date=active_start, description=f"Day-old chicks - 5000 heads @ P{chick_price:.2f}"))
        db.session.commit()

        # Daily records: realistic curves; verified ones go through the same code path the app uses
        for day_offset in range(ACTIVE_BATCH_AGE_DAYS):
            d = today - timedelta(days=ACTIVE_BATCH_AGE_DAYS - 1 - day_offset)
            age = (d - active.start_date).days
            worker = random.choice(workers)
            feed = feeds[feed_category_for_age(age)]
            avg_w = round(interp(WEIGHT_CURVE, age) * random.uniform(0.97, 1.03), 1)
            if age <= 7:
                mortality = random.randint(5, 12)
            elif age <= 14:
                mortality = random.randint(2, 6)
            else:
                mortality = random.randint(1, 4)
            cull = 1 if random.random() < 0.15 else 0
            cause = None
            if mortality + cull > 0:
                cause = random.choice(["Weak chick", "Yolk sac infection", "Pasty vent"] if age <= 7
                                      else ["Heat stress", "Injury", "Leg problem", "Respiratory"])
            feed_kg = round(interp(INTAKE_CURVE, age) * random.uniform(0.97, 1.03) * active.current_bird_count / 1000.0, 1)
            sub = DailyRecordSubmission(
                batch_id=active.batch_id, user_id=worker.user_id, record_date=d,
                avg_weight_g=avg_w, mortality=mortality, cull=cull, cause=cause,
                feed_kg=feed_kg, feed_record_id=feed.feed_record_id,
                water_consumption=f"{int(feed_kg * 2)} L",
                abnormal_behavior=random.choice([None, None, "Slight huddling"]),
                visible_illness=random.choice([None, None, None, "Watery eyes"]),
                remarks="Routine daily monitoring.", status="Pending",
                submitted_at=datetime.combine(d, datetime.min.time()) + timedelta(hours=17))
            db.session.add(sub)
            db.session.flush()

            if day_offset in (ACTIVE_BATCH_AGE_DAYS - 3, ACTIVE_BATCH_AGE_DAYS - 2):
                pass  # newest records stay Pending for the manager to review
            elif day_offset == 5:
                sub.status = "Rejected"
                sub.reviewed_by = manager.user_id
                sub.reviewed_at = datetime.utcnow()
                sub.review_notes = "Weight looks off - please re-measure tomorrow."
            else:
                record_growth_data(active, worker.user_id, d, sub.avg_weight_g, sub.feed_kg,
                                   sub.feed_record_id, sub.mortality, sub.cull, sub.cause)
                sub.status = "Verified"
                sub.reviewed_by = manager.user_id
                sub.reviewed_at = datetime.utcnow()
        db.session.commit()

        # Feed stock reflects what the verified records consumed
        for cat, f in feeds.items():
            used = db.session.query(func.sum(DailyFeedRecord.total_kg)).filter_by(
                batch_id=active.batch_id, feed_record_id=f.feed_record_id).scalar() or 0.0
            f.remaining_quantity = max(0.0, round(feed_stock[cat] - used, 1))
            if used > 0:  # the app no longer auto-logs feed cost, so log it as a manual expense
                db.session.add(FeedExpense(
                    feed_record_id=f.feed_record_id, batch_id=active.batch_id,
                    feed_expense_amount=round(used * feed_price[cat], 2), feed_expense_status="Paid",
                    expense_date=today, description=f"Feed {f.feed_name} - {round(used, 1)}kg"))

        # Vaccinations (ND-IB day 12, IBD day 16), administered ones log cost + stock like the app
        for v, day in zip(vaccines[:2], (12, 16)):
            sched = datetime.combine(active.start_date + timedelta(days=day), datetime.min.time()) + timedelta(hours=8)
            done = day <= ACTIVE_BATCH_AGE_DAYS
            db.session.add(VaccinationRecord(
                batch_id=active.batch_id, vaccine_id=v.vaccine_id, user_id=manager.user_id,
                dose_per_bird=DOSE_PER_BIRD_ML, administered_by=manager.full_name if done else None,
                scheduled_date=sched, status="Administered" if done else "Scheduled"))
            if done:
                bottles = DOSE_PER_BIRD_ML * active.current_bird_count / v.milliliters_per_bottle
                v.remaining_quantity = max(0.0, round(v.remaining_quantity - bottles, 2))
                db.session.add(VaccineExpense(
                    vaccine_id=v.vaccine_id, batch_id=active.batch_id,
                    vaccine_expense_amount=round(bottles * vaccine_cost[v.vaccine_name], 2),
                    vaccine_expense_status="Paid", expense_date=sched.date(),
                    description=f"{v.vaccine_name} - {round(bottles, 2)} bottle(s)"))

        for v, day, dose in zip(vitamins, (1, 8, 15, 22), ("1 g / L water", "1 g / L water", "1 mL / L water", "1 mL / L water")):
            sched = datetime.combine(active.start_date + timedelta(days=day), datetime.min.time()) + timedelta(hours=6)
            done = day <= ACTIVE_BATCH_AGE_DAYS
            db.session.add(VitaminSchedule(
                batch_id=active.batch_id, vitamin_id=v.vitamin_id, user_id=manager.user_id,
                day_given=day, dosage=dose, scheduled_date=sched,
                status="Administered" if done else "Scheduled",
                administered_by=manager.full_name if done else None))
        for name, day in [("Amoxicillin", 3), ("Tylosin", 17)]:
            sched = datetime.combine(active.start_date + timedelta(days=day), datetime.min.time()) + timedelta(hours=7)
            db.session.add(MedicationSchedule(
                batch_id=active.batch_id, user_id=manager.user_id, item_name=name,
                item_type="Medicine", dosage="1 g / L water", scheduled_date=sched,
                status="Administered", administered_by=manager.full_name))

        # Active-batch running costs so far (feed, vaccine and chick costs were logged above)
        db.session.add(WaterExpense(expense_category_id=cats["Water"].expense_category_id, batch_id=active.batch_id,
                                    water_expense_amount=3200, water_expense_status="Paid", expense_date=today - timedelta(days=8)))
        db.session.add(ElectricityExpense(expense_category_id=cats["Electricity"].expense_category_id, batch_id=active.batch_id,
                                          electricity_expense_amount=6100, electricity_expense_status="Paid", expense_date=today - timedelta(days=6)))
        for amt, prov, ago in [(2400, "Petron Gasul", 18), (2250, "Solane", 12)]:
            db.session.add(LpgExpense(expense_category_id=cats["LPG"].expense_category_id, batch_id=active.batch_id,
                                      lpg_expense_amount=amt, lpg_provider=prov, lpg_expense_status="Paid", expense_date=today - timedelta(days=ago)))
        db.session.add(LaborExpense(expense_category_id=cats["Labor"].expense_category_id, batch_id=active.batch_id,
                                    labor_expense_amount=16500, labor_expense_status="Paid", expense_date=today - timedelta(days=5)))
        db.session.add(OtherExpense(user_id=owner.user_id, expense_category_id=cats["Supplies"].expense_category_id,
                                    batch_id=active.batch_id, other_expense_amount=6500, other_expense_status="Paid",
                                    expense_date=active_start))
        db.session.add(OtherExpense(user_id=owner.user_id, expense_category_id=cats["Miscellaneous"].expense_category_id,
                                    batch_id=active.batch_id, other_expense_amount=2300, other_expense_status="Pending",
                                    expense_date=today - timedelta(days=3)))

        # Farm-gate (live weight) price history, weekly
        price = random.uniform(100, 108)
        for weeks_ago in range(7, -1, -1):
            price = min(115.0, max(92.0, price + random.uniform(-3, 3)))
            db.session.add(MarketPrice(user_id=owner.user_id, record_date=today - timedelta(weeks=weeks_ago),
                                       price_per_kg=round(price, 2), location="Farm-gate, Bulacan"))
        db.session.commit()

        # ── Summary ──
        print("Sample data seeded.")
        print("  Owner:    owner / owner123")
        print("  Manager:  manager1 / manager123")
        print("  Workers:  worker1..3 / worker123")
        print(f"  Active batch: {active.batch_name} ({active.current_bird_count} birds)")
        print(f"  Pending submissions: {DailyRecordSubmission.query.filter_by(status='Pending').count()}")
        print()
        print(f"{'Batch':<14}{'Birds':>7}{'Expenses':>12}{'Sales':>12}{'Profit':>11}{'/bird':>8}{'Cost/kg':>9}")
        for name, birds, exp, rev, lw, live_kg in summary_rows:
            print(f"{name:<14}{birds:>7}{exp:>12,.0f}{rev:>12,.0f}{rev - exp:>11,.0f}{(rev - exp) / birds:>8.1f}{exp / live_kg:>9.1f}")


if __name__ == "__main__":
    seed(reset="--reset" in sys.argv)