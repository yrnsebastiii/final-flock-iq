# add_harvested_batches.py
"""
Add realistic harvested batches to your EXISTING database (no reset, nothing deleted).

Usage:
    python add_harvested_batches.py          # adds 5 batches
    python add_harvested_batches.py 8        # adds 8 batches

- New batches are placed BEFORE your earliest existing batch, so the farm's
  "one batch at a time" rule still holds and nothing overlaps.
- Each batch gets chick, feed, vaccine, utility, labor and supply expenses, 1-3 sales,
  and a HarvestHistory row whose profit = that batch's sales - that batch's expenses.
- Uses your existing feeds, vaccines, owner and manager accounts; creates any that are missing.
- Mix of outcomes: some good, some average, one rough (disease/heat or a price dip).
"""
import random
import sys
from datetime import date, datetime, timedelta

from seed_data import (
    WEIGHT_CURVE, FEED_DEFS, VACCINE_DEFS, DOSE_PER_BIRD_ML, BUYERS,
    interp, split_amount, simulate_harvested_batch,
)

# (label, mortality %, FCR, farm-gate price/kg) - None means "use the normal random range"
PROFILES = [
    ("good",    3.2, 1.58, 108.0),
    ("average", None, None, None),
    ("average", None, None, None),
    ("rough",   9.5, 1.92, 95.0),   # disease/heat stress batch with a soft price
    ("good",    3.8, 1.62, 112.0),
]


