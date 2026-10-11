# flock_routes.py - COMPLETE REVISION
from flask import Blueprint, request, session, redirect, url_for, flash, render_template_string, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from db_ext import db
from sqlalchemy import func
from datetime import date, datetime, timedelta
from functools import wraps
import json
import re
import random
from flock_models import (
    User, FlockBatch, Vaccine, VaccinationRecord, MedicationSchedule,
    MortalityRecord, WeightRecord, AdgCalculation, FcrCalculation, FlockReport,
    MarketPrice, FeedRecord, DailyFeedRecord,
    ExpenseCategory, WaterExpense, ElectricityExpense, OtherExpense,
    PerformanceReport, Vitamin, VitaminSchedule, Medicine, LpgExpense, LaborExpense,
    HarvestHistory, HarvestSale, DailyRecordSubmission, WeeklyRecord,
    VaccineExpense, FeedExpense, ChickExpense,
)
from flock_templates import (
    TEMPLATE_LOGIN, TEMPLATE_OWNER, TEMPLATE_MANAGER, TEMPLATE_WORKER,
    TEMPLATE_PERFORMANCE_REPORT_PRINT, TEMPLATE_EXPENSE_HISTORY
)

bp = Blueprint("main", __name__)

MONTH_ORDER = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
FEED_CATEGORIES = ["Chick Booster", "Grower Pellets", "Finisher Pellets"]
SEASONS = ["Dry", "Wet"]
FEED_NUTRIENT_FIELDS = [
    "crude_protein", "crude_fat", "crude_fiber",
    "moisture", "calcium", "phosphorus",
]

# ─── Auth Decorators ────────────────────────────────────────────────────────