def main(n):
    from run import app
    from db_ext import db
    from flock_models import (
        User, FlockBatch, Vaccine, FeedRecord, ExpenseCategory,
        WaterExpense, ElectricityExpense, LpgExpense, LaborExpense, OtherExpense,
        HarvestHistory, HarvestSale, VaccineExpense, FeedExpense, ChickExpense,
    )

    with app.app_context():
        owner = User.query.filter_by(role="Owner").first()
        assert owner, "No Owner account found. Run run.py once first."
        manager = User.query.filter_by(role="Manager").first() or owner
        today = date.today()

        # categories
        cats = {}
        for name in ["Water", "Electricity", "LPG", "Labor", "Supplies", "Miscellaneous"]:
            c = ExpenseCategory.query.filter_by(category_name=name).first()
            if not c:
                c = ExpenseCategory(user_id=owner.user_id, category_name=name)
                db.session.add(c)
            cats[name] = c

        # feeds: first existing one per category, else create from defaults
        feeds, share, price_of = {}, {}, {}
        for cat, fname, cp, fat, fib, moist, ca, ph, price, stock, shelf, sh in FEED_DEFS:
            f = FeedRecord.query.filter_by(feed_category=cat).first()
            if not f:
                f = FeedRecord(user_id=manager.user_id, feed_name=fname, feed_category=cat,
                               expiration_date=today + timedelta(days=shelf),
                               crude_protein=cp, crude_fat=fat, crude_fiber=fib, moisture=moist,
                               calcium=ca, phosphorus=ph, remaining_quantity=stock)
                db.session.add(f)
            feeds[cat], share[cat], price_of[cat] = f, sh, price  # price only generates sample expense amounts

        # vaccines: first three existing, top up from defaults
        vaccine_cost = {n: cst for n, _t, _m, _s, cst in VACCINE_DEFS}  # sample prices only
        vaccines = Vaccine.query.order_by(Vaccine.vaccine_id).limit(3).all()
        for name, typ, ml, stock, cost in VACCINE_DEFS:
            if len(vaccines) >= 3:
                break
            if any(v.vaccine_name == name for v in vaccines):
                continue
            v = Vaccine(user_id=manager.user_id, vaccine_name=name, vaccine_type=typ,
                        vaccine_exp_date=today + timedelta(days=365),
                        milliliters_per_bottle=ml, remaining_quantity=stock)
            db.session.add(v)
            vaccines.append(v)
        db.session.flush()

        # place new batches before the earliest existing one
        earliest = db.session.query(db.func.min(FlockBatch.start_date)).scalar()
        h_earliest = db.session.query(db.func.min(HarvestHistory.start_date)).scalar()
        candidates = [d for d in (earliest, h_earliest) if d]
        prev_start = min(candidates) if candidates else today - timedelta(days=60)

        plan = []
        cursor_end = prev_start - timedelta(days=random.randint(8, 14))
        for i in range(n):
            age = random.randint(33, 37)
            start = cursor_end - timedelta(days=age)
            plan.append((start, age, PROFILES[i % len(PROFILES)]))
            cursor_end = start - timedelta(days=random.randint(8, 14))
        plan.reverse()  # oldest first

        def unique_name(start):
            year = start.year
            used = {b.batch_name for b in FlockBatch.query.filter(
                FlockBatch.batch_name.like(f"Batch-{year}-%")).all()}
            for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                if f"Batch-{year}-{c}" not in used:
                    return f"Batch-{year}-{c}"
            return f"Batch-{year}-{len(used) + 1}"

        rows = []
        for start, age, (label, mort, fcr, price) in plan:
            sim = simulate_harvested_batch(start, age, mort_pct=mort, fcr=fcr, price=price)
            end = start + timedelta(days=age)
            name = unique_name(start)
            b = FlockBatch(
                user_id=owner.user_id, batch_name=name, start_date=start, target_harvest_date=end,
                initial_bird_count=sim["initial"], current_bird_count=sim["harvest_count"],
                season=sim["season"], flock_status="Harvested")
            db.session.add(b)
            db.session.flush()
            bid = b.batch_id
            total = 0.0

            def d_at(frac):
                return start + timedelta(days=int(age * frac))

            chick_total = round(sim["initial"] * sim["chick_price"], 2)
            db.session.add(ChickExpense(
                batch_id=bid, quantity=sim["initial"],
                chick_expense_amount=chick_total, chick_expense_status="Paid", expense_date=start,
                description=f"Day-old chicks - {sim['initial']} heads @ P{sim['chick_price']:.2f}"))
            total += chick_total

            stage = {"Chick Booster": 0.2, "Grower Pellets": 0.5, "Finisher Pellets": 0.85}
            for cat, sh in share.items():
                kg = round(sim["total_feed_kg"] * sh, 1)
                cost = round(kg * price_of[cat], 2)
                db.session.add(FeedExpense(
                    feed_record_id=feeds[cat].feed_record_id, batch_id=bid, feed_expense_amount=cost,
                    feed_expense_status="Paid", expense_date=d_at(stage[cat]),
                    description=f"Feed {feeds[cat].feed_name} - {kg}kg"))
                total += cost

            for v, frac in zip(vaccines, (0.2, 0.4, 0.6)):
                ml = v.milliliters_per_bottle or 30.0
                bottles = DOSE_PER_BIRD_ML * sim["initial"] / ml
                cost = round(bottles * vaccine_cost.get(v.vaccine_name, 400.0), 2)
                db.session.add(VaccineExpense(
                    vaccine_id=v.vaccine_id, batch_id=bid, vaccine_expense_amount=cost,
                    vaccine_expense_status="Paid", expense_date=d_at(frac),
                    description=f"{v.vaccine_name} - {round(bottles, 2)} bottle(s)"))
                total += cost

            for amt, frac in zip(split_amount(random.uniform(5000, 8000), 2), (0.3, 0.8)):
                db.session.add(WaterExpense(expense_category_id=cats["Water"].expense_category_id, batch_id=bid,
                                            water_expense_amount=amt, water_expense_status="Paid", expense_date=d_at(frac)))
                total += amt
            for amt, frac in zip(split_amount(random.uniform(10000, 14000), 2), (0.3, 0.8)):
                db.session.add(ElectricityExpense(expense_category_id=cats["Electricity"].expense_category_id, batch_id=bid,
                                                  electricity_expense_amount=amt, electricity_expense_status="Paid", expense_date=d_at(frac)))
                total += amt
            for amt, prov, frac in zip(split_amount(random.uniform(4000, 6000), 2), ("Petron Gasul", "Solane"), (0.05, 0.25)):
                db.session.add(LpgExpense(expense_category_id=cats["LPG"].expense_category_id, batch_id=bid,
                                          lpg_expense_amount=amt, lpg_provider=prov, lpg_expense_status="Paid", expense_date=d_at(frac)))
                total += amt
            for amt, frac in zip(split_amount(random.uniform(30000, 34000), 2), (0.45, 0.95)):
                db.session.add(LaborExpense(expense_category_id=cats["Labor"].expense_category_id, batch_id=bid,
                                            labor_expense_amount=amt, labor_expense_status="Paid", expense_date=d_at(frac)))
                total += amt
            for cname, lo, hi, frac in (("Supplies", 5000, 8000, 0.0), ("Miscellaneous", 4000, 9000, 0.6)):
                amt = round(random.uniform(lo, hi), 2)
                db.session.add(OtherExpense(user_id=owner.user_id, expense_category_id=cats[cname].expense_category_id,
                                            batch_id=bid, other_expense_amount=amt, other_expense_status="Paid", expense_date=d_at(frac)))
                total += amt
            total = round(total, 2)

            sold_kg = sim["live_kg"] * random.uniform(0.975, 0.995)
            revenue = 0.0
            for i, kg in enumerate(split_amount(sold_kg, random.randint(1, 3))):
                p = round(sim["sale_price"] + random.uniform(-2.5, 2.5), 2)
                amount = round(kg * p, 2)
                revenue += amount
                db.session.add(HarvestSale(
                    batch_id=bid, user_id=manager.user_id, sale_date=end + timedelta(days=i),
                    kg_sold=round(kg, 1), price_per_kg=p, total_amount=amount,
                    buyer=random.choice(BUYERS), remarks="Live weight sale."))
            revenue = round(revenue, 2)

            live_kg = sim["harvest_count"] * sim["lw"] / 1000.0
            db.session.add(HarvestHistory(
                batch_name=name, start_date=start, end_date=end, age=age,
                initial_count=sim["initial"], harvest_count=sim["harvest_count"],
                mortality_pct=round(sim["deaths"] / sim["initial"] * 100, 2),
                total_deaths=sim["deaths"], culled=0,
                adg=round((sim["lw"] - WEIGHT_CURVE[0][1]) / age, 2),
                fcr=round(sim["total_feed_kg"] / live_kg, 2), lw=sim["lw"],
                expenses=total, season=sim["season"],
                chick_booster=feeds["Chick Booster"].feed_name,
                grower_pellets=feeds["Grower Pellets"].feed_name,
                finisher_pellets=feeds["Finisher Pellets"].feed_name,
                vaccine_day_12=vaccines[0].vaccine_name if vaccines else None,
                vaccine_day_16=vaccines[1].vaccine_name if len(vaccines) > 1 else None,
                medicines="Amoxicillin (day 3), Tylosin (day 17)",
                loss_gain=round(revenue - total, 2), remarks=f"Sample harvested batch ({label}).",
                created_at=datetime.combine(end, datetime.min.time()) + timedelta(hours=17)))
            rows.append((name, label, start, sim["harvest_count"], sim["deaths"] / sim["initial"] * 100,
                         total, revenue, live_kg))

        db.session.commit()
        print(f"Added {len(rows)} harvested batches.\n")
        print(f"{'Batch':<14}{'Type':<9}{'Start':<12}{'Birds':>6}{'Mort%':>7}{'Expenses':>11}{'Sales':>11}{'Profit':>10}{'/bird':>7}")
        for name, label, st, birds, mp, exp, rev, lk in rows:
            print(f"{name:<14}{label:<9}{st.isoformat():<12}{birds:>6}{mp:>7.1f}{exp:>11,.0f}{rev:>11,.0f}{rev - exp:>10,.0f}{(rev - exp) / birds:>7.1f}")


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 5)