def login_required(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in first.")
            return redirect(url_for("main.login"))
        return f(*args, **kwargs)
    return wrapped

def role_required(*roles):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if session.get("role") not in roles:
                flash("Access denied.")
                return redirect(url_for("main.dashboard"))
            return f(*args, **kwargs)
        return wrapped
    return decorator

# ─── Reference / Market Data ────────────────────────────────────────────────

BANTAY_PRESYO_URL = "https://www.bantaypresyo.da.gov.ph/tbl_meat.php"
BANTAY_PRESYO_FALLBACK_PRICE = 165.0

def get_da_bantay_presyo_price():
    try:
        import requests
        from bs4 import BeautifulSoup
    except ImportError:
        return {"price": BANTAY_PRESYO_FALLBACK_PRICE, "source": "Fallback reference", "live": False}
    try:
        resp = requests.get(BANTAY_PRESYO_URL, timeout=6)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        chicken_prices = []
        for row in soup.find_all("tr"):
            cells = [c.get_text(strip=True) for c in row.find_all(["td", "th"])]
            if len(cells) < 2:
                continue
            label = cells[0].lower()
            if "chicken" not in label and "manok" not in label:
                continue
            for cell in cells[1:]:
                cleaned = cell.replace(",", "").replace("₱", "").replace("php", "").strip()
                try:
                    val = float(cleaned)
                except ValueError:
                    continue
                if 50.0 <= val <= 500.0:
                    chicken_prices.append(val)
        if chicken_prices:
            avg_price = round(sum(chicken_prices) / len(chicken_prices), 2)
            return {"price": avg_price, "source": "DA Bantay Presyo (live)", "live": True}
    except Exception:
        pass
    return {"price": BANTAY_PRESYO_FALLBACK_PRICE, "source": "Fallback reference", "live": False}

def get_live_market_data():
    scraped = get_da_bantay_presyo_price()
    return {
        "retail_avg": scraped["price"],
        "last_update": date.today().strftime("%b %d, %Y"),
        "source": scraped["source"],
        "live": scraped["live"]
    }

def get_current_avg_market_price():
    return get_live_market_data()["retail_avg"]

# ─── Batch Snapshot ──────────────────────────────────────────────────────────

def get_batch_snapshot(batch):
    latest_weight = (WeightRecord.query.filter_by(batch_id=batch.batch_id)
                      .order_by(WeightRecord.record_date.desc(), WeightRecord.weight_id.desc()).first())
    latest_adg = (AdgCalculation.query.filter_by(batch_id=batch.batch_id)
                  .order_by(AdgCalculation.record_date.desc(), AdgCalculation.calc_id.desc()).first())
    latest_fcr = (FcrCalculation.query.filter_by(batch_id=batch.batch_id)
                  .order_by(FcrCalculation.fcr_id.desc()).first())
    total_feed = db.session.query(func.sum(DailyFeedRecord.total_kg)).filter_by(batch_id=batch.batch_id).scalar() or 0.0

    latest_weight_g = latest_weight.total_weight_gain if latest_weight else 0.0
    age_days = latest_adg.number_of_days if latest_adg else batch.age_days
    adg_value = latest_adg.adg_value if latest_adg else 0.0
    fcr_value = latest_fcr.fcr_value if latest_fcr else 0.0
    record_date = latest_weight.record_date if latest_weight else batch.start_date

    return {
        "latest_weight_g": latest_weight_g, "age_days": age_days, "adg_value": adg_value,
        "fcr_value": fcr_value, "total_feed": round(total_feed, 2), "record_date": record_date
    }

def get_flock_totals(flocks):
    initial = sum(f.initial_bird_count for f in flocks)
    remaining = sum(f.current_bird_count for f in flocks)
    deaths = max(0, initial - remaining)
    survival_pct = round((remaining / initial) * 100, 1) if initial > 0 else 0.0
    mortality_pct = round((deaths / initial) * 100, 1) if initial > 0 else 0.0
    return {"initial": initial, "remaining": remaining, "deaths": deaths,
            "survival_pct": survival_pct, "mortality_pct": mortality_pct}

# ─── Analytics Helpers ──────────────────────────────────────────────────────

def get_flock_analytics(flocks):
    analytics_list = []
    for f in flocks:
        snap = get_batch_snapshot(f)
        total_feed = snap["total_feed"]
        current_birds = f.current_bird_count or 0
        latest_weight = snap["latest_weight_g"] or 0
        initial_weight = 42
        age = f.age_days or 1
        adg = round((latest_weight - initial_weight) / age, 2) if age > 0 and latest_weight > 0 else 0.0
        total_weight_kg = round((current_birds * latest_weight) / 1000.0, 2) if current_birds > 0 else 0.0
        fcr = round(total_feed / total_weight_kg, 2) if total_weight_kg > 0 else 0.0
        
        analytics_list.append({
            "flock": f,
            "analytics": {
                "adg": adg, "fcr": fcr, "latest_weight": latest_weight,
                "age_days": age, "total_feed": total_feed, "total_weight_kg": total_weight_kg
            }
        })
    return analytics_list

def get_best_season_for_sales():
    harvests = HarvestHistory.query.filter_by(is_archived=False).all()
    if not harvests:
        return {"available": False}
    
    dry_sales, wet_sales, monthly_prices = [], [], {}
    for h in harvests:
        if h.end_date and h.loss_gain is not None and h.harvest_count and h.lw:
            live_kg = (h.harvest_count * h.lw) / 1000.0
            if live_kg > 0:
                revenue = (h.loss_gain or 0) + (h.expenses or 0)
                price_per_kg = revenue / live_kg
                if h.season == "Dry":
                    dry_sales.append(price_per_kg)
                elif h.season == "Wet":
                    wet_sales.append(price_per_kg)
                month = h.end_date.strftime("%b")
                monthly_prices.setdefault(month, []).append(price_per_kg)
    
    dry_avg = sum(dry_sales) / len(dry_sales) if dry_sales else 0
    wet_avg = sum(wet_sales) / len(wet_sales) if wet_sales else 0
    chart_labels, chart_data = [], []
    for m in MONTH_ORDER:
        if m in monthly_prices:
            chart_labels.append(m)
            chart_data.append(round(sum(monthly_prices[m]) / len(monthly_prices[m]), 2))
    
    return {
        "available": len(harvests) > 0, "dry_avg": round(dry_avg, 2), "wet_avg": round(wet_avg, 2),
        "best_season": "Dry" if dry_avg > wet_avg else "Wet", "labels": chart_labels, "data": chart_data
    }

def get_or_create_category(name):
    cat = ExpenseCategory.query.filter(func.lower(ExpenseCategory.category_name) == name.lower()).first()
    if not cat:
        cat = ExpenseCategory(user_id=session["user_id"], category_name=name)
        db.session.add(cat)
        db.session.flush()
    return cat

def parse_expense_date(form):
    raw = form.get("expense_date")
    if raw:
        try:
            return datetime.strptime(raw, "%Y-%m-%d").date()
        except ValueError:
            pass
    return date.today()

def get_active_batch():
    return FlockBatch.query.filter_by(flock_status="Active").first()

def get_category_spending(year=None, month=None):
    today = date.today()
    year = year or today.year
    month = month or today.month

    def month_totals(model, amount_col):
        return (db.session.query(ExpenseCategory.category_name, func.sum(amount_col))
                .join(model, model.expense_category_id == ExpenseCategory.expense_category_id)
                .filter(func.extract('year', model.expense_date) == year,
                        func.extract('month', model.expense_date) == month)
                .group_by(ExpenseCategory.category_name)
                .all())

    totals = {}
    for model, amount_col in [
        (WaterExpense, WaterExpense.water_expense_amount),
        (ElectricityExpense, ElectricityExpense.electricity_expense_amount),
        (LpgExpense, LpgExpense.lpg_expense_amount),
        (LaborExpense, LaborExpense.labor_expense_amount),
        (OtherExpense, OtherExpense.other_expense_amount),
    ]:
        for cat_name, amt in month_totals(model, amount_col):
            totals[cat_name] = totals.get(cat_name, 0.0) + (amt or 0.0)

    rows = sorted(
        ({"category": k, "total": round(v, 2)} for k, v in totals.items()),
        key=lambda r: r["total"], reverse=True
    )
    return {
        "year": year, "month": month, "month_value": f"{year:04d}-{month:02d}",
        "month_label": date(year, month, 1).strftime("%B %Y"), "rows": rows,
        "grand_total": round(sum(r["total"] for r in rows), 2)
    }

def get_expense_summary(all_batches=False):
    active = None if all_batches else get_active_batch()

    def tot(model, col):
        q = db.session.query(func.sum(col))
        if not all_batches:
            q = q.filter(model.batch_id == (active.batch_id if active else -1))
        return q.scalar() or 0.0

    water_total = tot(WaterExpense, WaterExpense.water_expense_amount)
    elec_total = tot(ElectricityExpense, ElectricityExpense.electricity_expense_amount)
    lpg_total = tot(LpgExpense, LpgExpense.lpg_expense_amount)
    labor_total = tot(LaborExpense, LaborExpense.labor_expense_amount)
    other_total = tot(OtherExpense, OtherExpense.other_expense_amount)
    vaccine_total = tot(VaccineExpense, VaccineExpense.vaccine_expense_amount)
    feed_total = tot(FeedExpense, FeedExpense.feed_expense_amount)
    chick_total = tot(ChickExpense, ChickExpense.chick_expense_amount)

    return {
        "water": round(water_total, 2), "electricity": round(elec_total, 2),
        "lpg": round(lpg_total, 2), "labor": round(labor_total, 2),
        "other": round(other_total, 2), "vaccine": round(vaccine_total, 2),
        "feed": round(feed_total, 2), "chick": round(chick_total, 2),
        "total": round(water_total + elec_total + lpg_total + labor_total + other_total + vaccine_total + feed_total + chick_total, 2)
    }

def get_profit_loss_summary():
    total_revenue = db.session.query(func.sum(HarvestSale.total_amount)).scalar() or 0.0
    total_expenses = get_expense_summary(all_batches=True)["total"]
    net = round(total_revenue - total_expenses, 2)
    return {
        "total_revenue": round(total_revenue, 2), "total_expenses": total_expenses,
        "net": net, "status": "Profit" if net >= 0 else "Loss", "has_sales": total_revenue > 0
    }

def get_batch_expense_total(batch_id):
    total = 0.0
    for model, col in [
        (WaterExpense, WaterExpense.water_expense_amount),
        (ElectricityExpense, ElectricityExpense.electricity_expense_amount),
        (LpgExpense, LpgExpense.lpg_expense_amount),
        (LaborExpense, LaborExpense.labor_expense_amount),
        (OtherExpense, OtherExpense.other_expense_amount),
        (VaccineExpense, VaccineExpense.vaccine_expense_amount),
        (FeedExpense, FeedExpense.feed_expense_amount),
        (ChickExpense, ChickExpense.chick_expense_amount),
    ]:
        total += db.session.query(func.sum(col)).filter(model.batch_id == batch_id).scalar() or 0.0
    return round(total, 2)

def recalc_harvest_profit(batch_id):
    batch = FlockBatch.query.get(batch_id) if batch_id else None
    if not batch or batch.flock_status not in ("Harvested", "Archived"):
        return
    h = HarvestHistory.query.filter_by(batch_name=batch.batch_name, start_date=batch.start_date).first()
    if not h:
        return
    revenue = db.session.query(func.sum(HarvestSale.total_amount)).filter_by(batch_id=batch_id).scalar() or 0.0
    expenses = get_batch_expense_total(batch_id)
    h.expenses = expenses
    h.loss_gain = round(revenue - expenses, 2)

def scoped_expenses(model):
    active = get_active_batch()
    if not active:
        return []
    return model.query.filter(model.batch_id == active.batch_id).order_by(model.expense_id.desc()).all()

EXPENSE_TYPES = [
    ("Chicks", ChickExpense, "chick_expense_amount", "chick_expense_status"),
    ("Feed", FeedExpense, "feed_expense_amount", "feed_expense_status"),
    ("Vaccine", VaccineExpense, "vaccine_expense_amount", "vaccine_expense_status"),
    ("Water", WaterExpense, "water_expense_amount", "water_expense_status"),
    ("Electricity", ElectricityExpense, "electricity_expense_amount", "electricity_expense_status"),
    ("LPG", LpgExpense, "lpg_expense_amount", "lpg_expense_status"),
    ("Labor", LaborExpense, "labor_expense_amount", "labor_expense_status"),
    ("Other", OtherExpense, "other_expense_amount", "other_expense_status"),
]

def get_batch_expense_rows(batch_id):
    rows = []
    for label, model, amt_col, status_col in EXPENSE_TYPES:
        for e in model.query.filter_by(batch_id=batch_id).all():
            desc = getattr(e, "description", None) or ""
            if label == "LPG":
                desc = getattr(e, "lpg_provider", None) or ""
            elif label == "Other":
                cat = getattr(e, "category", None)
                desc = cat.category_name if cat else ""
            rows.append({"type": label, "date": e.expense_date, "desc": desc,
                         "amount": getattr(e, amt_col) or 0.0, "status": getattr(e, status_col) or ""})
    rows.sort(key=lambda r: (r["date"] or date.min, r["type"]))
    return rows

def get_batch_cost_summary(batch):
    bid = batch.batch_id

    def total(model, col):
        return round(db.session.query(func.sum(col)).filter(model.batch_id == bid).scalar() or 0.0, 2)

    chick_qty = db.session.query(func.sum(ChickExpense.quantity)).filter_by(batch_id=bid).scalar() or 0
    parts = {
        "chicks": total(ChickExpense, ChickExpense.chick_expense_amount),
        "feed": total(FeedExpense, FeedExpense.feed_expense_amount),
        "vaccine": total(VaccineExpense, VaccineExpense.vaccine_expense_amount),
        "water": total(WaterExpense, WaterExpense.water_expense_amount),
        "electricity": total(ElectricityExpense, ElectricityExpense.electricity_expense_amount),
        "lpg": total(LpgExpense, LpgExpense.lpg_expense_amount),
        "labor": total(LaborExpense, LaborExpense.labor_expense_amount),
        "other": total(OtherExpense, OtherExpense.other_expense_amount),
    }
    grand = round(sum(parts.values()), 2)
    live_kg = 0.0
    if batch.flock_status in ("Harvested", "Archived"):
        h = HarvestHistory.query.filter_by(batch_name=batch.batch_name, start_date=batch.start_date).first()
        if h and h.harvest_count and h.lw:
            live_kg = h.harvest_count * h.lw / 1000.0
    else:
        snap = get_batch_snapshot(batch)
        live_kg = (batch.current_bird_count or 0) * (snap["latest_weight_g"] or 0.0) / 1000.0

    feed_kg = db.session.query(func.sum(DailyFeedRecord.total_kg)).filter_by(batch_id=bid).scalar() or 0.0
    birds = batch.current_bird_count or 0

    def ratio(a, b, nd=2):
        if not b:
            return None
        try:
            val_a, val_b = float(a), float(b)
            return round(val_a / val_b, nd) if val_b > 0 else None
        except (TypeError, ValueError, ZeroDivisionError):
            return None

    return {
        "batch_name": batch.batch_name, "status": batch.flock_status, "parts": parts, "total": grand,
        "cost_per_chick": ratio(parts["chicks"], chick_qty), "cost_per_bird": ratio(grand, birds),
        "feed_kg": round(feed_kg, 1), "feed_cost_per_kg": ratio(parts["feed"], feed_kg),
        "live_kg": round(live_kg, 1), "cost_per_kg_live": ratio(grand, live_kg),
    }

def get_harvest_profit_summary():
    harvests = HarvestHistory.query.filter_by(is_archived=False).all()
    total_batch_expenses = sum(h.expenses or 0.0 for h in harvests)
    total_profit = sum(h.loss_gain or 0.0 for h in harvests)
    total_revenue = total_profit + total_batch_expenses
    total_live_kg = sum(((h.harvest_count or 0) * (h.lw or 0.0)) / 1000.0 for h in harvests)
    cost_per_kg = round(total_batch_expenses / total_live_kg, 2) if total_live_kg > 0 else 0.0
    return {
        "cost_per_kg_live": cost_per_kg, "total_live_kg": round(total_live_kg, 1),
        "batch_count": len(harvests), "total_revenue": round(total_revenue, 2),
        "total_batch_expenses": round(total_batch_expenses, 2), "total_profit": round(total_profit, 2),
        "status": "Profit" if total_profit >= 0 else "Loss"
    }

def get_upcoming_schedule(days_ahead=7):
    now = datetime.utcnow()
    end = now + timedelta(days=days_ahead)
    lookback = now - timedelta(days=2)

    vaccinations = (VaccinationRecord.query
        .filter(VaccinationRecord.status == 'Scheduled',
                VaccinationRecord.scheduled_date <= end,
                VaccinationRecord.scheduled_date >= lookback)
        .order_by(VaccinationRecord.scheduled_date).all())

    vitamins = (VitaminSchedule.query
        .filter(VitaminSchedule.status == 'Scheduled',
                VitaminSchedule.scheduled_date <= end,
                VitaminSchedule.scheduled_date >= lookback)
        .order_by(VitaminSchedule.scheduled_date).all())

    items = []
    for v in vaccinations:
        items.append({
            "kind": "Vaccination", "label": v.vaccine_name,
            "batch": v.batch.batch_name if v.batch else "-", "date": v.scheduled_date,
            "overdue": v.scheduled_date < now, "id": v.vaccination_record_id, "icon": "fa-syringe"
        })
    for v in vitamins:
        items.append({
            "kind": "Vitamin", "label": v.vitamin.vitamin_name if v.vitamin else "Vitamin",
            "batch": v.batch.batch_name if v.batch else "-", "date": v.scheduled_date,
            "overdue": v.scheduled_date < now, "id": v.schedule_id, "icon": "fa-tablets"
        })
    items.sort(key=lambda i: i["date"])
    return items

def get_next_vaccination():
    now = datetime.utcnow()
    v = (VaccinationRecord.query
         .filter(VaccinationRecord.status == 'Scheduled',
                 VaccinationRecord.scheduled_date >= now)
         .order_by(VaccinationRecord.scheduled_date).first())
    if v:
        return {"name": v.vaccine_name, "date": v.scheduled_date, "batch": v.batch.batch_name if v.batch else "-"}
    return None

def get_next_medication():
    now = datetime.utcnow()
    m = (MedicationSchedule.query
         .filter(MedicationSchedule.status == 'Scheduled',
                 MedicationSchedule.scheduled_date >= now)
         .order_by(MedicationSchedule.scheduled_date).first())
    if m:
        return {"name": m.item_name, "date": m.scheduled_date, "batch": m.batch.batch_name if m.batch else "-"}
    return None

def vaccination_for_day(batch, day):
    if not batch or not batch.start_date:
        return None
    for v in (VaccinationRecord.query.filter_by(batch_id=batch.batch_id)
              .order_by(VaccinationRecord.scheduled_date).all()):
        if (v.scheduled_date.date() - batch.start_date).days == day:
            return v
    return None

def _active_day_vaccine(day):
    v = vaccination_for_day(get_active_batch(), day)
    return v.vaccine_name if v else None

def get_day12_vaccine():
    return _active_day_vaccine(12)

def get_day16_vaccine():
    return _active_day_vaccine(16)

def get_monthly_sales_forecast():
    harvests = HarvestHistory.query.filter_by(is_archived=False).all()
    if len(harvests) < 10:
        return {"available": False, "reason": "Not enough harvest data yet.", "sample_count": len(harvests)}

    monthly_revenues = {}
    for h in harvests:
        month = h.end_date.strftime("%b") if h.end_date else "Jan"
        monthly_revenues.setdefault(month, []).append(h.loss_gain or 0)

    labels = [m for m in MONTH_ORDER if m in monthly_revenues]
    monthly_sales = [round(sum(monthly_revenues[m]) / len(monthly_revenues[m]), 2) for m in labels]
    best_idx = monthly_sales.index(max(monthly_sales)) if monthly_sales else 0

    return {
        "available": True, "labels": labels, "monthly_sales": monthly_sales,
        "best_month": labels[best_idx] if labels else "—",
        "best_value": monthly_sales[best_idx] if monthly_sales else 0,
        "sample_count": len(harvests)
    }

def generate_batch_name(custom_suffix):
    year = date.today().year
    existing = FlockBatch.query.filter(
        FlockBatch.batch_name.like(f"Batch-{year}-%")
    ).all()
    used_letters = set()
    for b in existing:
        m = re.match(rf"Batch-{year}-([A-Z])", b.batch_name or "")
        if m:
            used_letters.add(m.group(1))
    letter = next((c for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" if c not in used_letters), "Z")
    suffix = (custom_suffix or "").strip()
    base = f"Batch-{year}-{letter}"
    return f"{base} {suffix}".strip() if suffix else base

def record_growth_data(batch, user_id, record_date, avg_weight_g, feed_kg, feed_record_id, mortality, cull, cause):
    db.session.add(MortalityRecord(batch_id=batch.batch_id, user_id=user_id, death_count=mortality,
                                    cull_count=cull, cause=cause, record_date=record_date))

    if feed_record_id:
        db.session.add(DailyFeedRecord(batch_id=batch.batch_id, feed_record_id=feed_record_id,
                                        record_date=record_date, total_kg=feed_kg))
        feed = FeedRecord.query.get(feed_record_id)
        if feed:
            feed.remaining_quantity = max(0.0, (feed.remaining_quantity or 0) - feed_kg)

    batch.current_bird_count = max(0, batch.current_bird_count - mortality - cull)
    db.session.flush()

    age_days = max(0, (record_date - batch.start_date).days)
    first_w = (WeightRecord.query.filter_by(batch_id=batch.batch_id)
               .order_by(WeightRecord.record_date.asc(), WeightRecord.weight_id.asc()).first())
    starting_weight = first_w.total_weight_gain if first_w else 42.0
    adg_value = round((avg_weight_g - starting_weight) / age_days, 2) if age_days > 0 else 0.0
    adg = AdgCalculation(batch_id=batch.batch_id, user_id=user_id, starting_weight=starting_weight,
                          ending_weight=avg_weight_g, number_of_days=age_days,
                          record_date=record_date, adg_value=adg_value)
    db.session.add(adg)

    total_feed = db.session.query(func.sum(DailyFeedRecord.total_kg)).filter_by(batch_id=batch.batch_id).scalar() or 0.0
    total_weight_kg = round((avg_weight_g * batch.current_bird_count) / 1000.0, 2)
    fcr_value = round(total_feed / total_weight_kg, 2) if total_weight_kg > 0 else 0.0
    fcr = FcrCalculation(batch_id=batch.batch_id, user_id=user_id, total_feed_intake=round(total_feed, 2),
                          total_weight_gain=total_weight_kg, fcr_value=fcr_value)
    db.session.add(fcr)

    db.session.add(WeightRecord(batch_id=batch.batch_id, user_id=user_id, record_date=record_date,
                                 total_weight_gain=avg_weight_g, fcr_value=fcr_value))
    db.session.flush()

    db.session.add(FlockReport(batch_id=batch.batch_id, user_id=user_id,
                                adg_id=adg.calc_id, fcr_id=fcr.fcr_id, report_date=record_date))
    db.session.commit()
    return adg, fcr

def redirect_dashboard():
    role = session.get("role")
    if role == "Owner":
        return redirect(url_for("main.owner_dashboard"))
    if role == "Manager":
        return redirect(url_for("main.manager_dashboard"))
    return redirect(url_for("main.worker_dashboard"))

# ─── Auth Routes ────────────────────────────────────────────────────────────

@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        u = User.query.filter_by(username=request.form["username"]).first()
        if u and check_password_hash(u.password_hash, request.form["password"]):
            if not u.is_active:
                flash("This account has been deactivated. Contact the Owner.")
                return render_template_string(TEMPLATE_LOGIN)
            session.update({"user_id": u.user_id, "role": u.role, "full_name": u.full_name})
            return redirect(url_for("main.dashboard"))
        flash("Invalid credentials.")
    return render_template_string(TEMPLATE_LOGIN)

@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("main.login"))

@bp.route("/")
@bp.route("/dashboard")
@login_required
def dashboard():
    role = session.get("role")
    if role == "Owner": return redirect(url_for("main.owner_dashboard"))
    if role == "Manager": return redirect(url_for("main.manager_dashboard"))
    return redirect(url_for("main.worker_dashboard"))

@bp.route("/owner")
@login_required
@role_required("Owner")
def owner_dashboard():
    active_flocks = FlockBatch.query.filter_by(flock_status='Active').all()
    all_flocks = FlockBatch.query.order_by(FlockBatch.batch_id.desc()).all()
    totals = get_flock_totals(active_flocks)
    avg_market = get_current_avg_market_price()

    harvest_data = HarvestHistory.query.filter_by(is_archived=False).order_by(HarvestHistory.end_date.desc()).all()
    sort = request.args.get("sort", "highest")
    harvest_data_sorted = sorted(harvest_data, key=lambda h: h.loss_gain or 0, reverse=(sort != "lowest"))

    summary_reports_list = []
    for h in harvest_data:
        summary_reports_list.append({
            "report_id": h.id, "batch_name": h.batch_name, "age": h.age,
            "initial_count": h.initial_count, "harvest_count": h.harvest_count,
            "mortality_pct": h.mortality_pct,
            "start_date": h.start_date.strftime('%b %d, %Y') if h.start_date else '—',
            "harvest_date": h.end_date.strftime('%b %d, %Y') if h.end_date else '—',
            "adg": h.adg, "fcr": h.fcr, "lw": h.lw, "expenses": h.expenses,
            "cost_per_kg": round(h.expenses / ((h.harvest_count or 0) * (h.lw or 0) / 1000.0), 2)
                           if (h.harvest_count and h.lw) else None,
            "season": h.season, "chick_booster": h.chick_booster, "grower_pellets": h.grower_pellets,
            "finisher_pellets": h.finisher_pellets, "vaccine_day_12": h.vaccine_day_12,
            "vaccine_day_16": h.vaccine_day_16, "medicines": h.medicines,
            "loss_gain": h.loss_gain, "remarks": h.remarks,
        })

    all_market_prices = MarketPrice.query.filter_by(user_id=session["user_id"]).order_by(MarketPrice.record_date.desc(), MarketPrice.price_id.desc()).all()

    return render_template_string(TEMPLATE_OWNER,
        full_name=session["full_name"], today_str=date.today().isoformat(), current_year=date.today().year,
        expense_summary=get_expense_summary(), users=User.query.order_by(User.user_id).all(),
        flocks=all_flocks, active_flocks=active_flocks, total_birds=sum(f.current_bird_count for f in active_flocks),
        totals=totals, avg_market=avg_market, live_market=get_live_market_data(), all_market_prices=all_market_prices,
        harvest_chart_data=harvest_data_sorted, all_harvest_data=harvest_data_sorted, summary_reports_list=summary_reports_list,
        sales_forecast=get_monthly_sales_forecast(), flock_analytics=get_flock_analytics(active_flocks),
        profit_loss=get_profit_loss_summary(), harvest_profit_summary=get_harvest_profit_summary(),
        best_season=get_best_season_for_sales(), current_sort=sort,
    )

@bp.route("/manager")
@login_required
@role_required("Manager", "Owner")
def manager_dashboard():
    flocks = FlockBatch.query.order_by(FlockBatch.batch_id.desc()).all()
    active_flocks = FlockBatch.query.filter_by(flock_status='Active').all()
    totals = get_flock_totals(active_flocks)
    expense_summary = get_expense_summary()
    pending_submissions = DailyRecordSubmission.query.filter_by(status='Pending').order_by(DailyRecordSubmission.submitted_at.asc()).all()

    month_param = request.args.get("month")
    sel_year, sel_month = None, None
    if month_param:
        try:
            sel_year, sel_month = (int(p) for p in month_param.split("-"))
        except ValueError:
            sel_year, sel_month = None, None
    category_spending = get_category_spending(sel_year, sel_month)

    other_expenses_all = scoped_expenses(OtherExpense)
    other_by_category = {}
    for e in other_expenses_all:
        cat = e.category.category_name if e.category else "Uncategorized"
        other_by_category.setdefault(cat, []).append(e)

    # Check if vitamins and medicines have inventory
    has_vitamins = Vitamin.query.count() > 0
    has_medicines = Medicine.query.count() > 0

    return render_template_string(TEMPLATE_MANAGER,
        full_name=session["full_name"], today_str=date.today().isoformat(), flocks=flocks, active_flocks=active_flocks,
        totals=totals, vaccines=Vaccine.query.order_by(Vaccine.vaccine_name).all(),
        vaccination_records=VaccinationRecord.query.order_by(VaccinationRecord.scheduled_date.desc()).all(),
        vitamins=Vitamin.query.order_by(Vitamin.vitamin_name).all(),
        vitamin_schedules=VitaminSchedule.query.order_by(VitaminSchedule.scheduled_date.desc()).all(),
        feed_records=FeedRecord.query.order_by(FeedRecord.feed_category, FeedRecord.feed_name).all(),
        medicines=Medicine.query.order_by(Medicine.medicine_name).all(),
        medication_schedules=MedicationSchedule.query.order_by(MedicationSchedule.scheduled_date.desc()).all(),
        upcoming_schedule=get_upcoming_schedule(7), flock_analytics=get_flock_analytics(active_flocks),
        sales_forecast=get_monthly_sales_forecast(), day12_vaccine=get_day12_vaccine(),
        day16_vaccine=get_day16_vaccine(), next_vaccination=get_next_vaccination(), next_medication=get_next_medication(),
        medication_count=MedicationSchedule.query.filter_by(status='Scheduled').count(),
        expense_categories=ExpenseCategory.query.all(), water_expenses=scoped_expenses(WaterExpense),
        electricity_expenses=scoped_expenses(ElectricityExpense), lpg_expenses=scoped_expenses(LpgExpense),
        labor_expenses=scoped_expenses(LaborExpense), other_expenses=other_expenses_all,
        other_by_category=other_by_category, vaccine_expenses=scoped_expenses(VaccineExpense),
        feed_expenses=scoped_expenses(FeedExpense), chick_expenses=scoped_expenses(ChickExpense),
        batch_costs=[get_batch_cost_summary(f) for f in flocks], expense_summary=expense_summary,
        profit_loss=get_profit_loss_summary(), harvest_sales=HarvestSale.query.order_by(HarvestSale.sale_date.desc(), HarvestSale.sale_id.desc()).all(),
        pending_submissions=pending_submissions, category_spending=category_spending,
        harvest_history=HarvestHistory.query.filter_by(is_archived=False).order_by(HarvestHistory.end_date.desc()).all(),
        market_prices=MarketPrice.query.order_by(MarketPrice.record_date.desc()).all(),
        current_da_price=get_current_avg_market_price(),
        has_vitamins=has_vitamins, has_medicines=has_medicines,
    )

@bp.route("/worker")
@login_required
def worker_dashboard():
    active_batch = get_active_batch()
    my_submissions = DailyRecordSubmission.query.filter_by(user_id=session["user_id"]).order_by(DailyRecordSubmission.submitted_at.desc()).limit(15).all()
    my_weekly = WeeklyRecord.query.filter_by(user_id=session["user_id"]).order_by(WeeklyRecord.submitted_at.desc()).limit(10).all()
    
    can_submit_weekly = True
    if active_batch:
        last_weekly = WeeklyRecord.query.filter_by(batch_id=active_batch.batch_id).order_by(WeeklyRecord.record_date.desc()).first()
        if last_weekly:
            days_since = (date.today() - last_weekly.record_date).days
            can_submit_weekly = days_since >= 7
    
    current_week = 1
    if active_batch:
        current_week = max(1, (active_batch.age_days // 7) + 1)
    
    # Get feed records for the dropdowns
    feed_records = FeedRecord.query.order_by(FeedRecord.feed_category, FeedRecord.feed_name).all()
    
    return render_template_string(TEMPLATE_WORKER,
        full_name=session["full_name"], active_batch=active_batch, my_records=my_submissions,
        my_weekly=my_weekly, feed_records=feed_records,
        today_date=date.today().strftime('%Y-%m-%d'), can_submit_weekly=can_submit_weekly, current_week=current_week
    )

# ─── Owner Management: Accounts (Manager deactivation/deletion allowed) ─────

@bp.route("/owner/user/add", methods=["POST"])
@login_required
@role_required("Owner")
def add_user():
    if User.query.filter_by(username=request.form["username"]).first():
        flash("That username is already taken.")
        return redirect(url_for("main.owner_dashboard"))

    role = request.form["role"]
    if role not in ("Manager", "Worker"):
        flash("Only Manager or Worker accounts can be created here.")
        return redirect(url_for("main.owner_dashboard"))

    phone = (request.form.get("phone_num") or "").strip()
    if not re.fullmatch(r"09\d{9}", phone):
        flash("Phone number must be 11 digits and start with 09.")
        return redirect(url_for("main.owner_dashboard"))

    u = User(
        first_name=request.form["first_name"], middle_name=request.form.get("middle_name") or None,
        last_name=request.form["last_name"], phone_num=phone, bday=date(2000, 1, 1),
        username=request.form["username"], password_hash=generate_password_hash(request.form["password"]),
        role=role, is_active=True,
    )
    db.session.add(u)
    db.session.commit()
    flash(f"Account for {u.full_name} created.")
    return redirect(url_for("main.owner_dashboard"))

@bp.route("/owner/user/edit/<int:id>", methods=["POST"])
@login_required
@role_required("Owner")
def edit_user(id):
    u = User.query.get_or_404(id)
    u.first_name = request.form.get("first_name", u.first_name).strip()
    u.middle_name = (request.form.get("middle_name") or "").strip() or None
    u.last_name = request.form.get("last_name", u.last_name).strip()
    phone = (request.form.get("phone_num") or "").strip()
    if phone and not re.fullmatch(r"09\d{9}", phone):
        flash("Phone number must be 11 digits and start with 09.")
        return redirect(url_for("main.owner_dashboard"))
    u.phone_num = phone or None
    db.session.commit()
    flash(f"Updated {u.full_name}.")
    return redirect(url_for("main.owner_dashboard"))

@bp.route("/owner/user/reset-password/<int:id>", methods=["POST"])
@login_required
@role_required("Owner")
def reset_user_password(id):
    u = User.query.get_or_404(id)
    new_password = request.form.get("new_password")
    if new_password and len(new_password) >= 6:
        u.password_hash = generate_password_hash(new_password)
        db.session.commit()
        flash(f"Password reset for {u.full_name}.")
    else:
        flash("Password must be at least 6 characters.")
    return redirect(url_for("main.owner_dashboard"))

@bp.route("/owner/user/deactivate/<int:id>", methods=["POST"])
@login_required
@role_required("Owner")
def toggle_user_active(id):
    u = User.query.get_or_404(id)
    if u.username == "owner":
        flash("Cannot deactivate the Owner account.")
        return redirect(url_for("main.owner_dashboard"))
    u.is_active = not u.is_active
    db.session.commit()
    flash(f"{'Activated' if u.is_active else 'Deactivated'} {u.full_name}.")
    return redirect(url_for("main.owner_dashboard"))

@bp.route("/owner/user/delete/<int:id>", methods=["POST"])
@login_required
@role_required("Owner")
def delete_user(id):
    u = User.query.get_or_404(id)
    if u.username == "owner":
        flash("Cannot delete the Owner account.")
        return redirect(url_for("main.owner_dashboard"))
    db.session.delete(u)
    db.session.commit()
    flash("User deleted.")
    return redirect(url_for("main.owner_dashboard"))

# ─── Flock Management ───────────────────────────────────────────────────────

@bp.route("/owner/flock/add", methods=["POST"])
@login_required
@role_required("Owner")
def add_flock():
    existing_active = FlockBatch.query.filter_by(flock_status="Active").first()
    if existing_active:
        flash(f"'{existing_active.batch_name}' is still Active. Harvest it first.")
        return redirect(url_for("main.owner_dashboard"))

    count = int(request.form["initial_bird_count"])
    start_str = (request.form.get("start_date") or "").strip()
    target_str = (request.form.get("target_harvest_date") or "").strip()
    season = (request.form.get("season") or "").strip()

    if not start_str or not target_str:
        flash("Date of Arrival and Target Harvest Date are both required.")
        return redirect(url_for("main.owner_dashboard"))

    try:
        start_date = datetime.strptime(start_str, "%Y-%m-%d").date()
        target_date = datetime.strptime(target_str, "%Y-%m-%d").date()
    except ValueError:
        flash("Invalid date format.")
        return redirect(url_for("main.owner_dashboard"))

    if target_date <= start_date:
        flash("Target Harvest Date must be after arrival.")
        return redirect(url_for("main.owner_dashboard"))

    if season not in ("Dry", "Wet"):
        flash("Please select a Season of Arrival.")
        return redirect(url_for("main.owner_dashboard"))

    cost_per_bird = float(request.form.get("cost_per_bird") or 0.0)
    custom_suffix = request.form.get("batch_suffix") or ""

    f = FlockBatch(
        user_id=session["user_id"], batch_name=generate_batch_name(custom_suffix),
        initial_bird_count=count, current_bird_count=count,
        start_date=start_date, target_harvest_date=target_date, season=season,
    )
    db.session.add(f)
    db.session.flush()

    if cost_per_bird > 0 and count > 0:
        db.session.add(ChickExpense(
            batch_id=f.batch_id, quantity=count,
            chick_expense_amount=round(cost_per_bird * count, 2), chick_expense_status="Paid",
            expense_date=start_date, description=f"Day-old chicks - {count} heads @ ₱{cost_per_bird:.2f}/head"
        ))

    db.session.commit()
    flash(f"Flock '{f.batch_name}' created.")
    return redirect(url_for("main.owner_dashboard"))

@bp.route("/owner/flock/edit/<int:id>", methods=["POST"])
@login_required
@role_required("Owner")
def edit_flock(id):
    f = FlockBatch.query.get_or_404(id)
    if f.flock_status in ("Harvested", "Archived"):
        flash("This batch is harvested and can no longer be edited.")
        return redirect(url_for("main.owner_dashboard"))
    f.batch_name = request.form["batch_name"]
    f.flock_status = request.form.get("flock_status", f.flock_status)
    db.session.commit()
    flash(f"Flock '{f.batch_name}' updated.")
    return redirect(url_for("main.owner_dashboard"))

@bp.route("/owner/flock/archive/<int:id>", methods=["POST"])
@login_required
@role_required("Owner")
def archive_flock(id):
    f = FlockBatch.query.get_or_404(id)
    if f.flock_status != "Harvested":
        flash("Only harvested batches can be archived.")
        return redirect_dashboard()
    h = HarvestHistory.query.filter_by(batch_name=f.batch_name, start_date=f.start_date).first()
    if h:
        h.is_archived = True
    f.flock_status = "Archived"
    db.session.commit()
    flash(f"Batch '{f.batch_name}' has been archived.")
    return redirect_dashboard()

@bp.route("/manager/flock/harvest/<int:id>", methods=["POST"])
@login_required
@role_required("Manager", "Owner")
def harvest_flock(id):
    f = FlockBatch.query.get_or_404(id)
    if f.flock_status != "Active":
        flash("This batch is not active.")
        return redirect_dashboard()
    if not f.has_data:
        flash("Cannot harvest this batch — it has no recorded data yet.")
        return redirect_dashboard()

    price_basis = request.form.get("price_basis", "DA")
    if price_basis == "Given":
        given_id = request.form.get("given_price_id")
        chosen = MarketPrice.query.get(int(given_id)) if given_id else None
        basis_value = chosen.price_per_kg if chosen else get_current_avg_market_price()
    else:
        basis_value = get_current_avg_market_price()

    harvest_season = request.form.get("harvest_season", f.season or "Dry")

    snap = get_batch_snapshot(f)
    batch_expenses = get_batch_expense_total(f.batch_id)
    batch_revenue = db.session.query(func.sum(HarvestSale.total_amount)).filter_by(batch_id=f.batch_id).scalar() or 0.0

    day12_vax = vaccination_for_day(f, 12)
    day16_vax = vaccination_for_day(f, 16)

    harvest = HarvestHistory(
        batch_name=f.batch_name, start_date=f.start_date, end_date=date.today(),
        age=snap["age_days"], initial_count=f.initial_bird_count,
        harvest_count=f.current_bird_count, mortality_pct=f.mortality_percentage,
        total_deaths=f.mortality_count, culled=0, adg=snap["adg_value"],
        fcr=snap["fcr_value"], lw=snap["latest_weight_g"], expenses=batch_expenses,
        season=harvest_season,  # Season of harvest identified by the manager
        vaccine_day_12=day12_vax.vaccine_name if day12_vax else None,
        vaccine_day_16=day16_vax.vaccine_name if day16_vax else None,
        loss_gain=round(batch_revenue - batch_expenses, 2),
        price_basis=price_basis, price_basis_value=basis_value,
        remarks="Batch harvested and archived."
    )
    db.session.add(harvest)
    f.flock_status = "Harvested"
    db.session.commit()
    flash(f"Batch '{f.batch_name}' harvested in {harvest_season} season.")
    return redirect_dashboard()

@bp.route("/owner/flock/delete/<int:id>", methods=["POST"])
@login_required
@role_required("Owner")
def delete_flock(id):
    f = FlockBatch.query.get_or_404(id)
    db.session.delete(f)
    db.session.commit()
    flash("Flock deleted.")
    return redirect(url_for("main.owner_dashboard"))

# ─── Market Prices & Expenses ───────────────────────────────────────────────

@bp.route("/owner/market-price/add", methods=["POST"])
@login_required
@role_required("Owner")
def add_market_price():
    date_str = request.form.get("record_date")
    rec_date = datetime.strptime(date_str, "%Y-%m-%d").date() if date_str else date.today()
    mp = MarketPrice(user_id=session["user_id"], record_date=rec_date,
                     price_per_kg=float(request.form["price_per_kg"]), location=request.form.get("location"))
    db.session.add(mp)
    db.session.commit()
    flash("Price recorded.")
    return redirect(url_for("main.owner_dashboard"))

@bp.route("/owner/expense-category/add", methods=["POST"])
@login_required
@role_required("Owner", "Manager")
def add_expense_category():
    name = request.form.get("category_name", "").strip()
    if name:
        db.session.add(ExpenseCategory(user_id=session["user_id"], category_name=name))
        db.session.commit()
    return redirect_dashboard()

@bp.route("/owner/expense-category/delete/<int:id>", methods=["POST"])
@login_required
@role_required("Owner", "Manager")
def delete_expense_category(id):
    db.session.delete(ExpenseCategory.query.get_or_404(id))
    db.session.commit()
    return redirect_dashboard()

# Expense Add/Toggle/Delete Routes (Water, Electricity, LPG, Labor, Other, Chick, Feed, Vaccine)
@bp.route("/owner/expense/water/add", methods=["POST"])
@login_required
@role_required("Owner", "Manager")
def add_water_expense():
    cat = get_or_create_category("Water")
    active = get_active_batch()
    if not active: return redirect_dashboard()
    db.session.add(WaterExpense(expense_category_id=cat.expense_category_id, batch_id=active.batch_id,
                                water_expense_amount=float(request.form["amount"]), water_expense_status=request.form.get("status", "Pending"), expense_date=parse_expense_date(request.form)))
    db.session.commit()
    return redirect_dashboard()

@bp.route("/owner/expense/water/toggle/<int:id>", methods=["POST"])
@login_required
@role_required("Owner", "Manager")
def toggle_water_expense(id):
    e = WaterExpense.query.get_or_404(id)
    e.water_expense_status = "Paid" if e.water_expense_status != "Paid" else "Pending"
    db.session.commit()
    return redirect_dashboard()

@bp.route("/owner/expense/water/delete/<int:id>", methods=["POST"])
@login_required
@role_required("Owner", "Manager")
def delete_water_expense(id):
    db.session.delete(WaterExpense.query.get_or_404(id))
    db.session.commit()
    return redirect_dashboard()

@bp.route("/owner/expense/electricity/add", methods=["POST"])
@login_required
@role_required("Owner", "Manager")
def add_electricity_expense():
    cat = get_or_create_category("Electricity")
    active = get_active_batch()
    if not active: return redirect_dashboard()
    db.session.add(ElectricityExpense(expense_category_id=cat.expense_category_id, batch_id=active.batch_id,
                                      electricity_expense_amount=float(request.form["amount"]), electricity_expense_status=request.form.get("status", "Pending"), expense_date=parse_expense_date(request.form)))
    db.session.commit()
    return redirect_dashboard()

@bp.route("/owner/expense/electricity/toggle/<int:id>", methods=["POST"])
@login_required
@role_required("Owner", "Manager")
def toggle_electricity_expense(id):
    e = ElectricityExpense.query.get_or_404(id)
    e.electricity_expense_status = "Paid" if e.electricity_expense_status != "Paid" else "Pending"
    db.session.commit()
    return redirect_dashboard()

@bp.route("/owner/expense/electricity/delete/<int:id>", methods=["POST"])
@login_required
@role_required("Owner", "Manager")
def delete_electricity_expense(id):
    db.session.delete(ElectricityExpense.query.get_or_404(id))
    db.session.commit()
    return redirect_dashboard()

@bp.route("/owner/expense/lpg/add", methods=["POST"])
@login_required
@role_required("Owner", "Manager")
def add_lpg_expense():
    cat = get_or_create_category("LPG")
    active = get_active_batch()
    if not active: return redirect_dashboard()
    db.session.add(LpgExpense(expense_category_id=cat.expense_category_id, batch_id=active.batch_id,
                              lpg_expense_amount=float(request.form["amount"]), lpg_provider=request.form.get("lpg_provider"), lpg_expense_status=request.form.get("status", "Pending"), expense_date=parse_expense_date(request.form)))
    db.session.commit()
    return redirect_dashboard()

@bp.route("/owner/expense/lpg/toggle/<int:id>", methods=["POST"])
@login_required
@role_required("Owner", "Manager")
def toggle_lpg_expense(id):
    e = LpgExpense.query.get_or_404(id)
    e.lpg_expense_status = "Paid" if e.lpg_expense_status != "Paid" else "Pending"
    db.session.commit()
    return redirect_dashboard()

@bp.route("/owner/expense/lpg/delete/<int:id>", methods=["POST"])
@login_required
@role_required("Owner", "Manager")
def delete_lpg_expense(id):
    db.session.delete(LpgExpense.query.get_or_404(id))
    db.session.commit()
    return redirect_dashboard()

@bp.route("/owner/expense/labor/add", methods=["POST"])
@login_required
@role_required("Owner", "Manager")
def add_labor_expense():
    cat = get_or_create_category("Labor")
    active = get_active_batch()
    if not active: return redirect_dashboard()
    db.session.add(LaborExpense(expense_category_id=cat.expense_category_id, batch_id=active.batch_id,
                                labor_expense_amount=float(request.form["amount"]), labor_expense_status=request.form.get("status", "Pending"), expense_date=parse_expense_date(request.form)))
    db.session.commit()
    return redirect_dashboard()

@bp.route("/owner/expense/labor/toggle/<int:id>", methods=["POST"])
@login_required
@role_required("Owner", "Manager")
def toggle_labor_expense(id):
    e = LaborExpense.query.get_or_404(id)
    e.labor_expense_status = "Paid" if e.labor_expense_status != "Paid" else "Pending"
    db.session.commit()
    return redirect_dashboard()

@bp.route("/owner/expense/labor/delete/<int:id>", methods=["POST"])
@login_required
@role_required("Owner", "Manager")
def delete_labor_expense(id):
    db.session.delete(LaborExpense.query.get_or_404(id))
    db.session.commit()
    return redirect_dashboard()

@bp.route("/owner/expense/other/add", methods=["POST"])
@login_required
@role_required("Owner", "Manager")
def add_other_expense():
    active = get_active_batch()
    if not active: return redirect_dashboard()
    db.session.add(OtherExpense(user_id=session["user_id"], expense_category_id=int(request.form["expense_category_id"]),
                                batch_id=active.batch_id, other_expense_amount=float(request.form["amount"]), other_expense_status=request.form.get("status", "Pending"), expense_date=parse_expense_date(request.form)))
    db.session.commit()
    return redirect_dashboard()

@bp.route("/owner/expense/other/toggle/<int:id>", methods=["POST"])
@login_required
@role_required("Owner", "Manager")
def toggle_other_expense(id):
    e = OtherExpense.query.get_or_404(id)
    e.other_expense_status = "Paid" if e.other_expense_status != "Paid" else "Pending"
    db.session.commit()
    return redirect_dashboard()

@bp.route("/owner/expense/other/delete/<int:id>", methods=["POST"])
@login_required
@role_required("Owner", "Manager")
def delete_other_expense(id):
    db.session.delete(OtherExpense.query.get_or_404(id))
    db.session.commit()
    return redirect_dashboard()

@bp.route("/manager/expenses/history")
@login_required
@role_required("Manager", "Owner")
def expense_history():
    active = get_active_batch()
    batches = [b for b in FlockBatch.query.order_by(FlockBatch.start_date.desc()).all() if not active or b.batch_id != active.batch_id]
    sel_id = request.args.get("batch_id", type=int)
    selected = next((b for b in batches if b.batch_id == sel_id), batches[0] if batches else None)
    return render_template_string(
        TEMPLATE_EXPENSE_HISTORY,
        batches=batches, selected=selected,
        rows=get_batch_expense_rows(selected.batch_id) if selected else [],
        summary=get_batch_cost_summary(selected) if selected else None,
        back_url=url_for("main.owner_dashboard") if session.get("role") == "Owner" else url_for("main.manager_dashboard"),
    )

@bp.route("/manager/chick-expense/add", methods=["POST"])
@login_required
@role_required("Owner", "Manager")
def add_chick_expense():
    active = get_active_batch()
    if not active: return redirect_dashboard()
    qty = int(request.form.get("quantity") or active.initial_bird_count or 0)
    amount = round(float(request.form.get("amount") or 0), 2)
    db.session.add(ChickExpense(batch_id=active.batch_id, quantity=qty, chick_expense_amount=amount,
                                chick_expense_status=request.form.get("status", "Paid"), expense_date=parse_expense_date(request.form), description=f"Day-old chicks - {qty} heads"))
    db.session.commit()
    return redirect_dashboard()

@bp.route("/manager/chick-expense/toggle/<int:id>", methods=["POST"])
@login_required
@role_required("Owner", "Manager")
def toggle_chick_expense(id):
    e = ChickExpense.query.get_or_404(id)
    e.chick_expense_status = "Paid" if e.chick_expense_status != "Paid" else "Pending"
    db.session.commit()
    return redirect_dashboard()

@bp.route("/manager/chick-expense/delete/<int:id>", methods=["POST"])
@login_required
@role_required("Owner", "Manager")
def delete_chick_expense(id):
    e = ChickExpense.query.get_or_404(id)
    bid = e.batch_id
    db.session.delete(e)
    db.session.flush()
    recalc_harvest_profit(bid)
    db.session.commit()
    return redirect_dashboard()

@bp.route("/manager/feed-expense/add", methods=["POST"])
@login_required
@role_required("Owner", "Manager")
def add_feed_expense():
    active = get_active_batch()
    if not active: return redirect_dashboard()
    fr_id = request.form.get("feed_record_id")
    feed = FeedRecord.query.get(int(fr_id)) if fr_id else None
    db.session.add(FeedExpense(feed_record_id=feed.feed_record_id if feed else None, batch_id=active.batch_id,
                               feed_expense_amount=round(float(request.form["amount"]), 2), feed_expense_status=request.form.get("status", "Paid"), expense_date=parse_expense_date(request.form), description=feed.feed_name if feed else "Feed purchase"))
    db.session.commit()
    return redirect_dashboard()

@bp.route("/manager/feed-expense/toggle/<int:id>", methods=["POST"])
@login_required
@role_required("Owner", "Manager")
def toggle_feed_expense(id):
    e = FeedExpense.query.get_or_404(id)
    e.feed_expense_status = "Paid" if e.feed_expense_status != "Paid" else "Pending"
    db.session.commit()
    return redirect_dashboard()

@bp.route("/manager/feed-expense/delete/<int:id>", methods=["POST"])
@login_required
@role_required("Owner", "Manager")
def delete_feed_expense(id):
    e = FeedExpense.query.get_or_404(id)
    bid = e.batch_id
    db.session.delete(e)
    db.session.flush()
    recalc_harvest_profit(bid)
    db.session.commit()
    return redirect_dashboard()

@bp.route("/manager/vaccine-expense/add", methods=["POST"])
@login_required
@role_required("Owner", "Manager")
def add_vaccine_expense():
    active = get_active_batch()
    if not active: return redirect_dashboard()
    vid = request.form.get("vaccine_id")
    vac = Vaccine.query.get(int(vid)) if vid else None
    db.session.add(VaccineExpense(vaccine_id=vac.vaccine_id if vac else None, batch_id=active.batch_id,
                                  vaccine_expense_amount=round(float(request.form["amount"]), 2), vaccine_expense_status=request.form.get("status", "Paid"), expense_date=parse_expense_date(request.form), description=vac.vaccine_name if vac else "Vaccine purchase"))
    db.session.commit()
    return redirect_dashboard()

@bp.route("/manager/vaccine-expense/toggle/<int:id>", methods=["POST"])
@login_required
@role_required("Owner", "Manager")
def toggle_vaccine_expense(id):
    e = VaccineExpense.query.get_or_404(id)
    e.vaccine_expense_status = "Paid" if e.vaccine_expense_status != "Paid" else "Pending"
    db.session.commit()
    return redirect_dashboard()

@bp.route("/manager/vaccine-expense/delete/<int:id>", methods=["POST"])
@login_required
@role_required("Owner", "Manager")
def delete_vaccine_expense(id):
    e = VaccineExpense.query.get_or_404(id)
    bid = e.batch_id
    db.session.delete(e)
    db.session.flush()
    recalc_harvest_profit(bid)
    db.session.commit()
    return redirect_dashboard()

@bp.route("/manager/sale/add", methods=["POST"])
@login_required
@role_required("Owner", "Manager")
def add_harvest_sale():
    kg_sold = float(request.form["kg_sold"])
    price_per_kg = float(request.form["price_per_kg"])
    s = HarvestSale(
        batch_id=int(request.form["batch_id"]), user_id=session["user_id"],
        sale_date=datetime.strptime(request.form["sale_date"], "%Y-%m-%d").date() if request.form.get("sale_date") else date.today(),
        kg_sold=kg_sold, price_per_kg=price_per_kg, total_amount=round(kg_sold * price_per_kg, 2),
        buyer=request.form.get("buyer") or None, remarks=request.form.get("remarks") or None
    )
    db.session.add(s)
    db.session.flush()
    recalc_harvest_profit(s.batch_id)
    db.session.commit()
    return redirect_dashboard()

@bp.route("/manager/sale/delete/<int:id>", methods=["POST"])
@login_required
@role_required("Owner", "Manager")
def delete_harvest_sale(id):
    s = HarvestSale.query.get_or_404(id)
    bid = s.batch_id
    db.session.delete(s)
    db.session.flush()
    recalc_harvest_profit(bid)
    db.session.commit()
    return redirect_dashboard()

# ─── Vaccination Management (Manual Vaccine Name) ───────────────────────────

@bp.route("/manager/vaccine/add", methods=["POST"])
@login_required
@role_required("Manager", "Owner")
def add_vaccine():
    v = Vaccine(
        user_id=session["user_id"], vaccine_name=request.form["vaccine_name"],
        vaccine_type=request.form.get("vaccine_type"),
        vaccine_exp_date=datetime.strptime(request.form["vaccine_exp_date"], "%Y-%m-%d").date() if request.form.get("vaccine_exp_date") else None,
        milliliters_per_bottle=float(request.form.get("milliliters_per_bottle", 0) or 0),
        remaining_quantity=float(request.form.get("remaining_quantity", 0) or 0),
    )
    db.session.add(v)
    db.session.commit()
    return redirect(url_for("main.manager_dashboard"))

@bp.route("/manager/vaccination/schedule", methods=["POST"])
@login_required
@role_required("Manager", "Owner")
def schedule_vaccination():
    back = redirect(url_for("main.manager_dashboard"))
    batch = FlockBatch.query.get(int(request.form["batch_id"])) if request.form.get("batch_id") else None
    if not batch or batch.flock_status != "Active":
        flash("Pick an active flock batch.")
        return back
    try:
        at = datetime.strptime(request.form.get("schedule_time") or "08:00", "%H:%M").time()
    except ValueError:
        at = datetime.strptime("08:00", "%H:%M").time()

    administered_by = (request.form.get("administered_by") or "").strip() or None

    made, skipped = [], []
    for day in (12, 16):
        # Manual vaccine name input takes precedence over dropdown
        manual_name = (request.form.get(f"vaccine_name_manual_{day}") or "").strip()
        vname = manual_name if manual_name else request.form.get(f"vaccine_name_{day}")
        if not vname:
            continue
        if vaccination_for_day(batch, day):
            skipped.append(day)
            continue
        db.session.add(VaccinationRecord(
            batch_id=batch.batch_id, vaccine_name=vname.strip(), user_id=session["user_id"],
            dose_per_bird=float(request.form.get(f"dose_{day}", 0) or 0),
            administered_by=administered_by,
            scheduled_date=datetime.combine(batch.start_date + timedelta(days=day), at),
            status="Scheduled"))
        made.append(day)
    db.session.commit()
    if made:
        flash("Scheduled " + " and ".join(f"Day {d}" for d in made) + f" vaccination for {batch.batch_name}.")
    return back

@bp.route("/manager/vaccination/administer/<int:id>", methods=["POST"])
@login_required
@role_required("Manager", "Owner")
def administer_vaccination(id):
    v = VaccinationRecord.query.get_or_404(id)
    v.status = "Administered"
    v.administered_by = (request.form.get("administered_by") or "").strip() or session["full_name"]
    db.session.commit()
    return redirect(url_for("main.manager_dashboard"))

@bp.route("/manager/vaccination/delete/<int:id>", methods=["POST"])
@login_required
@role_required("Manager", "Owner")
def delete_vaccination(id):
    db.session.delete(VaccinationRecord.query.get_or_404(id))
    db.session.commit()
    return redirect(url_for("main.manager_dashboard"))

# ─── Vitamin Management & Inventory Check ───────────────────────────────────

@bp.route("/manager/vitamin/add", methods=["POST"])
@login_required
@role_required("Manager", "Owner")
def add_vitamin():
    db.session.add(Vitamin(
        user_id=session["user_id"], vitamin_name=request.form["vitamin_name"],
        vitamin_type=request.form.get("vitamin_type"),
        vitamin_exp_date=datetime.strptime(request.form["vitamin_exp_date"], "%Y-%m-%d").date() if request.form.get("vitamin_exp_date") else None,
        quantity=float(request.form.get("quantity", 0) or 0), unit=request.form.get("unit"),
    ))
    db.session.commit()
    return redirect(url_for("main.manager_dashboard"))

@bp.route("/manager/vitamin/schedule", methods=["POST"])
@login_required
@role_required("Manager", "Owner")
def schedule_vitamin():
    if Vitamin.query.count() == 0:
        flash("Vitamin inventory is empty. Cannot schedule vitamins.")
        return redirect(url_for("main.manager_dashboard"))
    
    vitamin_id = int(request.form["vitamin_id"])
    qty_used = float(request.form.get("quantity_used", 0) or 0)
    v = Vitamin.query.get(vitamin_id)
    if v and qty_used > 0:
        v.quantity = max(0.0, (v.quantity or 0) - qty_used)
    
    db.session.add(VitaminSchedule(
        batch_id=int(request.form["batch_id"]), vitamin_id=vitamin_id, user_id=session["user_id"],
        day_given=int(request.form["day_given"]), dosage=request.form.get("dosage"),
        scheduled_date=datetime.utcnow() + timedelta(days=int(request.form["day_given"])),
        status="Scheduled", quantity_used=qty_used
    ))
    db.session.commit()
    return redirect(url_for("main.manager_dashboard"))

@bp.route("/manager/vitamin/administer/<int:id>", methods=["POST"])
@login_required
@role_required("Manager", "Owner")
def administer_vitamin(id):
    v = VitaminSchedule.query.get_or_404(id)
    v.status = "Administered"
    v.administered_by = session["full_name"]
    db.session.commit()
    return redirect(url_for("main.manager_dashboard"))

@bp.route("/manager/vitamin/delete/<int:id>", methods=["POST"])
@login_required
@role_required("Manager", "Owner")
def delete_vitamin_schedule(id):
    v = VitaminSchedule.query.get_or_404(id)
    if v.status == "Scheduled" and v.quantity_used > 0:
        vit = Vitamin.query.get(v.vitamin_id)
        if vit: vit.quantity = (vit.quantity or 0) + v.quantity_used
    db.session.delete(v)
    db.session.commit()
    return redirect(url_for("main.manager_dashboard"))

# ─── Medicine Inventory & Scheduling ───────────────────────────────────────

@bp.route("/manager/medicine-inventory/add", methods=["POST"])
@login_required
@role_required("Manager", "Owner")
def add_medicine():
    db.session.add(Medicine(
        user_id=session["user_id"], medicine_name=request.form["medicine_name"].strip(),
        medicine_type=request.form.get("medicine_type"),
        medicine_exp_date=datetime.strptime(request.form["medicine_exp_date"], "%Y-%m-%d").date() if request.form.get("medicine_exp_date") else None,
        quantity=float(request.form.get("quantity", 0) or 0), unit=request.form.get("unit"),
    ))
    db.session.commit()
    return redirect(url_for("main.manager_dashboard"))

@bp.route("/manager/medicine/schedule", methods=["POST"])
@login_required
@role_required("Manager", "Owner")
def schedule_medicine():
    if Medicine.query.count() == 0:
        flash("Medicine inventory is empty. Cannot schedule medicines.")
        return redirect(url_for("main.manager_dashboard"))
    
    med = Medicine.query.get(int(request.form["medicine_id"])) if request.form.get("medicine_id") else None
    qty_used = float(request.form.get("quantity_used", 0) or 0)
    if med and qty_used > 0:
        med.quantity = max(0.0, (med.quantity or 0) - qty_used)

    db.session.add(MedicationSchedule(
        batch_id=int(request.form["batch_id"]), user_id=session["user_id"],
        item_name=med.medicine_name if med else "Medicine", item_type="Medicine",
        dosage=request.form.get("dosage"), scheduled_date=datetime.utcnow(),
        status="Scheduled", notes=request.form.get("notes"), quantity_used=qty_used
    ))
    db.session.commit()
    return redirect(url_for("main.manager_dashboard"))

@bp.route("/manager/medicine/administer/<int:id>", methods=["POST"])
@login_required
@role_required("Manager", "Owner")
def administer_medicine(id):
    m = MedicationSchedule.query.get_or_404(id)
    m.status = "Administered"
    m.administered_by = session["full_name"]
    db.session.commit()
    return redirect(url_for("main.manager_dashboard"))

@bp.route("/manager/medicine/delete/<int:id>", methods=["POST"])
@login_required
@role_required("Manager", "Owner")
def delete_medicine_schedule(id):
    m = MedicationSchedule.query.get_or_404(id)
    if m.status == "Scheduled" and m.quantity_used > 0:
        med = Medicine.query.filter_by(medicine_name=m.item_name).first()
        if med: med.quantity = (med.quantity or 0) + m.quantity_used
    db.session.delete(m)
    db.session.commit()
    return redirect(url_for("main.manager_dashboard"))

# ─── Feed Inventory ─────────────────────────────────────────────────────────

@bp.route("/manager/feed/add", methods=["POST"])
@login_required
@role_required("Manager", "Owner")
def add_feed_record():
    f = FeedRecord(
        user_id=session["user_id"], feed_name=request.form["feed_name"],
        feed_category=request.form["feed_category"],
        expiration_date=datetime.strptime(request.form["expiration_date"], "%Y-%m-%d").date() if request.form.get("expiration_date") else None,
        remaining_quantity=float(request.form.get("remaining_quantity", 0) or 0),
    )
    for field in FEED_NUTRIENT_FIELDS:
        setattr(f, field, float(request.form.get(field, 0) or 0))
    db.session.add(f)
    db.session.commit()
    return redirect(url_for("main.manager_dashboard"))

# ─── Worker Daily & Weekly Submissions ──────────────────────────────────────

@bp.route("/worker/record/add", methods=["POST"])
@login_required
def worker_add_record():
    active = get_active_batch()
    if not active:
        flash("No active flock batch.")
        return redirect(url_for("main.worker_dashboard"))

    feed_record_id = request.form.get("feed_record_id")
    s = DailyRecordSubmission(
        batch_id=active.batch_id, user_id=session["user_id"],
        record_date=datetime.strptime(request.form["record_date"], "%Y-%m-%d").date(),
        avg_weight_g=float(request.form.get("avg_weight", 0) or 0),
        mortality=int(request.form.get("mortality", 0) or 0), cull=0,
        cause=request.form.get("cause"),
        feed_kg=float(request.form.get("feed_consumed", 0) or 0),
        feed_record_id=int(feed_record_id) if feed_record_id else None,
        status="Pending"
    )
    db.session.add(s)
    db.session.commit()
    flash("Daily record submitted for Manager verification.")
    return redirect(url_for("main.worker_dashboard"))

@bp.route("/worker/weekly/add", methods=["POST"])
@login_required
def worker_add_weekly():
    active = get_active_batch()
    if not active: return redirect(url_for("main.worker_dashboard"))
    
    total_weight = float(request.form.get("total_weight_sample", 0) or 0)
    total_birds = int(request.form.get("total_birds_weighed", 0) or 0)
    avg_weight = round(total_weight / total_birds, 2) if total_birds > 0 else 0.0
    
    db.session.add(WeeklyRecord(
        batch_id=active.batch_id, user_id=session["user_id"],
        week_number=int(request.form.get("week_number", 1)),
        total_weight_sample=total_weight, total_birds_weighed=total_birds,
        avg_bird_weight=avg_weight, record_date=date.today(), status="Pending"
    ))
    db.session.commit()
    flash("Weekly record submitted.")
    return redirect(url_for("main.worker_dashboard"))

@bp.route("/manager/submission/approve/<int:id>", methods=["POST"])
@login_required
@role_required("Manager", "Owner")
def approve_submission(id):
    s = DailyRecordSubmission.query.get_or_404(id)
    if s.status != "Pending": return redirect_dashboard()
    record_growth_data(s.batch, s.user_id, s.record_date, s.avg_weight_g, s.feed_kg,
                        s.feed_record_id, s.mortality, s.cull, s.cause)
    s.status = "Verified"
    s.reviewed_by = session["user_id"]
    s.reviewed_at = datetime.utcnow()
    db.session.commit()
    flash("Submission verified and applied.")
    return redirect_dashboard()

@bp.route("/manager/submission/reject/<int:id>", methods=["POST"])
@login_required
@role_required("Manager", "Owner")
def reject_submission(id):
    s = DailyRecordSubmission.query.get_or_404(id)
    s.status = "Rejected"
    s.reviewed_by = session["user_id"]
    s.reviewed_at = datetime.utcnow()
    s.review_notes = request.form.get("review_notes")
    db.session.commit()
    flash("Submission rejected.")
    return redirect_dashboard()

# ─── Performance Report Print ───────────────────────────────────────────────

@bp.route("/report/<int:id>/print")
@login_required
def print_performance_report(id):
    h = HarvestHistory.query.get_or_404(id)
    report = {
        "batch": {"batch_name": h.batch_name, "start_date": h.start_date},
        "end_date": h.end_date.strftime('%d-%m-%Y') if h.end_date else '—',
        "age": h.age, "initial_count": h.initial_count, "harvest_count": h.harvest_count,
        "mortality_pct": h.mortality_pct, "total_deaths": h.total_deaths, "culled": h.culled,
        "adg": h.adg, "fcr": h.fcr, "lw": h.lw, "expenses": h.expenses, "season": h.season,
        "chick_booster": h.chick_booster, "grower_pellets": h.grower_pellets, "finisher_pellets": h.finisher_pellets,
        "vaccine_day_12": h.vaccine_day_12, "vaccine_day_16": h.vaccine_day_16,
        "medicines": h.medicines, "loss_gain": h.loss_gain, "remarks": h.remarks,
        "price_basis": getattr(h, 'price_basis', 'DA'), "price_basis_value": getattr(h, 'price_basis_value', 0),
    }

    batch = FlockBatch.query.filter_by(batch_name=h.batch_name, start_date=h.start_date).first()
    expense_types = []
    if batch:
        cs = get_batch_cost_summary(batch)
        for key, label in [("chicks", "Chicks"), ("feed", "Feed"), ("vaccine", "Vaccine"), ("water", "Water"),
                           ("electricity", "Electricity"), ("lpg", "LPG"), ("labor", "Labor"), ("other", "Other")]:
            amt = cs["parts"][key]
            expense_types.append({"type": label, "amount": amt, "pct": round(amt / cs["total"] * 100, 1) if cs["total"] else 0.0})
        report["expense_types_total"] = cs["total"]
    report["expense_types"] = expense_types

    return render_template_string(
        TEMPLATE_PERFORMANCE_REPORT_PRINT, report=report,
        selected_fields=["batch_name", "age", "initial_count", "harvest_count", "mortality_pct", "start_date", "harvest_date", "adg", "fcr", "lw", "expenses", "expense_types", "season", "loss_gain", "remarks"]
    )