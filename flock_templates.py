# flock_templates.py - COMPLETE REVISION v6
##############################################################################
# FlockIQ Poultry Farm Management System — Templates
##############################################################################

_BASE_STYLE = """
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.4/dist/chart.umd.min.js"></script>
<style>
:root {
  --bg: #fdfcfb; --sidebar-bg: #ffffff; --card-bg: #ffffff; --text: #1c1917;
  --muted: #78716c; --border: rgba(120, 113, 108, 0.12); --sidebar-hover: #f5f5f4;
  --sidebar-active-bg: #f0fdf4; --sidebar-active-text: #166534;
  --accent: #166534; --accent2: #854d0e; --green: #15803d; --blue: #1e40af;
  --red: #991b1b; --yellow: #a16207;
  --shadow: 0 1px 3px rgba(0,0,0,0.05), 0 4px 12px rgba(22, 101, 52, 0.04);
  --shadow-lg: 0 10px 25px rgba(22, 101, 52, 0.08);
}
html.dark {
  --bg: #0c0a09; --sidebar-bg: #1c1917; --card-bg: #292524; --text: #f5f5f4;
  --muted: #a8a29e; --border: rgba(255,255,255,0.08); --sidebar-hover: #292524;
  --sidebar-active-bg: #14532d; --sidebar-active-text: #bbf7d0;
  --shadow: 0 4px 20px rgba(0,0,0,0.4);
}
*, *::before, *::after { box-sizing: border-box; }
body { background: var(--bg); color: var(--text); font-family: 'Inter', sans-serif; margin: 0; min-height: 100vh; transition: background 0.25s, color 0.25s; }
.app-shell { display: flex; min-height: 100vh; }
.sidebar { width: 268px; flex-shrink: 0; background: var(--sidebar-bg); border-right: 1px solid var(--border); display: flex; flex-direction: column; position: sticky; top: 0; height: 100vh; overflow-y: auto; z-index: 100; transition: transform 0.3s cubic-bezier(.4,0,.2,1); }
.sidebar-brand { padding: 24px 20px 16px; border-bottom: 1px solid var(--border); display: flex; align-items: center; gap: 12px; }
.brand-icon { width: 40px; height: 40px; border-radius: 10px; background: linear-gradient(135deg, #166534, #15803d); display: flex; align-items: center; justify-content: center; color: #fff; font-size: 18px; flex-shrink: 0; }
.brand-text { font-family: 'Inter', sans-serif; font-size: 15px; font-weight: 800; line-height: 1.2; }
.brand-sub { font-size: 11px; color: var(--muted); font-weight: 500; }
.sidebar-nav { padding: 16px 12px; flex: 1; }
.nav-section-label { font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: 1.2px; color: var(--muted); padding: 12px 8px 6px; }
.nav-link { display: flex; align-items: center; gap: 10px; padding: 10px 12px; border-radius: 9px; margin-bottom: 2px; color: var(--text); font-size: 14px; font-weight: 500; text-decoration: none; transition: all 0.15s; cursor: pointer; }
.nav-link:hover { background: var(--sidebar-hover); color: var(--accent); }
.nav-link.active { background: var(--sidebar-active-bg); color: var(--sidebar-active-text); font-weight: 700; }
.nav-link i { width: 20px; text-align: center; font-size: 14px; }
.badge-count { margin-left: auto; background: #dc2626; color: #fff; font-size: 11px; font-weight: 700; padding: 1px 7px; border-radius: 999px; line-height: 1.6; }
.sidebar-footer { padding: 16px 12px; border-top: 1px solid var(--border); }
.logout-btn { display: flex; align-items: center; gap: 10px; padding: 10px 12px; border-radius: 9px; color: #991b1b; font-size: 14px; font-weight: 600; text-decoration: none; transition: all 0.15s; width: 100%; background: none; border: none; cursor: pointer; }
.logout-btn:hover { background: rgba(153, 27, 27, 0.08); color: #991b1b; }
.main-content { flex: 1; overflow-x: hidden; }
.topbar { background: var(--sidebar-bg); border-bottom: 1px solid var(--border); padding: 14px 28px; display: flex; justify-content: space-between; align-items: center; position: sticky; top: 0; z-index: 50; }
.topbar-title { font-family: 'Inter', sans-serif; font-size: 18px; font-weight: 800; color: var(--accent); }
.topbar-actions { display: flex; align-items: center; gap: 10px; }
.page-body { padding: 28px; }
.tab-content { display: none; }
.tab-content.active { display: block; animation: fadeIn 0.3s ease; }
@keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
.card { background: var(--card-bg); border: 1px solid var(--border); border-radius: 14px; box-shadow: var(--shadow); }
.card-header-custom { padding: 18px 22px 0; font-size: 15px; font-weight: 700; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 10px; }
.card-body-custom { padding: 18px 22px; }
.stat-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; }
.stat-card { border-radius: 14px; padding: 22px; color: #fff; position: relative; overflow: hidden; box-shadow: var(--shadow-lg); }
.stat-card .sc-label { font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.8px; opacity: 0.9; }
.stat-card .sc-value { font-size: 32px; font-weight: 800; font-family: 'Inter', sans-serif; line-height: 1.1; margin-top: 6px; }
.stat-card .sc-icon { position: absolute; right: 18px; top: 18px; width: 48px; height: 48px; border-radius: 50%; background: rgba(255,255,255,0.2); display: flex; align-items: center; justify-content: center; font-size: 20px; }
.sc-farm-green { background: linear-gradient(135deg, #166534, #15803d); }
.sc-farm-earth { background: linear-gradient(135deg, #854d0e, #a16207); }
.sc-farm-olive { background: linear-gradient(135deg, #3f6212, #4d7c0f); }
.sc-farm-forest { background: linear-gradient(135deg, #064e3b, #065f46); }
.sc-farm-blue { background: linear-gradient(135deg, #1e3a8a, #1d4ed8); }
.sc-farm-red { background: linear-gradient(135deg, #7c2d12, #c2410c); }
.sc-farm-teal { background: linear-gradient(135deg, #0f766e, #14b8a6); }
.sc-farm-purple { background: linear-gradient(135deg, #5b21b6, #7c3aed); }
.table { --bs-table-bg: transparent; --bs-table-color: var(--text); }
.table > :not(caption) > * > * { background-color: transparent !important; color: var(--text) !important; border-color: var(--border) !important; }
.table thead th { font-size: 11px; text-transform: uppercase; letter-spacing: 0.8px; font-weight: 700; color: var(--muted); }
html.dark .table { border-color: var(--border); }
.badge-active { background: rgba(21, 128, 61, 0.12); color: #166534; border-radius: 20px; padding: 3px 10px; font-weight: 600; font-size: 12px; }
.badge-harvested { background: rgba(120, 113, 108, 0.12); color: #78716c; border-radius: 20px; padding: 3px 10px; font-weight: 600; font-size: 12px; }
.badge-success { background: rgba(21, 128, 61, 0.12); color: #166534; border-radius: 20px; padding: 3px 10px; font-weight: 600; font-size: 12px; }
.badge-warning { background: rgba(161, 98, 7, 0.12); color: #a16207; border-radius: 20px; padding: 3px 10px; font-weight: 600; font-size: 12px; }
.badge-danger { background: rgba(220, 38, 38, 0.12); color: #dc2626; border-radius: 20px; padding: 3px 10px; font-weight: 600; font-size: 12px; }
.badge-info { background: rgba(37, 99, 235, 0.12); color: #2563eb; border-radius: 20px; padding: 3px 10px; font-weight: 600; font-size: 12px; }
.status-pill { border-radius: 20px; padding: 3px 10px; font-weight: 700; font-size: 11px; text-transform: uppercase; letter-spacing: 0.4px; display: inline-flex; align-items: center; gap: 5px; }
.status-scheduled { background: rgba(161, 98, 7, 0.12); color: #a16207; }
.status-administered { background: rgba(21, 128, 61, 0.12); color: #166534; }
.status-missed, .status-skipped { background: rgba(220, 38, 38, 0.1); color: #dc2626; }
.status-paid { background: rgba(21, 128, 61, 0.12); color: #166534; }
.status-pending { background: rgba(161, 98, 7, 0.12); color: #a16207; }
.status-overdue { background: rgba(220, 38, 38, 0.12); color: #dc2626; }
.form-control, .form-select { background: var(--bg) !important; border: 1.5px solid var(--border) !important; color: var(--text) !important; border-radius: 9px !important; padding: 9px 13px !important; font-size: 14px !important; transition: border-color 0.15s; }
.form-control:focus, .form-select:focus { border-color: var(--accent) !important; box-shadow: 0 0 0 3px rgba(22, 101, 52, 0.1) !important; }
.form-label { font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.6px; color: var(--muted); margin-bottom: 5px; }
.btn-farm { background: linear-gradient(135deg, #166534, #15803d); color: #fff; border: none; border-radius: 9px; font-weight: 700; font-size: 14px; padding: 9px 20px; transition: opacity 0.15s; }
.btn-farm:hover { opacity: 0.88; color: #fff; }
.btn-farm:disabled { opacity: 0.5; cursor: not-allowed; }
.btn-ghost { background: var(--sidebar-hover); color: var(--text); border: none; border-radius: 9px; font-weight: 600; font-size: 13px; padding: 8px 16px; }
.btn-ghost:hover { color: var(--text); opacity: 0.8; }
.btn-danger-custom { background: #dc2626; color: #fff; border: none; border-radius: 9px; font-weight: 600; font-size: 13px; padding: 8px 16px; }
.btn-danger-custom:hover { opacity: 0.85; color: #fff; }
.alert-flash { border-radius: 10px; font-size: 14px; font-weight: 500; border: none; }
.theme-toggle { width: 36px; height: 36px; border-radius: 9px; background: var(--sidebar-hover); border: none; color: var(--text); cursor: pointer; display: flex; align-items: center; justify-content: center; transition: all 0.15s; font-size: 14px; }
.theme-toggle:hover { background: var(--border); }
.role-badge { font-size: 10px; font-weight: 800; text-transform: uppercase; letter-spacing: 1px; padding: 3px 9px; border-radius: 20px; }
.role-owner { background: rgba(22, 101, 52, 0.1); color: #166534; }
.role-manager { background: rgba(37,99,235,0.12); color: #2563eb; }
.role-worker { background: rgba(22,163,74,0.12); color: #16a34a; }
.mobile-topbar { display: none; background: var(--sidebar-bg); border-bottom: 1px solid var(--border); padding: 14px 20px; align-items: center; justify-content: space-between; position: sticky; top: 0; z-index: 200; }
.mobile-overlay { display: none; position: fixed; inset: 0; background: rgba(0,0,0,0.5); z-index: 150; backdrop-filter: blur(2px); }
.mobile-overlay.show { display: block; }
@media (max-width: 991px) {
  .sidebar { position: fixed; left: 0; top: 0; height: 100%; transform: translateX(-100%); }
  .sidebar.show { transform: translateX(0); box-shadow: 4px 0 20px rgba(0,0,0,0.15); }
  .mobile-topbar { display: flex; }
  .topbar { display: none; }
  .page-body { padding: 18px; }
}
@media (max-width: 576px) {
  .stat-grid { grid-template-columns: 1fr 1fr; }
  .sc-value { font-size: 24px; }
}
.section-header { display: flex; align-items: center; gap: 10px; margin-bottom: 16px; }
.section-header h5 { font-family: 'Inter', sans-serif; font-size: 16px; font-weight: 800; margin: 0; }
.section-divider { width: 4px; height: 22px; border-radius: 3px; background: linear-gradient(to bottom, #166534, #15803d); }
.hero-banner { border-radius: 18px; background: linear-gradient(135deg, #166534 0%, #3f6212 100%); color: #fff; padding: 28px 32px; display: flex; justify-content: space-between; align-items: center; margin-bottom: 28px; position: relative; overflow: hidden; }
.hero-banner::after { content:''; position:absolute; right:-30px; top:-30px; width:180px; height:180px; border-radius:50%; background:rgba(255,255,255,0.08); }
.hero-banner::before { content:''; position:absolute; right:60px; bottom:-40px; width:120px; height:120px; border-radius:50%; background:rgba(255,255,255,0.06); }
.metric-pill { display:inline-flex; align-items:center; gap:6px; background:rgba(255,255,255,0.15); border-radius:20px; padding:4px 12px; font-size:13px; font-weight:600; }
.tbl-actions { display:flex; gap:6px; }
.btn-sm-icon { width:30px;height:30px;border-radius:7px;border:none;display:flex;align-items:center;justify-content:center;font-size:12px;cursor:pointer;transition:all 0.15s; }
.btn-edit { background:rgba(37,99,235,0.12); color:#2563eb; }
.btn-edit:hover { background:#2563eb; color:#fff; }
.btn-del { background:rgba(220,38,38,0.1); color:#dc2626; }
.btn-del:hover { background:#dc2626; color:#fff; }
.btn-ok { background:rgba(21,128,61,0.12); color:#166534; }
.btn-ok:hover { background:#166534; color:#fff; }
.btn-warn { background:rgba(161,98,7,0.12); color:#a16207; }
.btn-warn:hover { background:#a16207; color:#fff; }
.analytics-grid { display:grid; grid-template-columns:1fr 1fr; gap:16px; }
@media(max-width:768px){ .analytics-grid{grid-template-columns:1fr;} .hero-banner{flex-direction:column;gap:16px;text-align:center;} }
.input-table-section { overflow-x:auto; }
.schedule-list { display: flex; flex-direction: column; gap: 8px; }
.schedule-item { display: flex; align-items: center; gap: 12px; padding: 10px 14px; border-radius: 10px; background: var(--bg); border: 1px solid var(--border); }
.schedule-item .si-icon { width: 34px; height: 34px; border-radius: 9px; flex-shrink: 0; display: flex; align-items: center; justify-content: center; font-size: 13px; background: rgba(22,101,52,0.1); color: var(--accent); }
.schedule-item.overdue .si-icon { background: rgba(220,38,38,0.12); color: #dc2626; }
.si-body { flex: 1; min-width: 0; }
.si-title { font-size: 13px; font-weight: 700; }
.si-sub { font-size: 12px; color: var(--muted); }
.si-date { font-size: 12px; font-weight: 600; color: var(--muted); white-space: nowrap; }
.confirm-row { display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid var(--border); font-size: 13px; }
.confirm-row:last-child { border-bottom: none; }
.confirm-row .label { color: var(--muted); font-weight: 600; }
.confirm-row .value { font-weight: 700; }
.chart-container { position: relative; height: 350px; width: 100%; }
.chart-container-sm { position: relative; height: 250px; width: 100%; }
.report-field-list { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 8px; }
.report-field-item { display: flex; align-items: center; gap: 8px; padding: 8px 12px; border-radius: 8px; background: var(--bg); border: 1px solid var(--border); font-size: 13px; cursor: pointer; }
.report-field-item:hover { background: var(--sidebar-hover); }
.report-field-item input[type="checkbox"] { cursor: pointer; }
.detail-panel { background: var(--bg); border-radius: 10px; padding: 16px; border: 1px solid var(--border); margin-top: 16px; }
.detail-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 12px; }
.detail-item { font-size: 13px; }
.detail-item .label { color: var(--muted); font-weight: 600; font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px; }
.detail-item .value { font-weight: 700; }
.expense-card-icon { width: 40px; height: 40px; border-radius: 10px; display:flex; align-items:center; justify-content:center; font-size:16px; color:#fff; flex-shrink:0; }
.price-basis-option { display:flex; align-items:center; gap:10px; padding:12px; border:1px solid var(--border); border-radius:10px; cursor:pointer; background:var(--bg); transition:all 0.15s; }
.price-basis-option:hover { border-color:var(--accent); background:var(--sidebar-active-bg); }
.price-basis-option input[type="radio"] { width:18px; height:18px; accent-color:#166534; }
.autofield { background: #e5e7eb !important; cursor: not-allowed; }
</style>
"""

def logo_svg(size=40, opacity=1):
    return f'''<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" style="opacity:{opacity};display:block;">
  <ellipse cx="50" cy="66" rx="34" ry="28" fill="#FFCF3F"/>
  <circle cx="50" cy="34" r="23" fill="#FFDD5C"/>
  <path d="M50 34 L74 39 L50 46 Z" fill="#FF8A3D"/>
  <circle cx="43" cy="29" r="4" fill="#2B2118"/>
  <circle cx="57" cy="29" r="4" fill="#2B2118"/>
  <path d="M18 16 Q28 6 37 18 Q27 20 18 16 Z" fill="#FFB03F"/>
  <path d="M63 18 Q72 6 82 16 Q73 20 63 18 Z" fill="#FFB03F"/>
  <path d="M22 62 Q10 66 14 78 Q24 74 26 64 Z" fill="#FFDD5C"/>
</svg>'''

_BASE_SCRIPT = """
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
<script>
(function(){
  const t = localStorage.getItem("theme");
  if(t === "dark") document.documentElement.classList.add("dark");
})();
function toggleDark(){
  document.documentElement.classList.toggle("dark");
  localStorage.setItem("theme", document.documentElement.classList.contains("dark") ? "dark" : "light");
  const el = document.getElementById("themeIcon");
  if (el) el.className = document.documentElement.classList.contains("dark") ? "fas fa-sun" : "fas fa-moon";
}
function toggleSidebar(){
  document.getElementById("sidebar").classList.toggle("show");
  document.getElementById("mobileOverlay").classList.toggle("show");
}
function showTab(tabId, element) {
    document.querySelectorAll('.tab-content').forEach(tab => { tab.classList.remove('active'); });
    document.querySelectorAll('.nav-link').forEach(link => { link.classList.remove('active'); });
    var activeTab = document.getElementById(tabId);
    activeTab.classList.add('active');
    element.classList.add('active');
    
    // Save active tab to localStorage so it persists across form submissions
    localStorage.setItem("activeTab", tabId);
    
    if (window.innerWidth < 992) { toggleSidebar(); }
    if (window.Chart) {
        activeTab.querySelectorAll('canvas').forEach(function(canvas) {
            var chart = Chart.getChart(canvas);
            if (chart) { chart.resize(); }
        });
    }
}

// Automatically restore the active tab on page load/form submission reload
document.addEventListener("DOMContentLoaded", function() {
  const savedTab = localStorage.getItem("activeTab");
  if (savedTab) {
    const tabEl = document.getElementById(savedTab);
    const navLink = document.querySelector(`[onclick*="${savedTab}"]`);
    if (tabEl && navLink) {
        showTab(savedTab, navLink);
    }
  }
});

setTimeout(()=>{ document.querySelectorAll(".alert-flash").forEach(a=>{ let b=bootstrap.Alert.getOrCreateInstance(a); b.close(); }); }, 4000);
</script>
"""

# ─────────────────────────────────────────────────────────────────────────────
# LOGIN
# ─────────────────────────────────────────────────────────────────────────────
TEMPLATE_LOGIN = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Login — FlockIQ</title>
""" + _BASE_STYLE + """
<style>
body { display: flex; align-items: center; justify-content: center; min-height: 100vh;
  background: #fdfcfb; background-image: radial-gradient(circle at 2px 2px, rgba(22,101,52,0.05) 1px, transparent 0); background-size: 40px 40px; }
.auth-card { background: var(--card-bg); border-radius: 20px; box-shadow: var(--shadow-lg); padding: 40px 36px; width: 100%; max-width: 420px; border: 1px solid var(--border); }
.auth-logo { width: 56px; height: 56px; border-radius: 16px; background: linear-gradient(135deg,#166534,#15803d); display: flex; align-items: center; justify-content: center; color: #fff; font-size: 24px; margin: 0 auto 20px; }
.auth-title { font-family: 'Inter', sans-serif; font-size: 26px; font-weight: 800; text-align: center; margin-bottom: 4px; color: var(--accent); }
.auth-sub { text-align: center; color: var(--muted); font-size: 14px; margin-bottom: 28px; }
.input-group-custom { position: relative; margin-bottom: 14px; }
.input-group-custom .icon { position: absolute; left: 13px; top: 50%; transform: translateY(-50%); color: var(--muted); font-size: 14px; z-index: 1; }
.input-group-custom input { padding-left: 38px !important; }
.password-toggle { position: absolute; right: 14px; top: 50%; transform: translateY(-50%); cursor: pointer; color: var(--muted); z-index: 1; }
.password-toggle:hover { color: var(--text); }
</style>
</head>
<body>
<div class="auth-card">
  <div class="auth-logo">""" + logo_svg(30) + """</div>
  <div class="auth-title">FlockIQ</div>
  <div class="auth-sub">Poultry Farm Management System</div>

  {% with msgs = get_flashed_messages() %}{% if msgs %}
    {% for m in msgs %}
    <div class="alert alert-warning alert-dismissible fade show alert-flash" role="alert" style="font-size:13px;border-radius:9px;">
      <i class="fas fa-exclamation-circle me-2"></i>{{ m }}
      <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    </div>
    {% endfor %}
  {% endif %}{% endwith %}

  <form method="post">
    <div class="input-group-custom">
      <i class="icon fas fa-user"></i>
      <input type="text" name="username" class="form-control" placeholder="Username" required>
    </div>
    <div class="input-group-custom">
      <i class="icon fas fa-lock"></i>
      <input type="password" name="password" id="loginPw" class="form-control" placeholder="Password" required style="padding-right:40px;">
      <i class="fas fa-eye password-toggle" id="loginPwToggle" onclick="togglePassword()"></i>
    </div>
    <button type="submit" class="btn-farm w-100 mt-2" style="padding:12px;">Sign In</button>
  </form>

  <div class="text-center mt-4" style="font-size:13px; color: var(--muted);">
    Accounts are created by the Farm Owner. Contact your Owner if you need access.
  </div>
</div>
""" + _BASE_SCRIPT + """
<script>
function togglePassword() {
  const f = document.getElementById('loginPw');
  const toggle = document.getElementById('loginPwToggle');
  const show = f.type === 'password';
  f.type = show ? 'text' : 'password';
  toggle.className = show ? 'fas fa-eye-slash password-toggle' : 'fas fa-eye password-toggle';
}
</script>
</body></html>
"""

# ─────────────────────────────────────────────────────────────────────────────
# OWNER DASHBOARD
# ─────────────────────────────────────────────────────────────────────────────
TEMPLATE_OWNER = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Owner Dashboard — FlockIQ</title>
""" + _BASE_STYLE + """
</head>
<body>
<script>(function(){const t=localStorage.getItem("theme");if(t==="dark")document.documentElement.classList.add("dark");})()</script>
<div id="mobileOverlay" class="mobile-overlay" onclick="toggleSidebar()"></div>
<div class="mobile-topbar">
  <button onclick="toggleSidebar()" style="background:none;border:none;color:var(--text);font-size:20px;"><i class="fas fa-bars"></i></button>
  <span style="font-family:'Inter',sans-serif;font-weight:800;font-size:16px;">FlockIQ</span>
  <button class="theme-toggle" onclick="toggleDark()"><i class="fas fa-moon"></i></button>
</div>
<div class="app-shell">

<nav id="sidebar" class="sidebar">
  <div class="sidebar-brand">
    <div class="brand-icon">""" + logo_svg(22) + """</div>
    <div><div class="brand-text">FlockIQ</div><div class="brand-sub">Farm Management</div></div>
  </div>
  <div class="sidebar-nav">
    <div class="nav-section-label">Owner Panel</div>
    <a onclick="showTab('overview', this)" class="nav-link active"><i class="fas fa-gauge"></i> Overview</a>
    <a onclick="showTab('account-mgmt', this)" class="nav-link"><i class="fas fa-users-cog"></i> Account Management</a>
    <a onclick="showTab('market-price', this)" class="nav-link"><i class="fas fa-chart-line"></i> Market Prices</a>
    <a onclick="showTab('flock-mgmt', this)" class="nav-link"><i class="fas fa-layer-group"></i> Flock Management</a>
    <a onclick="showTab('harvest-history', this)" class="nav-link"><i class="fas fa-history"></i> Harvest History</a>
    <a onclick="showTab('summary-reports', this)" class="nav-link"><i class="fas fa-file-alt"></i> Summary Reports</a>
  </div>
  <div class="sidebar-footer">
    <div style="display:flex;align-items:center;gap:10px;padding:8px 12px;margin-bottom:8px;">
      <div style="width:34px;height:34px;border-radius:50%;background:linear-gradient(135deg,#166534,#15803d);display:flex;align-items:center;justify-content:center;color:#fff;font-size:13px;"><i class="fas fa-crown"></i></div>
      <div><div style="font-size:13px;font-weight:700;">{{ full_name }}</div><span class="role-badge role-owner">Owner</span></div>
    </div>
    <a href="/logout" class="logout-btn"><i class="fas fa-sign-out-alt"></i> Logout</a>
  </div>
</nav>

<div class="main-content">
  <div class="topbar">
    <span class="topbar-title">Owner Dashboard</span>
    <div class="topbar-actions">
      <button class="theme-toggle" onclick="toggleDark()"><i class="fas fa-moon"></i></button>
    </div>
  </div>
  <div class="page-body">

    {% with msgs = get_flashed_messages() %}{% if msgs %}
    {% for m in msgs %}
    <div class="alert alert-success alert-dismissible fade show alert-flash mb-3" role="alert">
      <i class="fas fa-check-circle me-2"></i>{{ m }}
      <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    </div>
    {% endfor %}{% endif %}{% endwith %}

    <!-- ==================== OVERVIEW ==================== -->
    <div id="overview" class="tab-content active">
        <div class="hero-banner">
          <div style="position:relative;z-index:1;">
            <div style="font-size:13px;font-weight:600;opacity:0.85;margin-bottom:6px;">Welcome back,</div>
            <h2 style="font-family:'Inter',sans-serif;font-weight:800;font-size:26px;margin:0 0 14px;">{{ full_name }} <i class="fas fa-crown" style="font-size:16px;opacity:0.8;"></i></h2>
            <div style="display:flex;flex-wrap:wrap;gap:8px;">
              <div class="metric-pill"><i class="fas fa-layer-group"></i> {{ active_flocks|length }} Active Flocks</div>
              <div class="metric-pill"><i class="fas fa-feather-pointed"></i> {{ "{:,}".format(total_birds) }} Total Remaining Birds</div>
              <div class="metric-pill"><i class="fas fa-users"></i> {{ users|length }} System Users</div>
            </div>
          </div>
          <div style="position:relative;z-index:1;">""" + logo_svg(90, 0.25) + """</div>
        </div>

        {% if active_flocks %}
        {% for f in active_flocks %}
        <div class="card mb-4">
          <div class="card-header-custom">
            <div class="section-header" style="margin:0;">
              <div class="section-divider"></div>
              <h5><i class="fas fa-feather-pointed me-2" style="color:var(--accent);"></i>Active Flock: {{ f.batch_name }}</h5>
            </div>
            <div style="display:flex;gap:8px;align-items:center;">
              {% if f.season %}<span class="badge-info">{{ f.season }} Season</span>{% endif %}
              <span class="badge-active">Active</span>
            </div>
          </div>
          <div class="card-body-custom">
            <div class="stat-grid">
              <div class="stat-card sc-farm-green">
                <div class="sc-icon"><i class="fas fa-feather-pointed"></i></div>
                <div class="sc-label">Current Total Number</div>
                <div class="sc-value">{{ "{:,}".format(f.current_bird_count) }}</div>
              </div>
              <div class="stat-card sc-farm-earth">
                <div class="sc-icon"><i class="fas fa-calendar-day"></i></div>
                <div class="sc-label">Age</div>
                <div class="sc-value">Day {{ f.age_days }} <span style="font-size:16px;">of {{ f.target_age_days }}</span></div>
              </div>
              <div class="stat-card sc-farm-red">
                <div class="sc-icon"><i class="fas fa-skull-crossbones"></i></div>
                <div class="sc-label">Mortality</div>
                <div class="sc-value">{{ f.mortality_count }} <span style="font-size:16px;">({{ f.mortality_percentage }}%)</span></div>
              </div>
              <div class="stat-card sc-farm-blue">
                <div class="sc-icon"><i class="fas fa-calendar-check"></i></div>
                <div class="sc-label">Target Harvest</div>
                <div class="sc-value" style="font-size:20px;">{{ f.target_harvest_date.strftime('%b %d') if f.target_harvest_date else '—' }}</div>
              </div>
            </div>
          </div>
        </div>
        {% endfor %}
        {% else %}
        <div class="card mb-4">
          <div class="card-body-custom text-center py-5" style="color:var(--muted);">
            <i class="fas fa-layer-group fa-3x mb-3 d-block"></i>
            <h5 style="font-weight:700;">No Active Flock</h5>
            <p>Go to Flock Management to create a new batch.</p>
          </div>
        </div>
        {% endif %}

        <!-- Best Season of Sales Chart -->
        <div class="card mb-4">
          <div class="card-header-custom">
            <div class="section-header" style="margin:0;">
              <div class="section-divider"></div>
              <h5><i class="fas fa-chart-line me-2" style="color:var(--accent);"></i>Best Season of Sales</h5>
            </div>
          </div>
          <div class="card-body-custom">
            {% if best_season.available %}
            <div style="display:flex;gap:20px;margin-bottom:16px;flex-wrap:wrap;">
              <div style="flex:1;min-width:160px;background:{{ '#f0fdf4' if best_season.best_season == 'Dry' else '#f8fafc' }};border:1px solid {{ '#bbf7d0' if best_season.best_season == 'Dry' else '#e5e7eb' }};border-radius:10px;padding:14px;">
                <div style="font-size:11px;color:var(--muted);text-transform:uppercase;letter-spacing:.03em;">Dry Season Avg</div>
                <div style="font-size:22px;font-weight:800;">₱{{ best_season.dry_avg }}/kg</div>
              </div>
              <div style="flex:1;min-width:160px;background:{{ '#f0fdf4' if best_season.best_season == 'Wet' else '#f8fafc' }};border:1px solid {{ '#bbf7d0' if best_season.best_season == 'Wet' else '#e5e7eb' }};border-radius:10px;padding:14px;">
                <div style="font-size:11px;color:var(--muted);text-transform:uppercase;letter-spacing:.03em;">Wet Season Avg</div>
                <div style="font-size:22px;font-weight:800;">₱{{ best_season.wet_avg }}/kg</div>
              </div>
              <div style="flex:1;min-width:160px;background:linear-gradient(135deg,#166534,#15803d);color:#fff;border-radius:10px;padding:14px;">
                <div style="font-size:11px;opacity:0.85;text-transform:uppercase;letter-spacing:.03em;">Best Season</div>
                <div style="font-size:22px;font-weight:800;">{{ best_season.best_season }}</div>
              </div>
            </div>
            {% if best_season.labels %}
            <div class="chart-container-sm">
              <canvas id="seasonChart"></canvas>
            </div>
            <script>
            (function(){
              var el = document.getElementById('seasonChart');
              if (el && window.Chart) {
                new Chart(el, {
                  type: 'line',
                  data: {
                    labels: {{ best_season.labels|tojson }},
                    datasets: [{
                      label: 'Avg Price (₱/kg)',
                      data: {{ best_season.data|tojson }},
                      borderColor: '#15803d',
                      backgroundColor: 'rgba(21, 128, 61, 0.1)',
                      fill: true,
                      tension: 0.3,
                      pointRadius: 5,
                      pointBackgroundColor: '#15803d'
                    }]
                  },
                  options: {
                    responsive: true, maintainAspectRatio: false,
                    plugins: { legend: { display: false } },
                    scales: { y: { beginAtZero: false, title: { display: true, text: 'Price (₱/kg)' } } }
                  }
                });
              }
            })();
            </script>
            {% endif %}
            {% else %}
            <div class="text-center py-4" style="color:var(--muted);">
              <i class="fas fa-chart-line fa-2x mb-2 d-block"></i>
              Not enough harvest data to determine best season yet.
            </div>
            {% endif %}
          </div>
        </div>

        <div class="row g-4">
        <div class="col-lg-6 d-flex">
        <div class="card w-100">
          <div class="card-header-custom">
            <div class="section-header" style="margin:0;">
              <div class="section-divider"></div>
              <h5><i class="fas fa-chart-pie me-2" style="color:var(--accent);"></i>Expense Breakdown</h5>
            </div>
            <a href="/manager/expenses/history" class="btn-farm" style="font-size:12px;padding:6px 12px;text-decoration:none;"><i class="fas fa-clock-rotate-left me-1"></i> Past Batches</a>
          </div>
          <div class="card-body-custom">
            {% if expense_summary.total > 0 %}
            <div style="display:flex;flex-wrap:wrap;align-items:center;gap:28px;">
              <div class="chart-container-sm" style="max-width:280px;flex:1 1 240px;">
                <canvas id="ownerExpensePieChart"></canvas>
              </div>
              <div style="flex:1 1 200px;display:flex;flex-direction:column;gap:10px;">
                <div style="display:flex;align-items:center;gap:8px;font-size:13px;"><span style="width:12px;height:12px;border-radius:3px;background:#0ea5e9;display:inline-block;"></span> Water — ₱{{ "{:,.0f}".format(expense_summary.water) }}</div>
                <div style="display:flex;align-items:center;gap:8px;font-size:13px;"><span style="width:12px;height:12px;border-radius:3px;background:#facc15;display:inline-block;"></span> Electricity — ₱{{ "{:,.0f}".format(expense_summary.electricity) }}</div>
                <div style="display:flex;align-items:center;gap:8px;font-size:13px;"><span style="width:12px;height:12px;border-radius:3px;background:#d97706;display:inline-block;"></span> LPG — ₱{{ "{:,.0f}".format(expense_summary.lpg) }}</div>
                <div style="display:flex;align-items:center;gap:8px;font-size:13px;"><span style="width:12px;height:12px;border-radius:3px;background:#7c3aed;display:inline-block;"></span> Labor — ₱{{ "{:,.0f}".format(expense_summary.labor) }}</div>
                <div style="display:flex;align-items:center;gap:8px;font-size:13px;"><span style="width:12px;height:12px;border-radius:3px;background:#0f766e;display:inline-block;"></span> Vaccine — ₱{{ "{:,.0f}".format(expense_summary.vaccine) }}</div>
                <div style="display:flex;align-items:center;gap:8px;font-size:13px;"><span style="width:12px;height:12px;border-radius:3px;background:#ca8a04;display:inline-block;"></span> Chicks — ₱{{ "{:,.0f}".format(expense_summary.chick) }}</div>
                <div style="display:flex;align-items:center;gap:8px;font-size:13px;"><span style="width:12px;height:12px;border-radius:3px;background:#be123c;display:inline-block;"></span> Feed — ₱{{ "{:,.0f}".format(expense_summary.feed) }}</div>
                <div style="display:flex;align-items:center;gap:8px;font-size:13px;"><span style="width:12px;height:12px;border-radius:3px;background:#c2410c;display:inline-block;"></span> Other — ₱{{ "{:,.0f}".format(expense_summary.other) }}</div>
                <div style="display:flex;align-items:center;gap:8px;font-size:13px;font-weight:700;border-top:1px solid var(--border);padding-top:10px;margin-top:2px;">Total — ₱{{ "{:,.0f}".format(expense_summary.total) }}</div>
              </div>
            </div>
            <script>
            (function(){
              var el = document.getElementById('ownerExpensePieChart');
              if (el && window.Chart) {
                new Chart(el, {
                  type: 'pie',
                  data: {
                    labels: ['Water', 'Electricity', 'LPG', 'Labor', 'Vaccine', 'Chicks', 'Feed', 'Other'],
                    datasets: [{
                      data: [{{ expense_summary.water }}, {{ expense_summary.electricity }}, {{ expense_summary.lpg }}, {{ expense_summary.labor }}, {{ expense_summary.vaccine }}, {{ expense_summary.chick }}, {{ expense_summary.feed }}, {{ expense_summary.other }}],
                      backgroundColor: ['#0ea5e9', '#facc15', '#d97706', '#7c3aed', '#0f766e', '#ca8a04', '#be123c', '#c2410c'],
                      borderWidth: 0
                    }]
                  },
                  options: {
                    responsive: true, maintainAspectRatio: false,
                    plugins: {
                      legend: { display: false },
                      tooltip: {
                        callbacks: {
                          label: function(ctx) {
                            var val = ctx.parsed || 0;
                            var total = ctx.dataset.data.reduce(function(a,b){ return a+b; }, 0);
                            var pct = total > 0 ? ((val/total)*100).toFixed(1) : '0.0';
                            return ctx.label + ': ₱' + val.toLocaleString(undefined,{minimumFractionDigits:0,maximumFractionDigits:0}) + ' (' + pct + '%)';
                          }
                        }
                      }
                    }
                  }
                });
              }
            })();
            </script>
            {% else %}
            <div class="text-center py-4" style="color:var(--muted);">
              <i class="fas fa-chart-pie fa-2x mb-2 d-block"></i>
              No expenses logged yet.
            </div>
            {% endif %}
          </div>
        </div>
        </div>

        <div class="col-lg-6 d-flex">
        <div class="card w-100">
          <div class="card-header-custom">
            <div class="section-header" style="margin:0;">
              <div class="section-divider"></div>
              <h5><i class="fas fa-chart-column me-2" style="color:var(--accent);"></i>Flock Performance — ADG, FCR &amp; LW</h5>
            </div>
          </div>
          <div class="card-body-custom">
            {% if flock_analytics %}
            <div style="font-size:12px;color:var(--muted);margin-bottom:14px;">
              Batch-level metrics: ADG, FCR, and Live Weight calculated from the entire batch data.
            </div>
            <div style="display:flex;flex-direction:column;gap:12px;max-height:320px;overflow-y:auto;">
              {% for item in flock_analytics %}
              <div style="border:1px solid var(--border);border-radius:10px;padding:12px 14px;">
                <div style="font-weight:700;font-size:13px;margin-bottom:10px;">
                  {{ item.flock.batch_name }}
                  <span style="font-weight:400;color:var(--muted);">— Day {{ item.analytics.age_days }}</span>
                </div>
                <div style="display:flex;flex-wrap:wrap;gap:20px;">
                  <div>
                    <div style="font-size:11px;color:var(--muted);text-transform:uppercase;letter-spacing:.03em;">ADG</div>
                    <div style="font-size:16px;font-weight:800;color:#15803d;">{{ item.analytics.adg }} <span style="font-size:11px;font-weight:500;color:var(--muted);">g/batch</span></div>
                  </div>
                  <div>
                    <div style="font-size:11px;color:var(--muted);text-transform:uppercase;letter-spacing:.03em;">FCR</div>
                    <div style="font-size:16px;font-weight:800;color:#d97706;">{{ item.analytics.fcr }}</div>
                  </div>
                  <div>
                    <div style="font-size:11px;color:var(--muted);text-transform:uppercase;letter-spacing:.03em;">LW</div>
                    <div style="font-size:16px;font-weight:800;color:#0ea5e9;">{{ "{:,.0f}".format(item.analytics.latest_weight) }} <span style="font-size:11px;font-weight:500;color:var(--muted);">g/bird</span></div>
                  </div>
                </div>
              </div>
              {% endfor %}
            </div>
            {% else %}
            <div class="text-center py-4" style="color:var(--muted);">
              <i class="fas fa-chart-column fa-2x mb-2 d-block"></i>
              No flock data yet.
            </div>
            {% endif %}
          </div>
        </div>
        </div>
        </div>
    </div>

    <!-- ==================== ACCOUNT MANAGEMENT ==================== -->
    <div id="account-mgmt" class="tab-content">
      <div class="card mb-4">
        <div class="card-header-custom">
          <div class="section-header" style="margin:0;">
            <div class="section-divider"></div>
            <h5><i class="fas fa-users-cog me-2" style="color:var(--accent);"></i>Account Management</h5>
          </div>
          <button class="btn-farm" data-bs-toggle="modal" data-bs-target="#addUserModal" style="font-size:13px;padding:7px 14px;">
            <i class="fas fa-plus me-1"></i> Add User
          </button>
        </div>
        <div class="card-body-custom">
          <div style="font-size:12px;color:var(--muted);margin-bottom:14px;">
            <i class="fas fa-lock me-1"></i> Only the Owner can create, edit, or remove accounts. Manager accounts can be deactivated or deleted.
          </div>
          <div class="table-responsive">
            <table class="table table-hover align-middle">
              <thead><tr>
                <th>#</th><th>Full Name</th><th>Username</th><th>Phone Number</th><th>Role</th><th>Status</th><th>Actions</th>
              </tr></thead>
              <tbody>
              {% for u in users %}
              <tr>
                <td style="color:var(--muted);font-size:13px;">{{ u.user_id }}</td>
                <td style="font-weight:600;">{{ u.full_name }}</td>
                <td><code style="font-size:13px;">{{ u.username }}</code></td>
                <td style="font-size:13px;color:var(--muted);">{{ u.phone_num or '—' }}</td>
                <td>
                  {% if u.role == 'Owner' %}<span class="role-badge role-owner">Owner</span>
                  {% elif u.role == 'Manager' %}<span class="role-badge role-manager">Manager</span>
                  {% else %}<span class="role-badge role-worker">Worker</span>{% endif %}
                </td>
                <td>
                  {% if u.is_active %}
                  <span class="status-pill status-paid">Active</span>
                  {% else %}
                  <span class="status-pill status-missed">Inactive</span>
                  {% endif %}
                </td>
                <td>
                  <div class="tbl-actions">
                    <button class="btn-sm-icon btn-edit" type="button" data-bs-toggle="modal" data-bs-target="#editUserModal{{ u.user_id }}" title="Edit"><i class="fas fa-pen"></i></button>
                    <button class="btn-sm-icon btn-warn" type="button" data-bs-toggle="modal" data-bs-target="#resetPasswordModal{{ u.user_id }}" title="Reset Password"><i class="fas fa-key"></i></button>
                    {% if u.username != 'owner' %}
                    <form method="post" action="/owner/user/deactivate/{{ u.user_id }}" style="display:inline;">
                      <button class="btn-sm-icon {{ 'btn-del' if u.is_active else 'btn-ok' }}" type="submit" title="{{ 'Deactivate' if u.is_active else 'Activate' }}">
                        <i class="fas {{ 'fa-user-slash' if u.is_active else 'fa-user-check' }}"></i>
                      </button>
                    </form>
                    <form method="post" action="/owner/user/delete/{{ u.user_id }}" onsubmit="return confirm('Delete user {{ u.username }}? This cannot be undone.')" style="display:inline;">
                      <button class="btn-sm-icon btn-del" type="submit"><i class="fas fa-trash"></i></button>
                    </form>
                    {% endif %}
                  </div>
                </td>
              </tr>

              <div class="modal fade" id="editUserModal{{ u.user_id }}" tabindex="-1">
                <div class="modal-dialog modal-dialog-centered">
                  <div class="modal-content" style="background:var(--card-bg);border:1px solid var(--border);border-radius:16px;">
                    <div class="modal-header" style="border-color:var(--border);">
                      <h5 class="modal-title" style="font-weight:800;"><i class="fas fa-user-pen me-2" style="color:var(--accent);"></i>Edit {{ u.full_name }}</h5>
                      <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <form method="post" action="/owner/user/edit/{{ u.user_id }}">
                      <div class="modal-body">
                        <div class="row g-2 mb-3">
                          <div class="col-4"><label class="form-label">First Name</label><input name="first_name" class="form-control" value="{{ u.first_name }}" required></div>
                          <div class="col-4"><label class="form-label">Middle Name</label><input name="middle_name" class="form-control" value="{{ u.middle_name or '' }}"></div>
                          <div class="col-4"><label class="form-label">Last Name</label><input name="last_name" class="form-control" value="{{ u.last_name }}" required></div>
                        </div>
                        <div class="mb-1"><label class="form-label">Phone Number</label>
                          <input name="phone_num" class="form-control" value="{{ u.phone_num or '' }}"
                                 pattern="09[0-9]{9}" maxlength="11" placeholder="09XXXXXXXXX"
                                 title="11 digits starting with 09">
                          <small style="color:var(--muted);">Format: 09XXXXXXXXX (11 digits).</small>
                        </div>
                      </div>
                      <div class="modal-footer" style="border-color:var(--border);">
                        <button type="button" class="btn-ghost" data-bs-dismiss="modal">Cancel</button>
                        <button type="submit" class="btn-farm">Save Changes</button>
                      </div>
                    </form>
                  </div>
                </div>
              </div>

              <div class="modal fade" id="resetPasswordModal{{ u.user_id }}" tabindex="-1">
                <div class="modal-dialog modal-dialog-centered">
                  <div class="modal-content" style="background:var(--card-bg);border:1px solid var(--border);border-radius:16px;">
                    <div class="modal-header" style="border-color:var(--border);">
                      <h5 class="modal-title" style="font-weight:800;"><i class="fas fa-key me-2" style="color:#a16207;"></i>Reset Password: {{ u.full_name }}</h5>
                      <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <form method="post" action="/owner/user/reset-password/{{ u.user_id }}">
                      <div class="modal-body">
                        <div class="mb-1"><label class="form-label">New Password</label><input type="password" name="new_password" class="form-control" required minlength="6"></div>
                        <small style="color:var(--muted);">Minimum 6 characters.</small>
                      </div>
                      <div class="modal-footer" style="border-color:var(--border);">
                        <button type="button" class="btn-ghost" data-bs-dismiss="modal">Cancel</button>
                        <button type="submit" class="btn-farm">Reset Password</button>
                      </div>
                    </form>
                  </div>
                </div>
              </div>
              {% else %}
              <tr><td colspan="7" class="text-center py-4" style="color:var(--muted);">No users found.</td></tr>
              {% endfor %}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>

    <!-- ==================== MARKET PRICES ==================== -->
    <div id="market-price" class="tab-content">
      <div class="stat-grid mb-4">
        <div class="stat-card sc-farm-forest">
          <div class="sc-icon"><i class="fas fa-tower-broadcast"></i></div>
          <div class="sc-label">DA Bantay Presyo — Chicken Price</div>
          <div class="sc-value">₱{{ "%.2f"|format(live_market.retail_avg) }}</div>
          <div style="font-size:11px;opacity:0.8;margin-top:4px;">{{ live_market.source }} · {{ live_market.last_update }}</div>
        </div>
        <div class="stat-card sc-farm-blue">
          <div class="sc-icon"><i class="fas fa-pen"></i></div>
          <div class="sc-label">Latest Given Price</div>
          <div class="sc-value">{% if all_market_prices %}₱{{ "%.2f"|format(all_market_prices[0].price_per_kg) }}{% else %}—{% endif %}</div>
          <div style="font-size:11px;opacity:0.8;margin-top:4px;">{% if all_market_prices %}{{ all_market_prices[0].record_date.strftime('%b %d, %Y') }}{% else %}No price recorded yet{% endif %}</div>
        </div>
      </div>

      <div class="card">
        <div class="card-header-custom">
          <div class="section-header" style="margin:0;">
            <div class="section-divider"></div>
            <h5><i class="fas fa-table-list me-2" style="color:var(--accent);"></i>Given Prices History</h5>
          </div>
          <button class="btn-farm" data-bs-toggle="modal" data-bs-target="#addPriceModal" style="font-size:13px;padding:7px 14px;">
            <i class="fas fa-plus me-1"></i> Record Price
          </button>
        </div>
        <div class="card-body-custom">
          <div style="font-size:12px;color:var(--muted);margin-bottom:14px;">
            All given prices by date. Use these as basis for selling your flock.
          </div>
          <div class="table-responsive">
            <table class="table table-hover align-middle">
              <thead><tr><th>Date</th><th>Given Price / kg</th><th>Location</th></tr></thead>
              <tbody>
              {% for p in all_market_prices %}
              <tr>
                <td>{{ p.record_date.strftime('%b %d, %Y') }}</td>
                <td style="font-weight:700;color:var(--accent);">₱{{ "%.2f"|format(p.price_per_kg) }}</td>
                <td style="color:var(--muted);">{{ p.location or '—' }}</td>
              </tr>
              {% else %}
              <tr><td colspan="3" class="text-center py-4" style="color:var(--muted);">No prices recorded yet.</td></tr>
              {% endfor %}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>

    <!-- ==================== FLOCK MANAGEMENT ==================== -->
    <div id="flock-mgmt" class="tab-content">
      <div class="card mb-4">
        <div class="card-header-custom">
          <div class="section-header" style="margin:0;">
            <div class="section-divider"></div>
            <h5><i class="fas fa-layer-group me-2" style="color:var(--accent);"></i>Flock Management</h5>
          </div>
        </div>
        <div class="card-body-custom">
          {% if active_flocks %}
          <div class="alert" style="background:#fef3c7;color:#92400e;border:1px solid #fde68a;font-size:13px;border-radius:10px;padding:12px 16px;margin-bottom:18px;">
            <i class="fas fa-triangle-exclamation me-2"></i>
            <strong>{{ active_flocks[0].batch_name }}</strong> is still Active. You must harvest it first before creating a new batch.
          </div>
          {% else %}
          <div style="font-size:13px;color:var(--muted);margin-bottom:18px;">
            <i class="fas fa-info-circle me-1"></i> Add a new flock batch below. All fields are required.
          </div>
          {% endif %}

          <form method="post" action="/owner/flock/add" class="row g-3">
            <div class="col-md-4">
              <label class="form-label">Batch Suffix / Custom Name <span style="color:var(--muted);font-weight:400;">(optional)</span></label>
              <input name="batch_suffix" class="form-control" placeholder="e.g. Summer Cycle" {% if active_flocks %}disabled{% endif %}>
              <small style="color:var(--muted);">Auto-generated as <code>Batch-{{ current_year }}-X</code> + your suffix.</small>
            </div>
            <div class="col-md-2">
              <label class="form-label">Initial Bird Count <span class="text-danger">*</span></label>
              <input type="number" name="initial_bird_count" class="form-control" placeholder="0" min="0" required {% if active_flocks %}disabled{% endif %}>
            </div>
            <div class="col-md-2">
              <label class="form-label">Cost per Bird (₱) <span style="color:var(--muted);font-weight:400;">(optional)</span></label>
              <input type="number" step="0.01" min="0" name="cost_per_bird" id="ownerFlockCostPerBird" class="form-control" placeholder="0.00" oninput="calcOwnerChickTotal()" {% if active_flocks %}disabled{% endif %}>
              <small id="ownerFlockTotalChickHint" style="color:var(--muted);display:block;margin-top:2px;">Total: ₱0.00</small>
            </div>
            <div class="col-md-2">
              <label class="form-label">Date of Arrival <span class="text-danger">*</span></label>
              <input type="date" name="start_date" class="form-control" required {% if active_flocks %}disabled{% endif %}>
            </div>
            <div class="col-md-2">
              <label class="form-label">Target Harvest <span class="text-danger">*</span></label>
              <input type="date" name="target_harvest_date" class="form-control" required {% if active_flocks %}disabled{% endif %}>
            </div>
            <div class="col-md-2">
              <label class="form-label">Season of Arrival <span class="text-danger">*</span></label>
              <select name="season" class="form-select" required {% if active_flocks %}disabled{% endif %}>
                <option value="">— Select —</option>
                <option value="Dry">Dry</option>
                <option value="Wet">Wet</option>
              </select>
              <small style="color:var(--muted);">Note: Harvest season is identified separately by the Manager.</small>
            </div>
            <div class="col-12">
              <button type="submit" class="btn-farm" {% if active_flocks %}disabled{% endif %} style="padding:10px 24px;">
                <i class="fas fa-plus me-1"></i> Create Flock Batch
              </button>
            </div>
          </form>
          <script>
          function calcOwnerChickTotal() {
            var countInput = document.querySelector('input[name="initial_bird_count"]');
            var costInput = document.getElementById('ownerFlockCostPerBird');
            var hint = document.getElementById('ownerFlockTotalChickHint');
            if (!countInput || !costInput || !hint) return;
            var count = parseFloat(countInput.value) || 0;
            var cost = parseFloat(costInput.value) || 0;
            var total = count * cost;
            hint.innerHTML = total > 0 
              ? 'Chick Expense: <strong style="color:var(--accent);">₱' + total.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) + '</strong> (auto-added to Manager Expenses)' 
              : 'Total: ₱0.00';
          }
          document.addEventListener('DOMContentLoaded', function() {
            var countInput = document.querySelector('input[name="initial_bird_count"]');
            if (countInput) countInput.addEventListener('input', calcOwnerChickTotal);
          });
          </script>
        </div>
      </div>

      <!-- Current/Past Flocks Table -->
      <div class="card">
        <div class="card-header-custom">
          <div class="section-header" style="margin:0;">
            <div class="section-divider"></div>
            <h5><i class="fas fa-list me-2" style="color:var(--accent);"></i>All Flock Batches</h5>
          </div>
        </div>
        <div class="card-body-custom">
          <div class="table-responsive">
            <table class="table table-hover align-middle">
              <thead><tr>
                <th>Batch</th><th>Arrival Season</th><th>Initial</th><th>Current</th><th>Deaths</th><th>Mortality %</th><th>Age</th><th>Start Date</th><th>Status</th><th>Actions</th>
              </tr></thead>
              <tbody>
              {% for f in flocks %}
              <tr>
                <td style="font-weight:700;">{{ f.batch_name }}</td>
                <td>{% if f.season %}<span class="badge-info">{{ f.season }}</span>{% else %}—{% endif %}</td>
                <td>{{ "{:,}".format(f.initial_bird_count) }}</td>
                <td>{{ "{:,}".format(f.current_bird_count) }}</td>
                <td style="color:#dc2626;font-weight:700;">{{ "{:,}".format(f.mortality_count) }}</td>
                <td style="color:{{ '#dc2626' if f.mortality_percentage > 10 else 'var(--text)' }};">{{ f.mortality_percentage }}%</td>
                <td>{{ f.age_days }} / {{ f.target_age_days }}</td>
                <td style="font-size:13px;color:var(--muted);">{{ f.start_date.strftime('%b %d, %Y') if f.start_date else '—' }}</td>
                <td>
                  {% if f.flock_status == 'Active' %}<span class="badge-active">Active</span>
                  {% elif f.flock_status == 'Harvested' %}<span class="badge-harvested">Harvested</span>
                  {% else %}<span class="badge-harvested">Archived</span>{% endif %}
                </td>
                <td>
                  <div class="tbl-actions">
                    {% if f.flock_status == 'Active' %}
                    <button class="btn-sm-icon btn-edit" data-bs-toggle="modal" data-bs-target="#editFlockModal{{ f.batch_id }}" title="Edit"><i class="fas fa-pen"></i></button>
                    {% endif %}
                    {% if f.flock_status == 'Harvested' %}
                    <form method="post" action="/owner/flock/archive/{{ f.batch_id }}" onsubmit="return confirm('Archive {{ f.batch_name }}? This will reset the analytics.')">
                      <button class="btn-sm-icon btn-ok" type="submit" title="Archive & Reset Analytics"><i class="fas fa-box-archive"></i></button>
                    </form>
                    {% endif %}
                    <form method="post" action="/owner/flock/delete/{{ f.batch_id }}" onsubmit="return confirm('Delete flock {{ f.batch_name }}? This removes all its related records.')">
                      <button class="btn-sm-icon btn-del" type="submit"><i class="fas fa-trash"></i></button>
                    </form>
                  </div>
                </td>
              </tr>
              {% else %}
              <tr><td colspan="10" class="text-center py-4" style="color:var(--muted);">No flocks added yet.</td></tr>
              {% endfor %}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>

    <!-- ==================== HARVEST HISTORY ==================== -->
    <div id="harvest-history" class="tab-content">
      <div class="row g-4">
        <div class="col-lg-4">
          <div class="card">
            <div class="card-header-custom">
              <div class="section-header" style="margin:0;">
                <div class="section-divider"></div>
                <h5><i class="fas fa-list me-2" style="color:var(--accent);"></i>Select Batch</h5>
              </div>
            </div>
            <div class="card-body-custom">
              <div style="margin-bottom:12px;">
                <label class="form-label">Sort by Gain/Loss</label>
                <select class="form-select" onchange="location.href='?sort='+this.value+'#harvest-history'">
                  <option value="highest" {% if current_sort == 'highest' %}selected{% endif %}>Highest Gain → Lowest</option>
                  <option value="lowest" {% if current_sort == 'lowest' %}selected{% endif %}>Lowest → Highest Gain</option>
                </select>
              </div>
              <div style="display:flex;flex-direction:column;gap:6px;max-height:500px;overflow-y:auto;">
                {% for h in all_harvest_data %}
                <button type="button" class="harvest-pick-btn" data-batch-id="{{ h.id }}" onclick="showHarvestDetail({{ h.id }})"
                        style="text-align:left;padding:12px 14px;border-radius:10px;border:1px solid var(--border);background:var(--bg);cursor:pointer;transition:all 0.15s;width:100%;">
                  <div style="font-weight:700;font-size:13px;color:var(--text);">{{ h.batch_name }}</div>
                  <div style="font-size:11px;color:var(--muted);margin-top:2px;">{{ h.end_date.strftime('%b %d, %Y') if h.end_date else '—' }}{% if h.season %} · <span style="font-weight:700;">{{ h.season }}</span>{% endif %}</div>
                  <div style="font-size:12px;font-weight:700;margin-top:4px;color:{{ '#15803d' if h.loss_gain and h.loss_gain >= 0 else '#dc2626' }};">
                    {{ '+' if h.loss_gain and h.loss_gain >= 0 else '' }}₱{{ "{:,.0f}".format(h.loss_gain) if h.loss_gain is not none else '—' }}
                  </div>
                </button>
                {% else %}
                <div style="color:var(--muted);font-size:13px;padding:20px;text-align:center;">No harvest history yet.</div>
                {% endfor %}
              </div>
            </div>
          </div>
        </div>

        <div class="col-lg-8">
          <div class="card" id="harvestDetailCard">
            <div class="card-header-custom">
              <div class="section-header" style="margin:0;">
                <div class="section-divider"></div>
                <h5><i class="fas fa-chart-line me-2" style="color:var(--accent);"></i>Performance Data</h5>
              </div>
            </div>
            <div class="card-body-custom" id="harvestDetailBody">
              <div class="text-center py-5" style="color:var(--muted);">
                <i class="fas fa-hand-pointer fa-3x mb-3 d-block"></i>
                <h5 style="font-weight:700;">Select a batch</h5>
                <p>Pick a harvested batch from the list to view its performance data.</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="card mt-4">
        <div class="card-header-custom">
          <div class="section-header" style="margin:0;">
            <div class="section-divider"></div>
            <h5><i class="fas fa-chart-bar me-2" style="color:var(--accent);"></i>Overall Harvest Summary</h5>
          </div>
        </div>
        <div class="card-body-custom">
          <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:14px;">
            <div style="background:{{ '#f0fdf4' if harvest_profit_summary.total_profit >= 0 else '#fef2f2' }};border:1px solid {{ '#bbf7d0' if harvest_profit_summary.total_profit >= 0 else '#fecaca' }};border-radius:10px;padding:14px 16px;">
              <div style="font-size:11px;text-transform:uppercase;letter-spacing:.03em;color:var(--muted);margin-bottom:4px;">Total Profit ({{ harvest_profit_summary.batch_count }} Batch{{ 'es' if harvest_profit_summary.batch_count != 1 else '' }})</div>
              <div style="font-size:22px;font-weight:800;color:{{ '#15803d' if harvest_profit_summary.total_profit >= 0 else '#dc2626' }};">
                {{ '+' if harvest_profit_summary.total_profit >= 0 else '' }}₱{{ "{:,.0f}".format(harvest_profit_summary.total_profit) }}
              </div>
            </div>
            <div style="background:var(--card-bg);border:1px solid var(--border);border-radius:10px;padding:14px 16px;">
              <div style="font-size:11px;text-transform:uppercase;letter-spacing:.03em;color:var(--muted);margin-bottom:4px;">Total Revenue</div>
              <div style="font-size:22px;font-weight:800;">₱{{ "{:,.0f}".format(harvest_profit_summary.total_revenue) }}</div>
            </div>
            <div style="background:var(--card-bg);border:1px solid var(--border);border-radius:10px;padding:14px 16px;">
              <div style="font-size:11px;text-transform:uppercase;letter-spacing:.03em;color:var(--muted);margin-bottom:4px;">Total Batch Expenses</div>
              <div style="font-size:22px;font-weight:800;">₱{{ "{:,.0f}".format(harvest_profit_summary.total_batch_expenses) }}</div>
            </div>
            <div style="background:var(--card-bg);border:1px solid var(--border);border-radius:10px;padding:14px 16px;">
              <div style="font-size:11px;text-transform:uppercase;letter-spacing:.03em;color:var(--muted);margin-bottom:4px;">Cost per kg Live Weight</div>
              <div style="font-size:22px;font-weight:800;">₱{{ "{:,.2f}".format(harvest_profit_summary.cost_per_kg_live) }}</div>
              <div style="font-size:11px;color:var(--muted);">{{ "{:,.0f}".format(harvest_profit_summary.total_live_kg) }} kg total</div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- ==================== SUMMARY REPORTS ==================== -->
    <div id="summary-reports" class="tab-content">
      <div class="card">
        <div class="card-header-custom">
          <div class="section-header" style="margin:0;">
            <div class="section-divider"></div>
            <h5><i class="fas fa-file-alt me-2" style="color:var(--accent);"></i>Farm Head/Manager Reports</h5>
          </div>
          <button class="btn-farm" data-bs-toggle="modal" data-bs-target="#printReportModal" style="font-size:13px;padding:7px 14px;">
            <i class="fas fa-print me-1"></i> Print Report
          </button>
        </div>
        <div class="card-body-custom">
          <div style="font-size:12px;color:var(--muted);margin-bottom:14px;">
            Reports filed by the Farm Head/Manager. <strong>Season</strong> reflects the season during harvest (identified by the Manager).
          </div>
          <div class="table-responsive">
            <table class="table table-hover align-middle">
              <thead><tr><th>Batch</th><th>Age</th><th>Initial</th><th>Harvest</th><th>Mortality</th><th>Start</th><th>Harvest</th><th>ADG</th><th>FCR</th><th>LW</th><th>Season</th><th>Loss/Gain</th><th>Actions</th></tr></thead>
              <tbody>
              {% for r in summary_reports_list %}
              <tr>
                <td style="font-weight:700;">{{ r.batch_name }}</td>
                <td>{{ r.age }}</td>
                <td>{{ "{:,}".format(r.initial_count) }}</td>
                <td>{{ "{:,}".format(r.harvest_count) }}</td>
                <td style="color:{{ '#dc2626' if r.mortality_pct > 10 else 'var(--text)' }};">{{ r.mortality_pct }}%</td>
                <td style="font-size:13px;color:var(--muted);">{{ r.start_date }}</td>
                <td style="font-size:13px;color:var(--muted);">{{ r.harvest_date or '—' }}</td>
                <td>{{ r.adg }}</td>
                <td>{{ r.fcr }}</td>
                <td>{{ r.lw }} g</td>
                <td>
                  {% if r.season == 'Dry' %}<span class="badge-warning">Dry</span>
                  {% elif r.season == 'Wet' %}<span class="badge-info">Wet</span>
                  {% else %}—{% endif %}
                </td>
                <td style="font-weight:700;color:{{ '#15803d' if r.loss_gain and r.loss_gain >= 0 else '#dc2626' }};">
                  {% if r.loss_gain is not none %}
                  {{ '+' if r.loss_gain >= 0 else '' }}₱{{ "{:,.0f}".format(r.loss_gain) }}
                  {% else %}—{% endif %}
                </td>
                <td><a href="/report/{{ r.report_id }}/print" target="_blank" class="btn-farm" style="font-size:12px;padding:5px 12px;"><i class="fas fa-eye me-1"></i>View</a></td>
              </tr>
              {% else %}
              <tr><td colspan="13" class="text-center py-4" style="color:var(--muted);">No reports filed yet.</td></tr>
              {% endfor %}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>

  </div></div></div>

<!-- ==================== MODALS ==================== -->

<!-- Add Price Modal -->
<div class="modal fade" id="addPriceModal" tabindex="-1">
  <div class="modal-dialog modal-dialog-centered">
    <div class="modal-content" style="background:var(--card-bg);border:1px solid var(--border);border-radius:16px;">
      <div class="modal-header" style="border-color:var(--border);">
        <h5 class="modal-title" style="font-weight:800;"><i class="fas fa-peso-sign me-2" style="color:var(--accent);"></i>Record Market Price</h5>
        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
      </div>
      <form method="post" action="/owner/market-price/add">
        <div class="modal-body">
          <div class="mb-3">
            <label class="form-label">Date</label>
            <input type="date" name="record_date" class="form-control" required max="{{ today_str }}" value="{{ today_str }}">
            <small style="color:var(--muted);">Cannot be later than today.</small>
          </div>
          <div class="mb-3"><label class="form-label">Price per kg (₱)</label><input type="number" step="0.01" name="price_per_kg" class="form-control" required></div>
          <div class="mb-1"><label class="form-label">Location (optional)</label><input name="location" class="form-control"></div>
        </div>
        <div class="modal-footer" style="border-color:var(--border);">
          <button type="button" class="btn-ghost" data-bs-dismiss="modal">Cancel</button>
          <button type="submit" class="btn-farm">Save</button>
        </div>
      </form>
    </div>
  </div>
</div>

<!-- Add User Modal -->
<div class="modal fade" id="addUserModal" tabindex="-1">
  <div class="modal-dialog modal-dialog-centered">
    <div class="modal-content" style="background:var(--card-bg);border:1px solid var(--border);border-radius:16px;">
      <div class="modal-header" style="border-color:var(--border);">
        <h5 class="modal-title" style="font-weight:800;"><i class="fas fa-user-plus me-2" style="color:var(--accent);"></i>Add New User</h5>
        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
      </div>
      <form method="post" action="/owner/user/add">
        <div class="modal-body">
          <div class="row g-2 mb-3">
            <div class="col-4"><label class="form-label">First Name</label><input name="first_name" class="form-control" required></div>
            <div class="col-4"><label class="form-label">Middle Name</label><input name="middle_name" class="form-control"></div>
            <div class="col-4"><label class="form-label">Last Name</label><input name="last_name" class="form-control" required></div>
          </div>
          <div class="mb-3">
            <label class="form-label">Phone Number</label>
            <input name="phone_num" class="form-control" required
                   pattern="09[0-9]{9}" maxlength="11" placeholder="09XXXXXXXXX"
                   title="11 digits starting with 09">
            <small style="color:var(--muted);">Format: 09XXXXXXXXX (11 digits).</small>
          </div>
          <div class="row g-2 mb-3">
            <div class="col-6"><label class="form-label">Username</label><input name="username" class="form-control" required></div>
            <div class="col-6"><label class="form-label">Password</label>
              <div style="position:relative;">
                <input type="password" name="password" id="addUserPw" class="form-control" required minlength="6" style="padding-right:38px;">
                <i class="fas fa-eye" style="position:absolute;right:12px;top:50%;transform:translateY(-50%);cursor:pointer;color:var(--muted);" onclick="
                  const f=document.getElementById('addUserPw'); const show = f.type==='password';
                  f.type = show ? 'text' : 'password';
                  this.classList.toggle('fa-eye'); this.classList.toggle('fa-eye-slash');
                "></i>
              </div>
            </div>
          </div>
          <div class="mb-1"><label class="form-label">Role</label>
            <select name="role" class="form-select">
              <option value="Manager">Manager</option>
              <option value="Worker" selected>Worker</option>
            </select>
          </div>
        </div>
        <div class="modal-footer" style="border-color:var(--border);">
          <button type="button" class="btn-ghost" data-bs-dismiss="modal">Cancel</button>
          <button type="submit" class="btn-farm">Add User</button>
        </div>
      </form>
    </div>
  </div>
</div>

<!-- Edit Flock Modals -->
{% for f in flocks %}
<div class="modal fade" id="editFlockModal{{ f.batch_id }}" tabindex="-1">
  <div class="modal-dialog modal-dialog-centered">
    <div class="modal-content" style="background:var(--card-bg);border:1px solid var(--border);border-radius:16px;">
      <div class="modal-header" style="border-color:var(--border);">
        <h5 class="modal-title" style="font-weight:800;">Edit: {{ f.batch_name }}</h5>
        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
      </div>
      <form method="post" action="/owner/flock/edit/{{ f.batch_id }}">
        <div class="modal-body">
          <div class="mb-3"><label class="form-label">Batch Name</label>
            <input name="batch_name" class="form-control" value="{{ f.batch_name }}" required></div>
          <div class="mb-3"><label class="form-label">Current Bird Count</label>
            <div style="font-weight:700;font-size:15px;">{{ "{:,}".format(f.current_bird_count) }}
              <span style="font-weight:400;color:var(--muted);font-size:12px;">— auto-calculated</span>
            </div>
          </div>
          <div class="mt-3"><label class="form-label">Status</label>
            <select name="flock_status" class="form-select">
              <option value="Active" {% if f.flock_status=='Active' %}selected{% endif %}>Active</option>
              <option value="Harvested" {% if f.flock_status=='Harvested' %}selected{% endif %}>Harvested</option>
            </select>
          </div>
        </div>
        <div class="modal-footer" style="border-color:var(--border);">
          <button type="button" class="btn-ghost" data-bs-dismiss="modal">Cancel</button>
          <button type="submit" class="btn-farm">Save Changes</button>
        </div>
      </form>
    </div>
  </div>
</div>
{% endfor %}

<!-- Print Report Modal (Owner) -->
<div class="modal fade" id="printReportModal" tabindex="-1">
  <div class="modal-dialog modal-dialog-centered modal-lg">
    <div class="modal-content" style="background:var(--card-bg);border:1px solid var(--border);border-radius:16px;">
      <div class="modal-header" style="border-color:var(--border);">
        <h5 class="modal-title" style="font-weight:800;"><i class="fas fa-print me-2" style="color:var(--accent);"></i>Generate Summary Report</h5>
        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
      </div>
      <div class="modal-body">
        <p style="font-size:13px;color:var(--muted);margin-bottom:14px;">
          Select which fields you want to include in the report, then choose a batch to print.
        </p>
        <div class="mb-3">
          <label class="form-label">Select Batch</label>
          <select id="reportBatchSelect" class="form-select">
            <option value="">— Select a harvested batch —</option>
            {% for r in summary_reports_list %}
            <option value="{{ r.report_id }}">{{ r.batch_name }} ({{ r.harvest_date }}) — {{ r.season or 'Unknown' }} Season</option>
            {% endfor %}
          </select>
        </div>
        <label class="form-label">Fields to Include</label>
        <div class="report-field-list" id="reportFieldsList">
          <label class="report-field-item"><input type="checkbox" checked data-field="batch_name"> Batch Name</label>
          <label class="report-field-item"><input type="checkbox" checked data-field="age"> Age</label>
          <label class="report-field-item"><input type="checkbox" checked data-field="initial_count"> Initial Count</label>
          <label class="report-field-item"><input type="checkbox" checked data-field="harvest_count"> Harvest Count</label>
          <label class="report-field-item"><input type="checkbox" checked data-field="mortality_pct"> Mortality %</label>
          <label class="report-field-item"><input type="checkbox" checked data-field="start_date"> Start Date</label>
          <label class="report-field-item"><input type="checkbox" checked data-field="harvest_date"> Harvest Date</label>
          <label class="report-field-item"><input type="checkbox" checked data-field="adg"> ADG</label>
          <label class="report-field-item"><input type="checkbox" checked data-field="fcr"> FCR</label>
          <label class="report-field-item"><input type="checkbox" checked data-field="lw"> LW</label>
          <label class="report-field-item"><input type="checkbox" checked data-field="expenses"> Expenses</label>
          <label class="report-field-item"><input type="checkbox" checked data-field="expense_types"> Expense Types</label>
          <label class="report-field-item"><input type="checkbox" checked data-field="season"> Season</label>
          <label class="report-field-item"><input type="checkbox" checked data-field="chick_booster"> Chick Booster</label>
          <label class="report-field-item"><input type="checkbox" checked data-field="grower_pellets"> Grower Pellets</label>
          <label class="report-field-item"><input type="checkbox" checked data-field="finisher_pellets"> Finisher Pellets</label>
          <label class="report-field-item"><input type="checkbox" checked data-field="vaccine_day_12"> Vaccine Day 12</label>
          <label class="report-field-item"><input type="checkbox" checked data-field="vaccine_day_16"> Vaccine Day 16</label>
          <label class="report-field-item"><input type="checkbox" checked data-field="medicines"> Medicines</label>
          <label class="report-field-item"><input type="checkbox" checked data-field="loss_gain"> Loss/Gain</label>
          <label class="report-field-item"><input type="checkbox" checked data-field="price_basis"> Price Basis</label>
          <label class="report-field-item"><input type="checkbox" checked data-field="remarks"> Remarks</label>
        </div>
      </div>
      <div class="modal-footer" style="border-color:var(--border);">
        <button type="button" class="btn-ghost" data-bs-dismiss="modal">Cancel</button>
        <button type="button" class="btn-farm" onclick="openSelectedReport()"><i class="fas fa-print me-1"></i> Open Report</button>
      </div>
    </div>
  </div>
</div>

""" + _BASE_SCRIPT + """
<script>
var harvestDataMap = {
  {% for h in all_harvest_data %}
  "{{ h.id }}": {
    batch_name: "{{ h.batch_name }}",
    age: "{{ h.age }}",
    initial_count: "{{ h.initial_count }}",
    harvest_count: "{{ h.harvest_count }}",
    mortality_pct: "{{ h.mortality_pct }}",
    start_date: "{{ h.start_date.strftime('%b %d, %Y') if h.start_date else '' }}",
    end_date: "{{ h.end_date.strftime('%b %d, %Y') if h.end_date else '' }}",
    adg: "{{ h.adg }}",
    fcr: "{{ h.fcr }}",
    lw: "{{ h.lw }}",
    expenses: "{{ h.expenses }}",
    season: "{{ h.season or '' }}",
    vaccine_day_12: "{{ h.vaccine_day_12 or '' }}",
    vaccine_day_16: "{{ h.vaccine_day_16 or '' }}",
    loss_gain: "{{ h.loss_gain if h.loss_gain is not none else '' }}",
    remarks: "{{ h.remarks or '' }}"
  }{% if not loop.last %},{% endif %}
  {% endfor %}
};

function showHarvestDetail(id) {
  document.querySelectorAll('.harvest-pick-btn').forEach(function(b){
    b.style.borderColor = 'var(--border)';
    b.style.background = 'var(--bg)';
  });
  var btn = document.querySelector('.harvest-pick-btn[data-batch-id="' + id + '"]');
  if (btn) { btn.style.borderColor = '#166534'; btn.style.background = '#f0fdf4'; }

  var d = harvestDataMap[id];
  if (!d) return;
  var lg = d.loss_gain !== '' ? parseFloat(d.loss_gain) : 0;
  var lgColor = lg >= 0 ? '#15803d' : '#dc2626';
  var lgSign = lg >= 0 ? '+' : '';

  var html = '';
  html += '<div style="margin-bottom:16px;"><div style="font-family:Inter,sans-serif;font-size:22px;font-weight:800;">' + d.batch_name + '</div>';
  html += '<div style="font-size:12px;color:var(--muted);">' + d.start_date + ' → ' + d.end_date + ' · ' + d.age + ' days</div></div>';

  html += '<div class="detail-grid">';
  html += '<div class="detail-item"><div class="label">Initial Count</div><div class="value">' + parseInt(d.initial_count).toLocaleString() + '</div></div>';
  html += '<div class="detail-item"><div class="label">Harvest Count</div><div class="value">' + parseInt(d.harvest_count).toLocaleString() + '</div></div>';
  html += '<div class="detail-item"><div class="label">Mortality</div><div class="value" style="color:#dc2626;">' + d.mortality_pct + '%</div></div>';
  html += '<div class="detail-item"><div class="label">Season of Harvest</div><div class="value">' + (d.season || '—') + '</div></div>';
  html += '<div class="detail-item"><div class="label">ADG</div><div class="value" style="color:#15803d;">' + d.adg + ' g/batch</div></div>';
  html += '<div class="detail-item"><div class="label">FCR</div><div class="value" style="color:#d97706;">' + d.fcr + '</div></div>';
  html += '<div class="detail-item"><div class="label">Live Weight</div><div class="value" style="color:#0ea5e9;">' + d.lw + ' g</div></div>';
  html += '<div class="detail-item"><div class="label">Expenses</div><div class="value">₱' + parseFloat(d.expenses).toLocaleString() + '</div></div>';
  html += '<div class="detail-item"><div class="label">Vaccine Day 12</div><div class="value">' + (d.vaccine_day_12 || '—') + '</div></div>';
  html += '<div class="detail-item"><div class="label">Vaccine Day 16</div><div class="value">' + (d.vaccine_day_16 || '—') + '</div></div>';
  html += '<div class="detail-item"><div class="label">Loss/Gain</div><div class="value" style="color:' + lgColor + ';font-size:16px;">' + lgSign + '₱' + Math.abs(lg).toLocaleString() + '</div></div>';
  html += '</div>';

  if (d.remarks) {
    html += '<div style="margin-top:14px;padding:12px;background:var(--bg);border-radius:8px;border:1px solid var(--border);font-size:13px;color:var(--muted);"><i class="fas fa-comment me-1"></i>' + d.remarks + '</div>';
  }

  html += '<div style="margin-top:16px;"><a href="/report/' + id + '/print" target="_blank" class="btn-farm" style="font-size:13px;padding:7px 16px;"><i class="fas fa-print me-1"></i> Print Performance Report</a></div>';

  document.getElementById('harvestDetailBody').innerHTML = html;
}

function openSelectedReport() {
  var sel = document.getElementById('reportBatchSelect');
  if (!sel.value) { alert('Please select a batch first.'); return; }
  var fields = [];
  document.querySelectorAll('#reportFieldsList input[type="checkbox"]:checked').forEach(function(cb) {
    fields.push(cb.dataset.field);
  });
  var url = '/report/' + sel.value + '/print?fields=' + fields.join(',');
  window.open(url, '_blank');
}
</script>
</body></html>
"""

# ─────────────────────────────────────────────────────────────────────────────
# MANAGER DASHBOARD
# ─────────────────────────────────────────────────────────────────────────────
TEMPLATE_MANAGER = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Manager Dashboard — FlockIQ</title>
""" + _BASE_STYLE + """
</head>
<body>
<script>(function(){const t=localStorage.getItem("theme");if(t==="dark")document.documentElement.classList.add("dark");})()</script>
<div id="mobileOverlay" class="mobile-overlay" onclick="toggleSidebar()"></div>
<div class="mobile-topbar">
  <button onclick="toggleSidebar()" style="background:none;border:none;color:var(--text);font-size:20px;"><i class="fas fa-bars"></i></button>
  <span style="font-family:'Inter',sans-serif;font-weight:800;font-size:16px;">FlockIQ</span>
  <button class="theme-toggle" onclick="toggleDark()"><i class="fas fa-moon"></i></button>
</div>
<div class="app-shell">

<nav id="sidebar" class="sidebar">
  <div class="sidebar-brand">
    <div class="brand-icon" style="background:linear-gradient(135deg,#3f6212,#166534);">""" + logo_svg(22) + """</div>
    <div><div class="brand-text">FlockIQ</div><div class="brand-sub">Manager View</div></div>
  </div>
  <div class="sidebar-nav">
    <div class="nav-section-label">Manager Panel</div>
    <a onclick="showTab('mgr-overview', this)" class="nav-link active"><i class="fas fa-gauge"></i> Overview</a>
    <a onclick="showTab('mgr-verification', this)" class="nav-link"><i class="fas fa-clipboard-check"></i> Record Verification {% if pending_submissions %}<span class="badge-count">{{ pending_submissions|length }}</span>{% endif %}</a>
    <a onclick="showTab('mgr-expenses', this)" class="nav-link"><i class="fas fa-receipt"></i> Expenses</a>
    <a onclick="showTab('vaccination-mgmt', this)" class="nav-link"><i class="fas fa-syringe"></i> Vaccination Management</a>
    <a onclick="showTab('vitamin-mgmt', this)" class="nav-link"><i class="fas fa-tablets"></i> Vitamins & Medicine</a>
    <a onclick="showTab('feed-mgmt', this)" class="nav-link"><i class="fas fa-wheat-awn"></i> Feed Inventory</a>
    <a onclick="showTab('mgr-reports', this)" class="nav-link"><i class="fas fa-file-alt"></i> Reports</a>
  </div>
  <div class="sidebar-footer">
    <div style="display:flex;align-items:center;gap:10px;padding:8px 12px;margin-bottom:8px;">
      <div style="width:34px;height:34px;border-radius:50%;background:linear-gradient(135deg,#3f6212,#166534);display:flex;align-items:center;justify-content:center;color:#fff;font-size:13px;"><i class="fas fa-user-tie"></i></div>
      <div><div style="font-size:13px;font-weight:700;">{{ full_name }}</div><span class="role-badge role-manager">Manager</span></div>
    </div>
    <a href="/logout" class="logout-btn"><i class="fas fa-sign-out-alt"></i> Logout</a>
  </div>
</nav>

<div class="main-content">
  <div class="topbar">
    <span class="topbar-title">Manager Dashboard</span>
    <div class="topbar-actions">
      <button class="theme-toggle" onclick="toggleDark()"><i class="fas fa-moon"></i></button>
    </div>
  </div>
  <div class="page-body">

    {% with msgs = get_flashed_messages() %}{% if msgs %}
    {% for m in msgs %}
    <div class="alert alert-success alert-dismissible fade show alert-flash mb-3" role="alert">
      <i class="fas fa-check-circle me-2"></i>{{ m }}
      <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    </div>
    {% endfor %}{% endif %}{% endwith %}

    <!-- ==================== OVERVIEW ==================== -->
    <div id="mgr-overview" class="tab-content active">
        <div class="hero-banner">
          <div style="position:relative;z-index:1;">
            <div style="font-size:13px;font-weight:600;opacity:0.85;margin-bottom:6px;">Manager Portal</div>
            <h2 style="font-family:'Inter',sans-serif;font-weight:800;font-size:24px;margin:0 0 14px;">{{ full_name }} <i class="fas fa-user-tie" style="font-size:16px;opacity:0.8;"></i></h2>
            <div style="display:flex;flex-wrap:wrap;gap:8px;">
              <div class="metric-pill"><i class="fas fa-feather-pointed"></i> {{ totals.remaining }} Remaining Birds</div>
              <div class="metric-pill"><i class="fas fa-skull-crossbones"></i> {{ totals.deaths }} Total Deaths ({{ totals.mortality_pct }}%)</div>
            </div>
          </div>
          <div style="position:relative;z-index:1;">""" + logo_svg(90, 0.25) + """</div>
        </div>

        <div class="stat-grid mb-4">
          <div class="stat-card sc-farm-green">
            <div class="sc-icon"><i class="fas fa-feather-pointed"></i></div>
            <div class="sc-label">Remaining Birds</div>
            <div class="sc-value">{{ totals.remaining }}</div>
          </div>
          <div class="stat-card sc-farm-red">
            <div class="sc-icon"><i class="fas fa-skull-crossbones"></i></div>
            <div class="sc-label">Mortality</div>
            <div class="sc-value">{{ totals.deaths }} <span style="font-size:16px;">({{ totals.mortality_pct }}%)</span></div>
          </div>
          <div class="stat-card sc-farm-blue">
            <div class="sc-icon"><i class="fas fa-syringe"></i></div>
            <div class="sc-label">Next Vaccination</div>
            <div class="sc-value" style="font-size:14px;line-height:1.4;">
              {% if next_vaccination %}
                {{ next_vaccination.name }}<br>
                <span style="font-size:12px;opacity:0.8;">{{ next_vaccination.date.strftime('%b %d, %I:%M %p') }}</span>
              {% else %}—{% endif %}
            </div>
          </div>
          <div class="stat-card sc-farm-olive">
            <div class="sc-icon"><i class="fas fa-pills"></i></div>
            <div class="sc-label">Next Medicine</div>
            <div class="sc-value" style="font-size:14px;line-height:1.4;">
              {% if next_medication %}
                {{ next_medication.name }}<br>
                <span style="font-size:12px;opacity:0.8;">{{ next_medication.date.strftime('%b %d, %I:%M %p') }}</span>
              {% else %}—{% endif %}
            </div>
          </div>
          <div class="stat-card" style="background:linear-gradient(135deg,{{ '#b45309,#f59e0b' if pending_submissions else '#166534,#15803d' }});cursor:pointer;" onclick="showTab('mgr-verification', document.querySelector('[onclick*=mgr-verification]'))">
            <div class="sc-icon"><i class="fas fa-clipboard-check"></i></div>
            <div class="sc-label">Pending Records</div>
            <div class="sc-value">{{ pending_submissions|length }}</div>
          </div>
        </div>

        {% if active_flocks %}
        {% for f in active_flocks %}
        <div class="card mb-4" style="border-left:4px solid #166534;">
          <div class="card-body-custom">
            <div style="display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:16px;">
              <div>
                <div style="font-weight:800;font-size:16px;">{{ f.batch_name }}</div>
                <div style="font-size:13px;color:var(--muted);">Day {{ f.age_days }} of {{ f.target_age_days }} · {{ "{:,}".format(f.current_bird_count) }} birds remaining</div>
              </div>
              <button class="btn-farm" data-bs-toggle="modal" data-bs-target="#harvestFlockModal{{ f.batch_id }}" style="padding:9px 20px;">
                <i class="fas fa-check me-1"></i> Harvest Batch
              </button>
            </div>
          </div>
        </div>

        <!-- Harvest Modal with Price Basis Selection -->
        <div class="modal fade" id="harvestFlockModal{{ f.batch_id }}" tabindex="-1">
          <div class="modal-dialog modal-dialog-centered modal-lg">
            <div class="modal-content" style="background:var(--card-bg);border:1px solid var(--border);border-radius:16px;">
              <div class="modal-header" style="border-color:var(--border);">
                <h5 class="modal-title" style="font-weight:800;"><i class="fas fa-check-circle me-2" style="color:#166534;"></i>Confirm Harvest</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
              </div>
              <form method="post" action="/manager/flock/harvest/{{ f.batch_id }}">
                <div class="modal-body">
                  <p style="font-size:14px;margin-bottom:16px;">Are you sure you want to mark <strong>{{ f.batch_name }}</strong> as Harvested?</p>

                  <div style="background:var(--bg);border-radius:10px;padding:14px;border:1px solid var(--border);margin-bottom:16px;">
                    <div class="confirm-row"><span class="label">Batch</span><span class="value">{{ f.batch_name }}</span></div>
                    <div class="confirm-row"><span class="label">Arrival Season</span><span class="value">{{ f.season or '—' }}</span></div>
                    <div class="confirm-row"><span class="label">Age</span><span class="value">Day {{ f.age_days }} of {{ f.target_age_days }}</span></div>
                    <div class="confirm-row"><span class="label">Initial Count</span><span class="value">{{ "{:,}".format(f.initial_bird_count) }}</span></div>
                    <div class="confirm-row"><span class="label">Current Count</span><span class="value">{{ "{:,}".format(f.current_bird_count) }}</span></div>
                    <div class="confirm-row"><span class="label">Mortality</span><span class="value">{{ f.mortality_count }} ({{ f.mortality_percentage }}%)</span></div>
                  </div>

                  <!-- Season of Harvest (Manager identifies) -->
                  <div style="margin-bottom:16px;">
                    <label class="form-label">Season of Harvest <span class="text-danger">*</span></label>
                    <select name="harvest_season" class="form-select" required>
                      <option value="">— Select Season at Harvest —</option>
                      <option value="Dry">Dry</option>
                      <option value="Wet">Wet</option>
                    </select>
                    <small style="color:var(--muted);display:block;margin-top:4px;">
                      <i class="fas fa-info-circle me-1"></i>This is the season <strong>during harvest</strong>, used for the Summary Reports — not the arrival season.
                    </small>
                  </div>

                  <!-- Price Basis Selection -->
                  <div style="margin-bottom:16px;">
                    <label class="form-label">Price Basis Selection</label>
                    <div style="display:flex;flex-direction:column;gap:8px;">
                      <label class="price-basis-option">
                        <input type="radio" name="price_basis" value="DA" checked
                               onchange="document.getElementById('givenPriceSelect{{ f.batch_id }}').style.display='none'">
                        <div style="flex:1;">
                          <div style="font-weight:700;font-size:14px;">DA Bantay Presyo</div>
                          <div style="font-size:12px;color:var(--muted);">Current DA price: ₱{{ "%.2f"|format(current_da_price) }}/kg</div>
                        </div>
                      </label>
                      <label class="price-basis-option">
                        <input type="radio" name="price_basis" value="Given"
                               onchange="document.getElementById('givenPriceSelect{{ f.batch_id }}').style.display='block'">
                        <div style="flex:1;">
                          <div style="font-weight:700;font-size:14px;">Given Price</div>
                          <div style="font-size:12px;color:var(--muted);">Use a manually recorded price</div>
                        </div>
                      </label>
                    </div>
                    <div id="givenPriceSelect{{ f.batch_id }}" style="display:none;margin-top:12px;">
                      <label class="form-label">Select Given Price</label>
                      <select name="given_price_id" class="form-select">
                        <option value="">— Select a recorded price —</option>
                        {% for mp in market_prices %}
                        <option value="{{ mp.price_id }}">₱{{ "%.2f"|format(mp.price_per_kg) }}/kg — {{ mp.record_date.strftime('%b %d, %Y') }} ({{ mp.location or 'No location' }})</option>
                        {% endfor %}
                      </select>
                    </div>
                  </div>

                  {% if not f.has_data %}
                  <div class="alert" style="background:#fef2f2;color:#991b1b;border:1px solid #fecaca;font-size:13px;border-radius:10px;padding:10px 14px;margin-bottom:12px;">
                    <i class="fas fa-triangle-exclamation me-1"></i>
                    <strong>This batch has no recorded data yet.</strong>
                  </div>
                  {% endif %}
                </div>
                <div class="modal-footer" style="border-color:var(--border);">
                  <button type="button" class="btn-ghost" data-bs-dismiss="modal">Cancel</button>
                  <button type="submit" class="btn-farm" {% if not f.has_data %}disabled style="opacity:0.5;"{% endif %}>
                    Confirm Harvest
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
        {% endfor %}
        {% endif %}

        <div class="card">
          <div class="card-header-custom">
            <div class="section-header" style="margin:0;">
              <div class="section-divider"></div>
              <h5><i class="fas fa-chart-column me-2" style="color:var(--accent);"></i>Flock Analytics — ADG & FCR by Batch</h5>
            </div>
          </div>
          <div class="card-body-custom">
            {% if flock_analytics %}
            <div class="chart-container-sm">
              <canvas id="overviewAnalyticsChart"></canvas>
            </div>
            <script>
            (function(){
              var el = document.getElementById('overviewAnalyticsChart');
              if (el && window.Chart) {
                new Chart(el, {
                  type: 'bar',
                  data: {
                    labels: {{ flock_analytics|map(attribute='flock.batch_name')|list|tojson }},
                    datasets: [
                      { label: 'ADG (g/batch)', data: {{ flock_analytics|map(attribute='analytics.adg')|list|tojson }}, backgroundColor: '#15803d', borderRadius: 6, yAxisID: 'y' },
                      { label: 'FCR', data: {{ flock_analytics|map(attribute='analytics.fcr')|list|tojson }}, backgroundColor: '#d97706', borderRadius: 6, yAxisID: 'y1' }
                    ]
                  },
                  options: {
                    responsive: true, maintainAspectRatio: false,
                    plugins: { legend: { display: true, position: 'top' } },
                    scales: {
                      y: { beginAtZero: true, position: 'left', title: { display: true, text: 'ADG (g/batch)' } },
                      y1: { beginAtZero: true, position: 'right', title: { display: true, text: 'FCR' }, grid: { drawOnChartArea: false } }
                    }
                  }
                });
              }
            })();
            </script>
            {% else %}
            <div class="text-center py-4" style="color:var(--muted);">
              <i class="fas fa-chart-column fa-2x mb-2 d-block"></i>
              No flock data yet.
            </div>
            {% endif %}
          </div>
        </div>
    </div>

    <!-- ==================== RECORD VERIFICATION ==================== -->
    <div id="mgr-verification" class="tab-content">
      <div class="card">
        <div class="card-header-custom">
          <div class="section-header" style="margin:0;">
            <div class="section-divider"></div>
            <h5><i class="fas fa-clipboard-check me-2" style="color:var(--accent);"></i>Pending Worker Submissions</h5>
          </div>
        </div>
        <div class="card-body-custom">
          <div style="font-size:12px;color:var(--muted);margin-bottom:14px;">
            Nothing here affects bird counts, ADG, or FCR until you Approve it.
          </div>
          {% if pending_submissions %}
          <div class="table-responsive">
            <table class="table table-hover align-middle">
              <thead><tr><th>Batch</th><th>Worker</th><th>Date</th><th>Weight</th><th>Mortality</th><th>Feed</th><th></th></tr></thead>
              <tbody>
              {% for s in pending_submissions %}
              <tr>
                <td style="font-weight:700;">{{ s.batch.batch_name if s.batch else '—' }}</td>
                <td>{{ s.worker.full_name if s.worker else '—' }}</td>
                <td style="font-size:13px;color:var(--muted);">{{ s.record_date.strftime('%b %d, %Y') if s.record_date else '—' }}</td>
                <td>{{ s.avg_weight_g }} g</td>
                <td>{{ s.mortality }}{% if s.cause %}<div style="font-size:11px;color:var(--muted);">{{ s.cause }}</div>{% endif %}</td>
                <td>{{ s.feed_kg }} kg{% if s.feed %}<div style="font-size:11px;color:var(--muted);">{{ s.feed.feed_name }}</div>{% endif %}</td>
                <td style="white-space:nowrap;">
                  <form method="post" action="/manager/submission/approve/{{ s.submission_id }}" style="display:inline;">
                    <button type="submit" class="btn-sm-icon btn-ok" title="Approve"><i class="fas fa-check"></i></button>
                  </form>
                  <button type="button" class="btn-sm-icon btn-del" data-bs-toggle="modal" data-bs-target="#rejectModal{{ s.submission_id }}" title="Reject"><i class="fas fa-xmark"></i></button>
                </td>
              </tr>
              {% endfor %}
              </tbody>
            </table>
          </div>
          {% else %}
          <div class="text-center py-4" style="color:var(--muted);">
            <i class="fas fa-clipboard-check fa-2x mb-2 d-block"></i>
            No pending submissions — all caught up.
          </div>
          {% endif %}
        </div>
      </div>
    </div>

    {% for s in pending_submissions %}
    <div class="modal fade" id="rejectModal{{ s.submission_id }}" tabindex="-1">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content" style="background:var(--card-bg);border:1px solid var(--border);border-radius:16px;">
          <div class="modal-header" style="border-color:var(--border);">
            <h5 class="modal-title" style="font-weight:800;"><i class="fas fa-xmark me-2" style="color:#dc2626;"></i>Reject Submission</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <form method="post" action="/manager/submission/reject/{{ s.submission_id }}">
            <div class="modal-body">
              <p style="font-size:13px;color:var(--muted);">{{ s.batch.batch_name if s.batch else '—' }} — {{ s.record_date.strftime('%b %d, %Y') if s.record_date else '—' }}, submitted by {{ s.worker.full_name if s.worker else '—' }}</p>
              <div class="mb-1"><label class="form-label">Reason <span style="font-weight:400;color:var(--muted);">(optional)</span></label>
                <textarea name="review_notes" class="form-control" rows="2" placeholder="e.g. Weight looks off, please re-check"></textarea>
              </div>
            </div>
            <div class="modal-footer" style="border-color:var(--border);">
              <button type="button" class="btn-ghost" data-bs-dismiss="modal">Cancel</button>
              <button type="submit" class="btn-farm" style="background:#dc2626;">Reject</button>
            </div>
          </form>
        </div>
      </div>
    </div>
    {% endfor %}

    <!-- ==================== EXPENSES ==================== -->
    <div id="mgr-expenses" class="tab-content">

      <div class="d-flex flex-wrap align-items-center justify-content-between gap-2 mb-3">
        <div style="font-size:14px;">
          <i class="fas fa-layer-group me-1" style="color:var(--accent);"></i>
          {% if active_flocks %}Showing expenses for <strong>{{ active_flocks[0].batch_name }}</strong> only. They reset when the batch is archived.
          {% else %}No active batch, so there are no current expenses.{% endif %}
        </div>
        <a href="/manager/expenses/history" class="btn-farm" style="font-size:13px;padding:7px 14px;text-decoration:none;"><i class="fas fa-clock-rotate-left me-1"></i> Past Batch Expenses</a>
      </div>

      <div class="stat-grid mb-4">
        <div class="stat-card" style="background:linear-gradient(135deg,#0369a1,#0ea5e9);">
          <div class="sc-icon"><i class="fas fa-droplet"></i></div>
          <div class="sc-label">Water</div>
          <div class="sc-value">₱{{ "{:,.0f}".format(expense_summary.water) }}</div>
        </div>
        <div class="stat-card" style="background:linear-gradient(135deg,#b45309,#facc15);">
          <div class="sc-icon"><i class="fas fa-bolt"></i></div>
          <div class="sc-label">Electricity</div>
          <div class="sc-value">₱{{ "{:,.0f}".format(expense_summary.electricity) }}</div>
        </div>
        <div class="stat-card" style="background:linear-gradient(135deg,#a16207,#d97706);">
          <div class="sc-icon"><i class="fas fa-fire"></i></div>
          <div class="sc-label">LPG</div>
          <div class="sc-value">₱{{ "{:,.0f}".format(expense_summary.lpg) }}</div>
        </div>
        <div class="stat-card" style="background:linear-gradient(135deg,#5b21b6,#7c3aed);">
          <div class="sc-icon"><i class="fas fa-people-carry-box"></i></div>
          <div class="sc-label">Labor</div>
          <div class="sc-value">₱{{ "{:,.0f}".format(expense_summary.labor) }}</div>
        </div>
        <div class="stat-card" style="background:linear-gradient(135deg,#0f766e,#14b8a6);">
          <div class="sc-icon"><i class="fas fa-syringe"></i></div>
          <div class="sc-label">Vaccine</div>
          <div class="sc-value">₱{{ "{:,.0f}".format(expense_summary.vaccine) }}</div>
        </div>
        <div class="stat-card" style="background:linear-gradient(135deg,#a16207,#ca8a04);">
          <div class="sc-icon"><i class="fas fa-egg"></i></div>
          <div class="sc-label">Chicks</div>
          <div class="sc-value">₱{{ "{:,.0f}".format(expense_summary.chick) }}</div>
        </div>
        <div class="stat-card" style="background:linear-gradient(135deg,#9f1239,#be123c);">
          <div class="sc-icon"><i class="fas fa-wheat-awn"></i></div>
          <div class="sc-label">Feed</div>
          <div class="sc-value">₱{{ "{:,.0f}".format(expense_summary.feed) }}</div>
        </div>
        <div class="stat-card" style="background:linear-gradient(135deg,#7c2d12,#c2410c);">
          <div class="sc-icon"><i class="fas fa-file-invoice-dollar"></i></div>
          <div class="sc-label">Total</div>
          <div class="sc-value">₱{{ "{:,.0f}".format(expense_summary.total) }}</div>
        </div>
      </div>

      <div class="card mb-4">
        <div class="card-header-custom">
          <div class="section-header" style="margin:0;">
            <div class="section-divider"></div>
            <h5><i class="fas fa-chart-pie me-2" style="color:var(--accent);"></i>Expense Breakdown</h5>
          </div>
        </div>
        <div class="card-body-custom">
          {% if expense_summary.total > 0 %}
          <div style="display:flex;flex-wrap:wrap;align-items:center;gap:28px;">
            <div class="chart-container-sm" style="max-width:280px;flex:1 1 240px;">
              <canvas id="expensePieChart"></canvas>
            </div>
            <div style="flex:1 1 200px;display:flex;flex-direction:column;gap:10px;">
              <div style="display:flex;align-items:center;gap:8px;font-size:13px;"><span style="width:12px;height:12px;border-radius:3px;background:#0ea5e9;display:inline-block;"></span> Water — ₱{{ "{:,.0f}".format(expense_summary.water) }}</div>
              <div style="display:flex;align-items:center;gap:8px;font-size:13px;"><span style="width:12px;height:12px;border-radius:3px;background:#facc15;display:inline-block;"></span> Electricity — ₱{{ "{:,.0f}".format(expense_summary.electricity) }}</div>
              <div style="display:flex;align-items:center;gap:8px;font-size:13px;"><span style="width:12px;height:12px;border-radius:3px;background:#d97706;display:inline-block;"></span> LPG — ₱{{ "{:,.0f}".format(expense_summary.lpg) }}</div>
              <div style="display:flex;align-items:center;gap:8px;font-size:13px;"><span style="width:12px;height:12px;border-radius:3px;background:#7c3aed;display:inline-block;"></span> Labor — ₱{{ "{:,.0f}".format(expense_summary.labor) }}</div>
              <div style="display:flex;align-items:center;gap:8px;font-size:13px;"><span style="width:12px;height:12px;border-radius:3px;background:#14b8a6;display:inline-block;"></span> Vaccine — ₱{{ "{:,.0f}".format(expense_summary.vaccine) }}</div>
              <div style="display:flex;align-items:center;gap:8px;font-size:13px;"><span style="width:12px;height:12px;border-radius:3px;background:#ca8a04;display:inline-block;"></span> Chicks — ₱{{ "{:,.0f}".format(expense_summary.chick) }}</div>
              <div style="display:flex;align-items:center;gap:8px;font-size:13px;"><span style="width:12px;height:12px;border-radius:3px;background:#be123c;display:inline-block;"></span> Feed — ₱{{ "{:,.0f}".format(expense_summary.feed) }}</div>
              <div style="display:flex;align-items:center;gap:8px;font-size:13px;"><span style="width:12px;height:12px;border-radius:3px;background:#c2410c;display:inline-block;"></span> Other — ₱{{ "{:,.0f}".format(expense_summary.other) }}</div>
            </div>
          </div>
          <script>
          (function(){
            var el = document.getElementById('expensePieChart');
            if (el && window.Chart) {
              new Chart(el, {
                type: 'pie',
                data: {
                  labels: ['Water', 'Electricity', 'LPG', 'Labor', 'Vaccine', 'Chicks', 'Feed', 'Other'],
                  datasets: [{
                    data: [{{ expense_summary.water }}, {{ expense_summary.electricity }}, {{ expense_summary.lpg }}, {{ expense_summary.labor }}, {{ expense_summary.vaccine }}, {{ expense_summary.chick }}, {{ expense_summary.feed }}, {{ expense_summary.other }}],
                    backgroundColor: ['#0ea5e9', '#facc15', '#d97706', '#7c3aed', '#14b8a6', '#ca8a04', '#be123c', '#c2410c'],
                    borderWidth: 0
                  }]
                },
                options: {
                  responsive: true, maintainAspectRatio: false,
                  plugins: {
                    legend: { display: false },
                    tooltip: {
                      callbacks: {
                        label: function(ctx) {
                          var val = ctx.parsed || 0;
                          var total = ctx.dataset.data.reduce(function(a,b){ return a+b; }, 0);
                          var pct = total > 0 ? ((val/total)*100).toFixed(1) : '0.0';
                          return ctx.label + ': ₱' + val.toLocaleString() + ' (' + pct + '%)';
                        }
                      }
                    }
                  }
                }
              });
            }
          })();
          </script>
          {% else %}
          <div class="text-center py-4" style="color:var(--muted);">
            <i class="fas fa-chart-pie fa-2x mb-2 d-block"></i>
            No expenses logged yet.
          </div>
          {% endif %}
        </div>
      </div>

      <div class="card mb-4">
        <div class="card-header-custom">
          <div class="section-header" style="margin:0;">
            <div class="section-divider"></div>
            <h5><i class="fas fa-tags me-2" style="color:var(--accent);"></i>Expense Categories</h5>
          </div>
          <button class="btn-farm" data-bs-toggle="modal" data-bs-target="#addCategoryModal" style="font-size:13px;padding:7px 14px;">
            <i class="fas fa-plus me-1"></i> Add Category
          </button>
        </div>
        <div class="card-body-custom">
          <div style="display:flex;flex-wrap:wrap;gap:8px;">
            {% set system_cats = ['water', 'electricity', 'lpg', 'labor', 'vaccine', 'feed', 'chick', 'chicks'] %}
            {% for c in expense_categories if c.category_name|lower not in system_cats %}
            <form method="post" action="/owner/expense-category/delete/{{ c.expense_category_id }}" onsubmit="return confirm('Delete category?')" style="display:inline-flex;align-items:center;gap:6px;background:var(--sidebar-hover);border-radius:20px;padding:5px 6px 5px 14px;font-size:13px;font-weight:600;">
              {{ c.category_name }}
              <button type="submit" class="btn-sm-icon btn-del" style="width:22px;height:22px;font-size:10px;"><i class="fas fa-xmark"></i></button>
            </form>
            {% else %}
            <span style="color:var(--muted);font-size:13px;">No custom categories yet.</span>
            {% endfor %}
          </div>
        </div>
      </div>

      <div class="analytics-grid">
        <div class="card">
          <div class="card-header-custom">
            <div class="section-header" style="margin:0;"><div class="section-divider"></div>
              <h5><i class="fas fa-droplet me-2" style="color:#0369a1;"></i>Water Expenses</h5></div>
            <button class="btn-farm" data-bs-toggle="modal" data-bs-target="#addWaterModal" style="font-size:12px;padding:6px 12px;"><i class="fas fa-plus me-1"></i> Add</button>
          </div>
          <div class="card-body-custom input-table-section">
            <table class="table table-hover align-middle">
              <thead><tr><th>Date</th><th>Amount</th><th>Status</th><th></th></tr></thead>
              <tbody>
              {% for e in water_expenses %}
              <tr>
                <td style="font-size:13px;color:var(--muted);">{{ e.expense_date.strftime('%b %d, %Y') if e.expense_date else '—' }}</td>
                <td style="font-weight:700;">₱{{ "%.2f"|format(e.water_expense_amount) }}</td>
                <td><form method="post" action="/owner/expense/water/toggle/{{ e.expense_id }}"><button type="submit" class="status-pill {{ 'status-paid' if e.water_expense_status == 'Paid' else 'status-pending' }}" style="border:none;cursor:pointer;">{{ e.water_expense_status }}</button></form></td>
                <td><form method="post" action="/owner/expense/water/delete/{{ e.expense_id }}"><button class="btn-sm-icon btn-del"><i class="fas fa-trash"></i></button></form></td>
              </tr>
              {% else %}<tr><td colspan="4" class="text-center py-3" style="color:var(--muted);font-size:13px;">No water expenses.</td></tr>{% endfor %}
              </tbody>
            </table>
          </div>
        </div>

        <div class="card">
          <div class="card-header-custom">
            <div class="section-header" style="margin:0;"><div class="section-divider"></div>
              <h5><i class="fas fa-bolt me-2" style="color:#b45309;"></i>Electricity Expenses</h5></div>
            <button class="btn-farm" data-bs-toggle="modal" data-bs-target="#addElectricityModal" style="font-size:12px;padding:6px 12px;"><i class="fas fa-plus me-1"></i> Add</button>
          </div>
          <div class="card-body-custom input-table-section">
            <table class="table table-hover align-middle">
              <thead><tr><th>Date</th><th>Amount</th><th>Status</th><th></th></tr></thead>
              <tbody>
              {% for e in electricity_expenses %}
              <tr>
                <td style="font-size:13px;color:var(--muted);">{{ e.expense_date.strftime('%b %d, %Y') if e.expense_date else '—' }}</td>
                <td style="font-weight:700;">₱{{ "%.2f"|format(e.electricity_expense_amount) }}</td>
                <td><form method="post" action="/owner/expense/electricity/toggle/{{ e.expense_id }}"><button type="submit" class="status-pill {{ 'status-paid' if e.electricity_expense_status == 'Paid' else 'status-pending' }}" style="border:none;cursor:pointer;">{{ e.electricity_expense_status }}</button></form></td>
                <td><form method="post" action="/owner/expense/electricity/delete/{{ e.expense_id }}"><button class="btn-sm-icon btn-del"><i class="fas fa-trash"></i></button></form></td>
              </tr>
              {% else %}<tr><td colspan="4" class="text-center py-3" style="color:var(--muted);font-size:13px;">No electricity expenses.</td></tr>{% endfor %}
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <div class="analytics-grid mt-4">
        <div class="card">
          <div class="card-header-custom">
            <div class="section-header" style="margin:0;"><div class="section-divider"></div>
              <h5><i class="fas fa-fire me-2" style="color:#a16207;"></i>LPG Expenses</h5></div>
            <button class="btn-farm" data-bs-toggle="modal" data-bs-target="#addLpgModal" style="font-size:12px;padding:6px 12px;"><i class="fas fa-plus me-1"></i> Add</button>
          </div>
          <div class="card-body-custom input-table-section">
            <table class="table table-hover align-middle">
              <thead><tr><th>Date</th><th>Amount</th><th>Provider</th><th>Status</th><th></th></tr></thead>
              <tbody>
              {% for e in lpg_expenses %}
              <tr>
                <td style="font-size:13px;color:var(--muted);">{{ e.expense_date.strftime('%b %d, %Y') if e.expense_date else '—' }}</td>
                <td style="font-weight:700;">₱{{ "%.2f"|format(e.lpg_expense_amount) }}</td>
                <td style="font-size:13px;color:var(--muted);">{{ e.lpg_provider or '—' }}</td>
                <td><form method="post" action="/owner/expense/lpg/toggle/{{ e.expense_id }}"><button type="submit" class="status-pill {{ 'status-paid' if e.lpg_expense_status == 'Paid' else 'status-pending' }}" style="border:none;cursor:pointer;">{{ e.lpg_expense_status }}</button></form></td>
                <td><form method="post" action="/owner/expense/lpg/delete/{{ e.expense_id }}"><button class="btn-sm-icon btn-del"><i class="fas fa-trash"></i></button></form></td>
              </tr>
              {% else %}<tr><td colspan="5" class="text-center py-3" style="color:var(--muted);font-size:13px;">No LPG expenses.</td></tr>{% endfor %}
              </tbody>
            </table>
          </div>
        </div>

        <div class="card">
          <div class="card-header-custom">
            <div class="section-header" style="margin:0;"><div class="section-divider"></div>
              <h5><i class="fas fa-people-carry-box me-2" style="color:#7c3aed;"></i>Labor Expenses</h5></div>
            <button class="btn-farm" data-bs-toggle="modal" data-bs-target="#addLaborModal" style="font-size:12px;padding:6px 12px;"><i class="fas fa-plus me-1"></i> Add</button>
          </div>
          <div class="card-body-custom input-table-section">
            <table class="table table-hover align-middle">
              <thead><tr><th>Date</th><th>Amount</th><th>Status</th><th></th></tr></thead>
              <tbody>
              {% for e in labor_expenses %}
              <tr>
                <td style="font-size:13px;color:var(--muted);">{{ e.expense_date.strftime('%b %d, %Y') if e.expense_date else '—' }}</td>
                <td style="font-weight:700;">₱{{ "%.2f"|format(e.labor_expense_amount) }}</td>
                <td><form method="post" action="/owner/expense/labor/toggle/{{ e.expense_id }}"><button type="submit" class="status-pill {{ 'status-paid' if e.labor_expense_status == 'Paid' else 'status-pending' }}" style="border:none;cursor:pointer;">{{ e.labor_expense_status }}</button></form></td>
                <td><form method="post" action="/owner/expense/labor/delete/{{ e.expense_id }}"><button class="btn-sm-icon btn-del"><i class="fas fa-trash"></i></button></form></td>
              </tr>
              {% else %}<tr><td colspan="4" class="text-center py-3" style="color:var(--muted);font-size:13px;">No labor expenses.</td></tr>{% endfor %}
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <div class="card mt-4">
        <div class="card-header-custom">
          <div class="section-header" style="margin:0;"><div class="section-divider"></div>
            <h5><i class="fas fa-egg me-2" style="color:#ca8a04;"></i>Chick Expenses</h5></div>
        </div>
        <div class="card-body-custom input-table-section">
          <form method="post" action="/manager/chick-expense/add" style="display:flex;flex-wrap:wrap;gap:8px;align-items:end;margin-bottom:12px;">
            <div><label class="form-label" style="font-size:11px;">Quantity</label><input type="number" name="quantity" min="1" class="form-control" placeholder="Birds" style="width:120px;"></div>
            <div><label class="form-label" style="font-size:11px;">Total amount (₱)</label><input type="number" step="0.01" min="0" name="amount" class="form-control" required style="width:150px;"></div>
            <div><label class="form-label" style="font-size:11px;">Date</label><input type="date" name="expense_date" class="form-control" value="{{ today_str }}" style="width:150px;"></div>
            <button type="submit" class="btn-farm" style="font-size:13px;padding:8px 14px;"><i class="fas fa-plus me-1"></i> Add</button>
            <span style="font-size:11px;color:var(--muted);align-self:center;margin-left:auto;"><i class="fas fa-info-circle me-1"></i>Chick expenses added by the Owner upon flock arrival automatically appear here.</span>
          </form>
          <table class="table table-hover align-middle">
            <thead><tr><th>Date</th><th>Description</th><th>Amount</th><th>Status</th><th></th></tr></thead>
            <tbody>
            {% for e in chick_expenses %}
            <tr>
              <td style="font-size:13px;color:var(--muted);">{{ e.expense_date.strftime('%b %d, %Y') if e.expense_date else '—' }}</td>
              <td style="font-size:13px;">{{ e.description or '—' }}</td>
              <td style="font-weight:700;">₱{{ "%.2f"|format(e.chick_expense_amount) }}</td>
              <td><form method="post" action="/manager/chick-expense/toggle/{{ e.expense_id }}"><button type="submit" class="status-pill {{ 'status-paid' if e.chick_expense_status == 'Paid' else 'status-pending' }}" style="border:none;cursor:pointer;">{{ e.chick_expense_status }}</button></form></td>
              <td><form method="post" action="/manager/chick-expense/delete/{{ e.expense_id }}"><button type="submit" class="btn-sm-icon btn-del"><i class="fas fa-trash"></i></button></form></td>
            </tr>
            {% else %}<tr><td colspan="5" class="text-center py-3" style="color:var(--muted);font-size:13px;">No chick expenses.</td></tr>{% endfor %}
            </tbody>
          </table>
        </div>
      </div>

      <div class="analytics-grid mt-4">
        <div class="card">
          <div class="card-header-custom">
            <div class="section-header" style="margin:0;"><div class="section-divider"></div>
              <h5><i class="fas fa-syringe me-2" style="color:#0f766e;"></i>Vaccine Expenses</h5></div>
          </div>
          <div class="card-body-custom input-table-section">
            <form method="post" action="/manager/vaccine-expense/add" style="display:flex;flex-wrap:wrap;gap:8px;align-items:end;margin-bottom:12px;">
              <div><label class="form-label" style="font-size:11px;">Vaccine</label>
                <select name="vaccine_id" class="form-select" style="width:170px;">
                  <option value="">— Any / other —</option>
                  {% for v in vaccines %}<option value="{{ v.vaccine_id }}">{{ v.vaccine_name }}</option>{% endfor %}
                </select></div>
              <div><label class="form-label" style="font-size:11px;">Amount (₱)</label><input type="number" step="0.01" min="0" name="amount" class="form-control" required style="width:120px;"></div>
              <div><label class="form-label" style="font-size:11px;">Date</label><input type="date" name="expense_date" class="form-control" value="{{ today_str }}" style="width:150px;"></div>
              <button type="submit" class="btn-farm" style="font-size:13px;padding:8px 14px;"><i class="fas fa-plus me-1"></i> Add</button>
            </form>
            <table class="table table-hover align-middle">
              <thead><tr><th>Date</th><th>Description</th><th>Amount</th><th>Status</th><th></th></tr></thead>
              <tbody>
              {% for e in vaccine_expenses %}
              <tr>
                <td style="font-size:13px;color:var(--muted);">{{ e.expense_date.strftime('%b %d, %Y') if e.expense_date else '—' }}</td>
                <td style="font-size:13px;">{{ e.description or '—' }}</td>
                <td style="font-weight:700;">₱{{ "%.2f"|format(e.vaccine_expense_amount) }}</td>
                <td><form method="post" action="/manager/vaccine-expense/toggle/{{ e.expense_id }}"><button type="submit" class="status-pill {{ 'status-paid' if e.vaccine_expense_status == 'Paid' else 'status-pending' }}" style="border:none;cursor:pointer;">{{ e.vaccine_expense_status }}</button></form></td>
                <td><form method="post" action="/manager/vaccine-expense/delete/{{ e.expense_id }}"><button type="submit" class="btn-sm-icon btn-del"><i class="fas fa-trash"></i></button></form></td>
              </tr>
              {% else %}<tr><td colspan="5" class="text-center py-3" style="color:var(--muted);font-size:13px;">No vaccine expenses.</td></tr>{% endfor %}
              </tbody>
            </table>
          </div>
        </div>

        <div class="card">
          <div class="card-header-custom">
            <div class="section-header" style="margin:0;"><div class="section-divider"></div>
              <h5><i class="fas fa-wheat-awn me-2" style="color:#be123c;"></i>Feed Expenses</h5></div>
          </div>
          <div class="card-body-custom input-table-section">
            <form method="post" action="/manager/feed-expense/add" style="display:flex;flex-wrap:wrap;gap:8px;align-items:end;margin-bottom:12px;">
              <div><label class="form-label" style="font-size:11px;">Feed</label>
                <select name="feed_record_id" class="form-select" style="width:170px;">
                  <option value="">— Any / other —</option>
                  {% for fr in feed_records %}<option value="{{ fr.feed_record_id }}">{{ fr.feed_category }} — {{ fr.feed_name }}</option>{% endfor %}
                </select></div>
              <div><label class="form-label" style="font-size:11px;">Amount (₱)</label><input type="number" step="0.01" min="0" name="amount" class="form-control" required style="width:120px;"></div>
              <div><label class="form-label" style="font-size:11px;">Date</label><input type="date" name="expense_date" class="form-control" value="{{ today_str }}" style="width:150px;"></div>
              <button type="submit" class="btn-farm" style="font-size:13px;padding:8px 14px;"><i class="fas fa-plus me-1"></i> Add</button>
            </form>
            <table class="table table-hover align-middle">
              <thead><tr><th>Date</th><th>Description</th><th>Amount</th><th>Status</th><th></th></tr></thead>
              <tbody>
              {% for e in feed_expenses %}
              <tr>
                <td style="font-size:13px;color:var(--muted);">{{ e.expense_date.strftime('%b %d, %Y') if e.expense_date else '—' }}</td>
                <td style="font-size:13px;">{{ e.description or '—' }}</td>
                <td style="font-weight:700;">₱{{ "%.2f"|format(e.feed_expense_amount) }}</td>
                <td><form method="post" action="/manager/feed-expense/toggle/{{ e.expense_id }}"><button type="submit" class="status-pill {{ 'status-paid' if e.feed_expense_status == 'Paid' else 'status-pending' }}" style="border:none;cursor:pointer;">{{ e.feed_expense_status }}</button></form></td>
                <td><form method="post" action="/manager/feed-expense/delete/{{ e.expense_id }}"><button type="submit" class="btn-sm-icon btn-del"><i class="fas fa-trash"></i></button></form></td>
              </tr>
              {% else %}<tr><td colspan="5" class="text-center py-3" style="color:var(--muted);font-size:13px;">No feed expenses.</td></tr>{% endfor %}
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <div class="mt-4">
        <div class="section-header">
          <div class="section-divider"></div>
          <h5><i class="fas fa-sack-dollar me-2" style="color:#c2410c;"></i>Other Expenses by Category</h5>
          <button class="btn-farm ms-auto" data-bs-toggle="modal" data-bs-target="#addOtherModal" style="font-size:12px;padding:6px 12px;"><i class="fas fa-plus me-1"></i> Add</button>
        </div>

        {% if other_by_category %}
        <div class="row g-4">
          {% for cat_name, expenses in other_by_category.items() %}
          <div class="col-md-6">
            <div class="card">
              <div class="card-header-custom">
                <div class="section-header" style="margin:0;">
                  <div class="section-divider"></div>
                  <h5 style="font-size:14px;"><i class="fas fa-tag me-2" style="color:#c2410c;"></i>{{ cat_name }}</h5>
                </div>
                <span style="font-size:12px;color:var(--muted);">
                  Total: ₱{{ "{:,.2f}".format(expenses|sum(attribute='other_expense_amount')) }}
                </span>
              </div>
              <div class="card-body-custom input-table-section">
                <table class="table table-hover align-middle">
                  <thead><tr><th>Date</th><th>Amount</th><th>Status</th><th></th></tr></thead>
                  <tbody>
                  {% for e in expenses %}
                  <tr>
                    <td style="font-size:13px;color:var(--muted);">{{ e.expense_date.strftime('%b %d, %Y') if e.expense_date else '—' }}</td>
                    <td style="font-weight:700;">₱{{ "%.2f"|format(e.other_expense_amount) }}</td>
                    <td><form method="post" action="/owner/expense/other/toggle/{{ e.expense_id }}"><button type="submit" class="status-pill {{ 'status-paid' if e.other_expense_status == 'Paid' else 'status-pending' }}" style="border:none;cursor:pointer;">{{ e.other_expense_status }}</button></form></td>
                    <td><form method="post" action="/owner/expense/other/delete/{{ e.expense_id }}"><button class="btn-sm-icon btn-del"><i class="fas fa-trash"></i></button></form></td>
                  </tr>
                  {% endfor %}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
          {% endfor %}
        </div>
        {% else %}
        <div class="card">
          <div class="card-body-custom text-center py-4" style="color:var(--muted);font-size:13px;">
            <i class="fas fa-sack-dollar fa-2x mb-2 d-block"></i>
            No other expenses logged yet.
          </div>
        </div>
        {% endif %}
      </div>
    </div>

    <!-- ==================== VACCINATION MANAGEMENT ==================== -->
    <div id="vaccination-mgmt" class="tab-content">
      <div class="card mb-4">
        <div class="card-header-custom">
          <div class="section-header" style="margin:0;">
            <div class="section-divider"></div>
            <h5><i class="fas fa-calendar-check me-2" style="color:var(--accent);"></i>Vaccination Scheduling <span style="font-weight:400;color:var(--muted);font-size:12px;">(Day 12 & Day 16 from arrival date)</span></h5>
          </div>
          <button class="btn-farm" data-bs-toggle="modal" data-bs-target="#scheduleVaccinationModal" style="font-size:13px;padding:7px 14px;">
            <i class="fas fa-calendar-plus me-1"></i> Schedule Vaccination
          </button>
        </div>
        <div class="card-body-custom">
          <div style="font-size:12px;color:var(--muted);margin-bottom:14px;">
            <i class="fas fa-info-circle me-1"></i> You can type the vaccine name manually, or pick one from the existing vaccine inventory. Administered vaccinations deduct from stock.
          </div>
          <div class="table-responsive">
            <table class="table table-hover align-middle">
              <thead><tr><th>Batch</th><th>Vaccine</th><th>Dose/Bird</th><th>Scheduled</th><th>Status</th><th>Administered By</th><th>Actions</th></tr></thead>
              <tbody>
              {% for vr in vaccination_records %}
              <tr>
                <td style="font-weight:700;">{{ vr.batch.batch_name if vr.batch else '—' }}</td>
                <td>{{ vr.vaccine_name or '—' }}</td>
                <td>{{ vr.dose_per_bird }} mL</td>
                <td style="font-size:13px;color:var(--muted);">{{ vr.scheduled_date.strftime('%b %d, %Y %I:%M %p') }}{% if vr.batch and vr.batch.start_date %}<br><span style="font-weight:700;color:var(--accent);">Day {{ (vr.scheduled_date.date() - vr.batch.start_date).days }}</span>{% endif %}</td>
                <td>
                  {% if vr.status == 'Scheduled' %}<span class="status-pill status-scheduled">Scheduled</span>
                  {% elif vr.status == 'Administered' %}<span class="status-pill status-administered">Administered</span>
                  {% else %}<span class="status-pill status-missed">{{ vr.status }}</span>{% endif %}
                </td>
                <td style="font-size:13px;color:var(--muted);">{{ vr.administered_by or '—' }}</td>
                <td>
                  <div class="tbl-actions">
                    {% if vr.status == 'Scheduled' %}
                    <button class="btn-sm-icon btn-ok" type="button" title="Mark administered"
                            data-id="{{ vr.vaccination_record_id }}" data-name="{{ vr.vaccine_name }}"
                            onclick="openAdminister(this)"><i class="fas fa-check"></i></button>
                    {% endif %}
                    <form method="post" action="/manager/vaccination/delete/{{ vr.vaccination_record_id }}" onsubmit="return confirm('Delete this schedule entry?')">
                      <button class="btn-sm-icon btn-del" type="submit"><i class="fas fa-trash"></i></button>
                    </form>
                  </div>
                </td>
              </tr>
              {% else %}
              <tr><td colspan="7" class="text-center py-4" style="color:var(--muted);">No vaccinations scheduled yet.</td></tr>
              {% endfor %}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>

    <!-- ==================== VITAMINS & MEDICINE ==================== -->
    <div id="vitamin-mgmt" class="tab-content">
      <div class="card mb-4">
        <div class="card-header-custom">
          <div class="section-header" style="margin:0;">
            <div class="section-divider"></div>
            <h5><i class="fas fa-tablets me-2" style="color:var(--accent);"></i>Vitamins Inventory</h5>
          </div>
          <div style="display:flex;gap:10px;flex-wrap:wrap;">
            <div style="position:relative;">
              <i class="fas fa-magnifying-glass" style="position:absolute;left:12px;top:50%;transform:translateY(-50%);color:var(--muted);font-size:13px;"></i>
              <input type="text" id="vitaminSearchInput" class="form-control" style="padding-left:34px;width:220px;" placeholder="Search vitamins..." onkeyup="filterVitaminTable()">
            </div>
            <button class="btn-farm" data-bs-toggle="modal" data-bs-target="#addVitaminModal" style="font-size:13px;padding:7px 14px;">
              <i class="fas fa-plus me-1"></i> Add Vitamin
            </button>
          </div>
        </div>
        <div class="card-body-custom">
          <div class="table-responsive">
            <table class="table table-hover align-middle" id="vitaminTable">
              <thead><tr><th>Vitamin</th><th>Type</th><th>Expiry</th><th>Quantity</th><th>Actions</th></tr></thead>
              <tbody>
              {% for v in vitamins %}
              <tr>
                <td style="font-weight:700;">{{ v.vitamin_name }}</td>
                <td>{{ v.vitamin_type or '—' }}</td>
                <td style="font-size:13px;color:var(--muted);">{{ v.vitamin_exp_date.strftime('%b %d, %Y') if v.vitamin_exp_date else '—' }}</td>
                <td>{{ v.quantity }} {{ v.unit or 'units' }}</td>
                <td>
                  <div class="tbl-actions">
                    <button class="btn-sm-icon btn-edit" data-bs-toggle="modal" data-bs-target="#editVitaminModal{{ v.vitamin_id }}"><i class="fas fa-pen"></i></button>
                    <form method="post" action="/manager/vitamin/delete/{{ v.vitamin_id }}" onsubmit="return confirm('Remove {{ v.vitamin_name }}?')">
                      <button class="btn-sm-icon btn-del" type="submit"><i class="fas fa-trash"></i></button>
                    </form>
                  </div>
                </td>
              </tr>
              {% else %}
              <tr><td colspan="5" class="text-center py-4" style="color:var(--muted);">No vitamins in inventory yet.</td></tr>
              {% endfor %}
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <div class="card mb-4">
        <div class="card-header-custom">
          <div class="section-header" style="margin:0;">
            <div class="section-divider"></div>
            <h5><i class="fas fa-calendar-check me-2" style="color:var(--accent);"></i>Vitamins Scheduling</h5>
          </div>
          <button class="btn-farm" data-bs-toggle="modal" data-bs-target="#scheduleVitaminModal" style="font-size:13px;padding:7px 14px;" {% if not has_vitamins %}disabled{% endif %}>
            <i class="fas fa-calendar-plus me-1"></i> Schedule Vitamin
          </button>
        </div>
        <div class="card-body-custom">
          {% if not has_vitamins %}
          <div class="alert" style="background:#fef3c7;color:#92400e;border:1px solid #fde68a;font-size:13px;border-radius:10px;padding:10px 14px;margin-bottom:12px;">
            <i class="fas fa-triangle-exclamation me-1"></i>
            <strong>Vitamin inventory is empty.</strong> Add a vitamin first to enable scheduling.
          </div>
          {% endif %}
          <div style="font-size:12px;color:var(--muted);margin-bottom:12px;">
            Scheduling automatically reduces the vitamin inventory.
          </div>
          <div class="table-responsive">
            <table class="table table-hover align-middle">
              <thead><tr><th>Batch</th><th>Vitamin</th><th>Day Given</th><th>Dosage</th><th>Qty Used</th><th>Status</th><th>Actions</th></tr></thead>
              <tbody>
              {% for vs in vitamin_schedules %}
              <tr>
                <td style="font-weight:700;">{{ vs.batch.batch_name if vs.batch else '—' }}</td>
                <td>{{ vs.vitamin.vitamin_name if vs.vitamin else '—' }}</td>
                <td style="font-size:13px;color:var(--muted);">Day {{ vs.day_given }}</td>
                <td>{{ vs.dosage or '—' }}</td>
                <td>{{ vs.quantity_used or 0 }}</td>
                <td>
                  {% if vs.status == 'Scheduled' %}<span class="status-pill status-scheduled">Scheduled</span>
                  {% elif vs.status == 'Administered' %}<span class="status-pill status-administered">Administered</span>
                  {% else %}<span class="status-pill status-skipped">{{ vs.status }}</span>{% endif %}
                </td>
                <td>
                  <div class="tbl-actions">
                    {% if vs.status == 'Scheduled' %}
                    <form method="post" action="/manager/vitamin/administer/{{ vs.schedule_id }}">
                      <button class="btn-sm-icon btn-ok" type="submit" title="Mark administered"><i class="fas fa-check"></i></button>
                    </form>
                    {% endif %}
                    <form method="post" action="/manager/vitamin/delete/{{ vs.schedule_id }}" onsubmit="return confirm('Delete this schedule entry?')">
                      <button class="btn-sm-icon btn-del" type="submit"><i class="fas fa-trash"></i></button>
                    </form>
                  </div>
                </td>
              </tr>
              {% else %}
              <tr><td colspan="7" class="text-center py-4" style="color:var(--muted);">No vitamins scheduled yet.</td></tr>
              {% endfor %}
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <div class="card mb-4">
        <div class="card-header-custom">
          <div class="section-header" style="margin:0;">
            <div class="section-divider"></div>
            <h5><i class="fas fa-capsules me-2" style="color:var(--accent);"></i>Medicine Inventory</h5>
          </div>
          <div style="display:flex;gap:10px;flex-wrap:wrap;">
            <div style="position:relative;">
              <i class="fas fa-magnifying-glass" style="position:absolute;left:12px;top:50%;transform:translateY(-50%);color:var(--muted);font-size:13px;"></i>
              <input type="text" id="medicineSearchInput" class="form-control" style="padding-left:34px;width:220px;" placeholder="Search medicines..." onkeyup="filterMedicineTable()">
            </div>
            <button class="btn-farm" data-bs-toggle="modal" data-bs-target="#addMedicineModal" style="font-size:13px;padding:7px 14px;">
              <i class="fas fa-plus me-1"></i> Add Medicine
            </button>
          </div>
        </div>
        <div class="card-body-custom">
          <div class="table-responsive">
            <table class="table table-hover align-middle" id="medicineTable">
              <thead><tr><th>Medicine</th><th>Type</th><th>Expiry</th><th>Quantity</th><th>Actions</th></tr></thead>
              <tbody>
              {% for m in medicines %}
              <tr>
                <td style="font-weight:700;">{{ m.medicine_name }}</td>
                <td>{{ m.medicine_type or '—' }}</td>
                <td style="font-size:13px;color:var(--muted);">{{ m.medicine_exp_date.strftime('%b %d, %Y') if m.medicine_exp_date else '—' }}</td>
                <td>{{ m.quantity }} {{ m.unit or 'units' }}</td>
                <td>
                  <div class="tbl-actions">
                    <button class="btn-sm-icon btn-edit" data-bs-toggle="modal" data-bs-target="#editMedicineModal{{ m.medicine_id }}"><i class="fas fa-pen"></i></button>
                    <form method="post" action="/manager/medicine-inventory/delete/{{ m.medicine_id }}" onsubmit="return confirm('Remove {{ m.medicine_name }}?')">
                      <button class="btn-sm-icon btn-del" type="submit"><i class="fas fa-trash"></i></button>
                    </form>
                  </div>
                </td>
              </tr>
              {% else %}
              <tr><td colspan="5" class="text-center py-4" style="color:var(--muted);">No medicines in inventory yet.</td></tr>
              {% endfor %}
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <div class="card">
        <div class="card-header-custom">
          <div class="section-header" style="margin:0;">
            <div class="section-divider"></div>
            <h5><i class="fas fa-pills me-2" style="color:var(--accent);"></i>Medicine Scheduling</h5>
          </div>
          <button class="btn-farm" data-bs-toggle="modal" data-bs-target="#scheduleMedicineModal" style="font-size:13px;padding:7px 14px;" {% if not has_medicines %}disabled{% endif %}>
            <i class="fas fa-calendar-plus me-1"></i> Schedule Medicine
          </button>
        </div>
        <div class="card-body-custom">
          {% if not has_medicines %}
          <div class="alert" style="background:#fef3c7;color:#92400e;border:1px solid #fde68a;font-size:13px;border-radius:10px;padding:10px 14px;margin-bottom:12px;">
            <i class="fas fa-triangle-exclamation me-1"></i>
            <strong>Medicine inventory is empty.</strong> Add a medicine first to enable scheduling.
          </div>
          {% endif %}
          <div style="font-size:12px;color:var(--muted);margin-bottom:12px;">
            Scheduling automatically reduces the medicine inventory.
          </div>
          <div class="table-responsive">
            <table class="table table-hover align-middle">
              <thead><tr><th>Batch</th><th>Medicine</th><th>Dosage</th><th>Scheduled</th><th>Qty Used</th><th>Status</th><th>Actions</th></tr></thead>
              <tbody>
              {% for ms in medication_schedules %}
              <tr>
                <td style="font-weight:700;">{{ ms.batch.batch_name if ms.batch else '—' }}</td>
                <td>{{ ms.item_name }}</td>
                <td>{{ ms.dosage or '—' }}</td>
                <td style="font-size:13px;color:var(--muted);">{{ ms.scheduled_date.strftime('%b %d, %Y') }}</td>
                <td>{{ ms.quantity_used or 0 }}</td>
                <td>
                  {% if ms.status == 'Scheduled' %}<span class="status-pill status-scheduled">Scheduled</span>
                  {% elif ms.status == 'Administered' %}<span class="status-pill status-administered">Administered</span>
                  {% else %}<span class="status-pill status-skipped">{{ ms.status }}</span>{% endif %}
                </td>
                <td>
                  <div class="tbl-actions">
                    {% if ms.status == 'Scheduled' %}
                    <form method="post" action="/manager/medicine/administer/{{ ms.schedule_id }}">
                      <button class="btn-sm-icon btn-ok" type="submit" title="Mark administered"><i class="fas fa-check"></i></button>
                    </form>
                    {% endif %}
                    <form method="post" action="/manager/medicine/delete/{{ ms.schedule_id }}" onsubmit="return confirm('Delete this schedule entry?')">
                      <button class="btn-sm-icon btn-del" type="submit"><i class="fas fa-trash"></i></button>
                    </form>
                  </div>
                </td>
              </tr>
              {% else %}
              <tr><td colspan="7" class="text-center py-4" style="color:var(--muted);">No medicines scheduled yet.</td></tr>
              {% endfor %}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>

    <!-- ==================== FEED INVENTORY ==================== -->
    <div id="feed-mgmt" class="tab-content">
      <div class="card">
        <div class="card-header-custom">
          <div class="section-header" style="margin:0;">
            <div class="section-divider"></div>
            <h5><i class="fas fa-wheat-awn me-2" style="color:var(--accent);"></i>Feed Inventory</h5>
          </div>
          <div style="display:flex;gap:10px;flex-wrap:wrap;">
            <div style="position:relative;">
              <i class="fas fa-magnifying-glass" style="position:absolute;left:12px;top:50%;transform:translateY(-50%);color:var(--muted);font-size:13px;"></i>
              <input type="text" id="feedSearchInput" class="form-control" style="padding-left:34px;width:220px;" placeholder="Search feed..." onkeyup="filterFeedTable()">
            </div>
            <button class="btn-farm" data-bs-toggle="modal" data-bs-target="#addFeedModal" style="font-size:13px;padding:7px 14px;">
              <i class="fas fa-plus me-1"></i> Add Feed Type
            </button>
          </div>
        </div>
        <div class="card-body-custom">
          <div class="table-responsive">
            <table class="table table-hover align-middle" id="feedTable">
              <thead><tr>
                <th>Category</th><th>Feed Name</th>
                <th>CP %</th><th>Fat %</th><th>Fiber %</th><th>Moisture %</th><th>Ca %</th><th>P %</th>
                <th>Expiration</th><th>Remaining</th><th>Actions</th>
              </tr></thead>
              <tbody>
              {% for f in feed_records %}
              <tr>
                <td><span class="badge {{ 'badge-success' if f.feed_category == 'Chick Booster' else ('badge-warning' if f.feed_category == 'Grower Pellets' else 'badge-info') }}">{{ f.feed_category }}</span></td>
                <td style="font-weight:700;">{{ f.feed_name }}</td>
                <td>{{ f.crude_protein }}%</td>
                <td>{{ f.crude_fat }}%</td>
                <td>{{ f.crude_fiber }}%</td>
                <td>{{ f.moisture }}%</td>
                <td>{{ f.calcium }}%</td>
                <td>{{ f.phosphorus }}%</td>
                <td style="font-size:13px;color:var(--muted);">{{ f.expiration_date.strftime('%b %d, %Y') if f.expiration_date else '—' }}</td>
                <td>
                  {% if f.remaining_quantity <= 50 %}
                  <span class="status-pill status-missed">{{ f.remaining_quantity }} kg</span>
                  {% else %}{{ f.remaining_quantity }} kg{% endif %}
                </td>
                <td>
                  <div class="tbl-actions">
                    <button class="btn-sm-icon btn-edit" data-bs-toggle="modal" data-bs-target="#editFeedModal{{ f.feed_record_id }}"><i class="fas fa-pen"></i></button>
                    <form method="post" action="/manager/feed/delete/{{ f.feed_record_id }}" onsubmit="return confirm('Remove {{ f.feed_name }}?')">
                      <button class="btn-sm-icon btn-del" type="submit"><i class="fas fa-trash"></i></button>
                    </form>
                  </div>
                </td>
              </tr>
              {% else %}
              <tr><td colspan="11" class="text-center py-4" style="color:var(--muted);">No feed types added yet.</td></tr>
              {% endfor %}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>

    <!-- ==================== REPORTS ==================== -->
    <div id="mgr-reports" class="tab-content">
      <div class="card">
        <div class="card-header-custom">
          <div class="section-header" style="margin:0;">
            <div class="section-divider"></div>
            <h5><i class="fas fa-file-alt me-2" style="color:var(--accent);"></i>Submit Performance Report</h5>
          </div>
        </div>
        <div class="card-body-custom">
          <div style="font-size:12px;color:var(--muted);margin-bottom:14px;">
            Select the batch, then preview and submit to Owner. The <strong>Season</strong> shown in the report is the one you selected at harvest time.
          </div>
          <div class="row g-3 mb-4">
            <div class="col-md-4">
              <label class="form-label">Select Harvested Batch</label>
              <select id="mgrReportBatchSelect" class="form-select">
                <option value="">— Select a harvested batch —</option>
                {% for h in harvest_history %}
                <option value="{{ h.id }}">{{ h.batch_name }} ({{ h.end_date.strftime('%b %d, %Y') if h.end_date else '—' }}) — {{ h.season or 'Unknown' }} Season</option>
                {% endfor %}
              </select>
            </div>
            <div class="col-md-5 d-flex align-items-end gap-2">
              <button type="button" class="btn-farm" onclick="previewMgrReport()">
                <i class="fas fa-eye me-1"></i> Preview Report
              </button>
              <button type="button" class="btn-ghost" onclick="printMgrReport()">
                <i class="fas fa-print me-1"></i> Print
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

  </div></div></div>

<!-- ==================== MODALS ==================== -->

<!-- Schedule Vaccination Modal -->
<div class="modal fade" id="scheduleVaccinationModal" tabindex="-1">
  <div class="modal-dialog modal-dialog-centered">
    <div class="modal-content" style="background:var(--card-bg);border:1px solid var(--border);border-radius:16px;">
      <div class="modal-header" style="border-color:var(--border);">
        <h5 class="modal-title" style="font-weight:800;"><i class="fas fa-calendar-plus me-2" style="color:var(--accent);"></i>Schedule Vaccination</h5>
        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
      </div>
      <form method="post" action="/manager/vaccination/schedule">
        <div class="modal-body">
          <div class="mb-3"><label class="form-label">Flock Batch</label>
            <select name="batch_id" class="form-select" required>
              {% for f in active_flocks %}<option value="{{ f.batch_id }}">{{ f.batch_name }} (arrived {{ f.start_date.strftime('%b %d, %Y') if f.start_date else '—' }})</option>{% endfor %}
            </select>
          </div>
          {% for day in [12, 16] %}
          <div class="p-3 mb-3" style="border:1px solid var(--border);border-radius:10px;background:var(--bg);">
            <div style="font-weight:700;margin-bottom:10px;color:var(--accent);">Day {{ day }}</div>
            <div class="row g-2">
              <div class="col-12">
                <label class="form-label" style="font-size:11px;">Vaccine Name (Manual Input) <span class="text-danger">*</span></label>
                <input type="text" name="vaccine_name_manual_{{ day }}" class="form-control" placeholder="Type vaccine name here..." required>
                <small style="color:var(--muted);">Enter the vaccine name manually</small>
              </div>
            </div>
            <div class="row g-2 mt-2">
              <div class="col-12">
                <label class="form-label" style="font-size:11px;">Or Quick-Select from Inventory (optional)</label>
                <select name="vaccine_name_{{ day }}" class="form-select" onchange="if(this.value) document.querySelector('input[name=vaccine_name_manual_{{ day }}]').value = this.value;">
                  <option value="">— none —</option>
                  {% for v in vaccines %}<option value="{{ v.vaccine_name }}">{{ v.vaccine_name }}</option>{% endfor %}
                </select>
              </div>
            </div>
            <div class="row g-2 mt-2">
              <div class="col-6"><label class="form-label" style="font-size:11px;">Dose/Bird (mL)</label><input type="number" step="0.01" name="dose_{{ day }}" class="form-control" value="0.03"></div>
            </div>
          </div>
          {% endfor %}
          <div class="mb-3"><label class="form-label">Time</label><input type="time" name="schedule_time" class="form-control" value="08:00" style="max-width:160px;"></div>
          <div class="mb-1"><label class="form-label">Administered / Assigned To <span style="font-weight:400;color:var(--muted);">(optional)</span></label>
            <input name="administered_by" class="form-control" value="{{ full_name }}" placeholder="Name of person">
          </div>
        </div>
        <div class="modal-footer" style="border-color:var(--border);">
          <button type="button" class="btn-ghost" data-bs-dismiss="modal">Cancel</button>
          <button type="submit" class="btn-farm">Schedule</button>
        </div>
      </form>
    </div>
  </div>
</div>

<!-- Administer Vaccination Modal -->
<div class="modal fade" id="administerVaccinationModal" tabindex="-1">
  <div class="modal-dialog modal-dialog-centered">
    <div class="modal-content" style="background:var(--card-bg);border:1px solid var(--border);border-radius:16px;">
      <div class="modal-header" style="border-color:var(--border);">
        <h5 class="modal-title" style="font-weight:800;"><i class="fas fa-syringe me-2" style="color:var(--accent);"></i>Mark Administered</h5>
        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
      </div>
      <form method="post" id="administerVaccinationForm" action="">
        <div class="modal-body">
          <div id="administerVaxName" style="font-weight:700;margin-bottom:10px;"></div>
          <label class="form-label">Administered By</label>
          <input name="administered_by" class="form-control" value="{{ full_name }}" required>
        </div>
        <div class="modal-footer" style="border-color:var(--border);">
          <button type="button" class="btn-ghost" data-bs-dismiss="modal">Cancel</button>
          <button type="submit" class="btn-farm">Confirm</button>
        </div>
      </form>
    </div>
  </div>
</div>

<script>
function openAdminister(btn) {
  document.getElementById('administerVaccinationForm').action = '/manager/vaccination/administer/' + btn.dataset.id;
  document.getElementById('administerVaxName').textContent = btn.dataset.name || '';
  new bootstrap.Modal(document.getElementById('administerVaccinationModal')).show();
}
</script>

<!-- Add Vitamin Modal -->
<div class="modal fade" id="addVitaminModal" tabindex="-1">
  <div class="modal-dialog modal-dialog-centered">
    <div class="modal-content" style="background:var(--card-bg);border:1px solid var(--border);border-radius:16px;">
      <div class="modal-header" style="border-color:var(--border);">
        <h5 class="modal-title" style="font-weight:800;"><i class="fas fa-tablets me-2" style="color:var(--accent);"></i>Add Vitamin</h5>
        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
      </div>
      <form method="post" action="/manager/vitamin/add">
        <div class="modal-body">
          <div class="mb-3"><label class="form-label">Vitamin Name</label><input name="vitamin_name" class="form-control" required></div>
          <div class="row g-2 mb-3">
            <div class="col-6"><label class="form-label">Type</label>
              <select name="vitamin_type" class="form-select">
                <option value="">— Select —</option>
                <option value="Water-soluble">Water-soluble</option>
                <option value="Fat-soluble">Fat-soluble</option>
              </select>
            </div>
            <div class="col-6"><label class="form-label">Expiry Date</label><input type="date" name="vitamin_exp_date" class="form-control"></div>
          </div>
          <div class="row g-2 mb-3">
            <div class="col-6"><label class="form-label">Quantity</label><input type="number" step="0.01" name="quantity" class="form-control" placeholder="0"></div>
            <div class="col-6"><label class="form-label">Unit</label>
              <select name="unit" class="form-select">
                <option value="L">L</option>
                <option value="mL">mL</option>
                <option value="kg">kg</option>
                <option value="g">g</option>
                <option value="sachets">sachets</option>
              </select>
            </div>
          </div>
        </div>
        <div class="modal-footer" style="border-color:var(--border);">
          <button type="button" class="btn-ghost" data-bs-dismiss="modal">Cancel</button>
          <button type="submit" class="btn-farm">Add Vitamin</button>
        </div>
      </form>
    </div>
  </div>
</div>

<!-- Edit Vitamin Modals -->
{% for v in vitamins %}
<div class="modal fade" id="editVitaminModal{{ v.vitamin_id }}" tabindex="-1">
  <div class="modal-dialog modal-dialog-centered">
    <div class="modal-content" style="background:var(--card-bg);border:1px solid var(--border);border-radius:16px;">
      <div class="modal-header" style="border-color:var(--border);">
        <h5 class="modal-title" style="font-weight:800;">Edit: {{ v.vitamin_name }}</h5>
        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
      </div>
      <form method="post" action="/manager/vitamin/edit/{{ v.vitamin_id }}">
        <div class="modal-body">
          <div class="mb-3"><label class="form-label">Vitamin Name</label><input name="vitamin_name" class="form-control" value="{{ v.vitamin_name }}" required></div>
          <div class="row g-2 mb-3">
            <div class="col-6"><label class="form-label">Type</label><input name="vitamin_type" class="form-control" value="{{ v.vitamin_type or '' }}"></div>
            <div class="col-6"><label class="form-label">Expiry Date</label><input type="date" name="vitamin_exp_date" class="form-control" value="{{ v.vitamin_exp_date.strftime('%Y-%m-%d') if v.vitamin_exp_date else '' }}"></div>
          </div>
          <div class="row g-2 mb-3">
            <div class="col-6"><label class="form-label">Quantity</label><input type="number" step="0.01" name="quantity" class="form-control" value="{{ v.quantity }}"></div>
            <div class="col-6"><label class="form-label">Unit</label><input name="unit" class="form-control" value="{{ v.unit or '' }}"></div>
          </div>
        </div>
        <div class="modal-footer" style="border-color:var(--border);">
          <button type="button" class="btn-ghost" data-bs-dismiss="modal">Cancel</button>
          <button type="submit" class="btn-farm">Save Changes</button>
        </div>
      </form>
    </div>
  </div>
</div>
{% endfor %}

<!-- Schedule Vitamin Modal -->
<div class="modal fade" id="scheduleVitaminModal" tabindex="-1">
  <div class="modal-dialog modal-dialog-centered">
    <div class="modal-content" style="background:var(--card-bg);border:1px solid var(--border);border-radius:16px;">
      <div class="modal-header" style="border-color:var(--border);">
        <h5 class="modal-title" style="font-weight:800;"><i class="fas fa-calendar-plus me-2" style="color:var(--accent);"></i>Schedule Vitamin</h5>
        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
      </div>
      <form method="post" action="/manager/vitamin/schedule">
        <div class="modal-body">
          <div class="row g-2 mb-3">
            <div class="col-6"><label class="form-label">Flock Batch</label>
              <select name="batch_id" class="form-select" required>
                {% for f in active_flocks %}<option value="{{ f.batch_id }}">{{ f.batch_name }}</option>{% endfor %}
              </select>
            </div>
            <div class="col-6"><label class="form-label">Vitamin</label>
              <select name="vitamin_id" class="form-select" required>
                {% for v in vitamins %}<option value="{{ v.vitamin_id }}">{{ v.vitamin_name }} ({{ v.quantity }} {{ v.unit }})</option>{% endfor %}
              </select>
            </div>
          </div>
          <div class="row g-2 mb-3">
            <div class="col-4"><label class="form-label">Day Given</label><input type="number" name="day_given" class="form-control" placeholder="12" required></div>
            <div class="col-4"><label class="form-label">Dosage</label><input name="dosage" class="form-control" placeholder="e.g. 2mL/L"></div>
            <div class="col-4"><label class="form-label">Qty to Use</label><input type="number" step="0.01" name="quantity_used" class="form-control" placeholder="0"></div>
          </div>
        </div>
        <div class="modal-footer" style="border-color:var(--border);">
          <button type="button" class="btn-ghost" data-bs-dismiss="modal">Cancel</button>
          <button type="submit" class="btn-farm">Schedule</button>
        </div>
      </form>
    </div>
  </div>
</div>

<!-- Add Medicine Modal -->
<div class="modal fade" id="addMedicineModal" tabindex="-1">
  <div class="modal-dialog modal-dialog-centered">
    <div class="modal-content" style="background:var(--card-bg);border:1px solid var(--border);border-radius:16px;">
      <div class="modal-header" style="border-color:var(--border);">
        <h5 class="modal-title" style="font-weight:800;"><i class="fas fa-capsules me-2" style="color:var(--accent);"></i>Add Medicine</h5>
        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
      </div>
      <form method="post" action="/manager/medicine-inventory/add">
        <div class="modal-body">
          <div class="mb-3"><label class="form-label">Medicine Name</label><input name="medicine_name" class="form-control" placeholder="e.g. Amoxicillin" required></div>
          <div class="row g-2 mb-3">
            <div class="col-6"><label class="form-label">Type</label>
              <select name="medicine_type" class="form-select">
                <option value="">— Select —</option>
                <option value="Antibiotic">Antibiotic</option>
                <option value="Anticoccidial">Anticoccidial</option>
                <option value="Antiparasitic">Antiparasitic</option>
                <option value="Anti-inflammatory">Anti-inflammatory</option>
                <option value="Other">Other</option>
              </select>
            </div>
            <div class="col-6"><label class="form-label">Expiry Date</label><input type="date" name="medicine_exp_date" class="form-control"></div>
          </div>
          <div class="row g-2 mb-3">
            <div class="col-6"><label class="form-label">Quantity</label><input type="number" step="0.01" min="0" name="quantity" class="form-control" placeholder="0"></div>
            <div class="col-6"><label class="form-label">Unit</label><input name="unit" class="form-control" placeholder="e.g. g, mL"></div>
          </div>
        </div>
        <div class="modal-footer" style="border-color:var(--border);">
          <button type="button" class="btn-ghost" data-bs-dismiss="modal">Cancel</button>
          <button type="submit" class="btn-farm">Add Medicine</button>
        </div>
      </form>
    </div>
  </div>
</div>

<!-- Edit Medicine Modals -->
{% for m in medicines %}
<div class="modal fade" id="editMedicineModal{{ m.medicine_id }}" tabindex="-1">
  <div class="modal-dialog modal-dialog-centered">
    <div class="modal-content" style="background:var(--card-bg);border:1px solid var(--border);border-radius:16px;">
      <div class="modal-header" style="border-color:var(--border);">
        <h5 class="modal-title" style="font-weight:800;">Edit: {{ m.medicine_name }}</h5>
        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
      </div>
      <form method="post" action="/manager/medicine-inventory/edit/{{ m.medicine_id }}">
        <div class="modal-body">
          <div class="mb-3"><label class="form-label">Medicine Name</label><input name="medicine_name" class="form-control" value="{{ m.medicine_name }}" required></div>
          <div class="row g-2 mb-3">
            <div class="col-6"><label class="form-label">Type</label><input name="medicine_type" class="form-control" value="{{ m.medicine_type or '' }}"></div>
            <div class="col-6"><label class="form-label">Expiry Date</label><input type="date" name="medicine_exp_date" class="form-control" value="{{ m.medicine_exp_date.strftime('%Y-%m-%d') if m.medicine_exp_date else '' }}"></div>
          </div>
          <div class="row g-2 mb-3">
            <div class="col-6"><label class="form-label">Quantity</label><input type="number" step="0.01" min="0" name="quantity" class="form-control" value="{{ m.quantity }}"></div>
            <div class="col-6"><label class="form-label">Unit</label><input name="unit" class="form-control" value="{{ m.unit or '' }}"></div>
          </div>
        </div>
        <div class="modal-footer" style="border-color:var(--border);">
          <button type="button" class="btn-ghost" data-bs-dismiss="modal">Cancel</button>
          <button type="submit" class="btn-farm">Save Changes</button>
        </div>
      </form>
    </div>
  </div>
</div>
{% endfor %}

<!-- Schedule Medicine Modal -->
<div class="modal fade" id="scheduleMedicineModal" tabindex="-1">
  <div class="modal-dialog modal-dialog-centered">
    <div class="modal-content" style="background:var(--card-bg);border:1px solid var(--border);border-radius:16px;">
      <div class="modal-header" style="border-color:var(--border);">
        <h5 class="modal-title" style="font-weight:800;"><i class="fas fa-pills me-2" style="color:var(--accent);"></i>Schedule Medicine</h5>
        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
      </div>
      <form method="post" action="/manager/medicine/schedule">
        <div class="modal-body">
          <div class="row g-2 mb-3">
            <div class="col-6"><label class="form-label">Flock Batch</label>
              <select name="batch_id" class="form-select" required>
                {% for f in active_flocks %}<option value="{{ f.batch_id }}">{{ f.batch_name }}</option>{% endfor %}
              </select>
            </div>
            <div class="col-6"><label class="form-label">Medicine</label>
              <select name="medicine_id" class="form-select" required>
                {% for m in medicines %}<option value="{{ m.medicine_id }}">{{ m.medicine_name }} ({{ m.quantity }} {{ m.unit }})</option>{% endfor %}
              </select>
            </div>
          </div>
          <div class="row g-2 mb-3">
            <div class="col-4"><label class="form-label">Dosage</label><input name="dosage" class="form-control" placeholder="e.g. 1g/L"></div>
            <div class="col-4"><label class="form-label">Scheduled Date</label><input type="date" name="scheduled_date" class="form-control" required></div>
            <div class="col-4"><label class="form-label">Qty to Use</label><input type="number" step="0.01" name="quantity_used" class="form-control" placeholder="0"></div>
          </div>
          <div class="mb-1"><label class="form-label">Notes</label><input name="notes" class="form-control" placeholder="Optional notes"></div>
        </div>
        <div class="modal-footer" style="border-color:var(--border);">
          <button type="button" class="btn-ghost" data-bs-dismiss="modal">Cancel</button>
          <button type="submit" class="btn-farm">Schedule</button>
        </div>
      </form>
    </div>
  </div>
</div>

<!-- Add Feed Modal -->
<div class="modal fade" id="addFeedModal" tabindex="-1">
  <div class="modal-dialog modal-dialog-centered modal-lg">
    <div class="modal-content" style="background:var(--card-bg);border:1px solid var(--border);border-radius:16px;">
      <div class="modal-header" style="border-color:var(--border);">
        <h5 class="modal-title" style="font-weight:800;"><i class="fas fa-wheat-awn me-2" style="color:var(--accent);"></i>Add Feed Type</h5>
        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
      </div>
      <form method="post" action="/manager/feed/add">
        <div class="modal-body">
          <div class="mb-3"><label class="form-label">Feed Name</label>
            <input name="feed_name" list="phFeedNames" class="form-control" placeholder="Pick a brand or type your own" required>
            <datalist id="phFeedNames">
              <option value="B-MEG Broiler Booster">
              <option value="B-MEG Broiler Grower">
              <option value="B-MEG Broiler Finisher">
              <option value="Pilmico Broiler Starter">
              <option value="Pilmico Broiler Grower">
              <option value="Pilmico Broiler Finisher">
              <option value="Thunderbird Broiler Starter">
              <option value="Thunderbird Broiler Grower">
              <option value="Thunderbird Broiler Finisher">
              <option value="CP Broiler Starter">
              <option value="CP Broiler Grower">
              <option value="CP Broiler Finisher">
            </datalist>
          </div>
          <div class="row g-2 mb-3">
            <div class="col-6"><label class="form-label">Feed Type</label>
              <select name="feed_category" class="form-select" required onchange="applyFeedPreset(this.value)">
                <option value="">— Select —</option>
                <option value="Chick Booster">Chick Booster (0–14 days)</option>
                <option value="Grower Pellets">Grower Pellets (15–28 days)</option>
                <option value="Finisher Pellets">Finisher Pellets (29+ days)</option>
              </select>
            </div>
          </div>
          <label class="form-label">Nutritional Profile (%)</label>
          <div class="row g-2 mb-3">
            <div class="col-4"><label class="form-label" style="font-size:11px;">Crude Protein</label><input type="number" step="0.01" name="crude_protein" class="form-control" placeholder="0"></div>
            <div class="col-4"><label class="form-label" style="font-size:11px;">Crude Fat</label><input type="number" step="0.01" name="crude_fat" class="form-control" placeholder="0"></div>
            <div class="col-4"><label class="form-label" style="font-size:11px;">Crude Fiber</label><input type="number" step="0.01" name="crude_fiber" class="form-control" placeholder="0"></div>
            <div class="col-4"><label class="form-label" style="font-size:11px;">Moisture</label><input type="number" step="0.01" name="moisture" class="form-control" placeholder="0"></div>
            <div class="col-4"><label class="form-label" style="font-size:11px;">Calcium</label><input type="number" step="0.01" name="calcium" class="form-control" placeholder="0"></div>
            <div class="col-4"><label class="form-label" style="font-size:11px;">Phosphorus</label><input type="number" step="0.01" name="phosphorus" class="form-control" placeholder="0"></div>
          </div>
          <div class="row g-2 mb-3">
            <div class="col-6"><label class="form-label">Remaining (kg)</label><input type="number" step="0.1" name="remaining_quantity" class="form-control" placeholder="0"></div>
            <div class="col-6"><label class="form-label">Expiration Date</label><input type="date" name="expiration_date" class="form-control"></div>
          </div>
        </div>
        <div class="modal-footer" style="border-color:var(--border);">
          <button type="button" class="btn-ghost" data-bs-dismiss="modal">Cancel</button>
          <button type="submit" class="btn-farm">Add Feed</button>
        </div>
      </form>
      <script>
        var FEED_PRESETS = {
          'Chick Booster':    { crude_protein: 22.0, crude_fat: 5.0, crude_fiber: 4.0, moisture: 12.0, calcium: 1.00, phosphorus: 0.45 },
          'Grower Pellets':   { crude_protein: 20.0, crude_fat: 5.0, crude_fiber: 4.5, moisture: 12.0, calcium: 0.90, phosphorus: 0.42 },
          'Finisher Pellets': { crude_protein: 18.0, crude_fat: 5.5, crude_fiber: 5.0, moisture: 12.0, calcium: 0.85, phosphorus: 0.40 }
        };
        function applyFeedPreset(cat) {
          var preset = FEED_PRESETS[cat];
          var form = document.getElementById('addFeedModal').querySelector('form');
          if (!preset) return;
          Object.keys(preset).forEach(function (k) {
            if (form.elements[k]) form.elements[k].value = preset[k];
          });
        }
      </script>
    </div>
  </div>
</div>

<!-- Edit Feed Modals -->
{% for f in feed_records %}
<div class="modal fade" id="editFeedModal{{ f.feed_record_id }}" tabindex="-1">
  <div class="modal-dialog modal-dialog-centered modal-lg">
    <div class="modal-content" style="background:var(--card-bg);border:1px solid var(--border);border-radius:16px;">
      <div class="modal-header" style="border-color:var(--border);">
        <h5 class="modal-title" style="font-weight:800;">Edit: {{ f.feed_name }}</h5>
        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
      </div>
      <form method="post" action="/manager/feed/edit/{{ f.feed_record_id }}">
        <div class="modal-body">
          <div class="mb-3"><label class="form-label">Feed Name</label><input name="feed_name" class="form-control" value="{{ f.feed_name }}" required></div>
          <div class="row g-2 mb-3">
            <div class="col-6"><label class="form-label">Category</label>
              <select name="feed_category" class="form-select" required>
                <option value="Chick Booster" {% if f.feed_category == 'Chick Booster' %}selected{% endif %}>Chick Booster</option>
                <option value="Grower Pellets" {% if f.feed_category == 'Grower Pellets' %}selected{% endif %}>Grower Pellets</option>
                <option value="Finisher Pellets" {% if f.feed_category == 'Finisher Pellets' %}selected{% endif %}>Finisher Pellets</option>
              </select>
            </div>
          </div>
          <label class="form-label">Nutritional Profile (%)</label>
          <div class="row g-2 mb-3">
            <div class="col-4"><label class="form-label" style="font-size:11px;">Crude Protein</label><input type="number" step="0.01" name="crude_protein" class="form-control" value="{{ f.crude_protein }}"></div>
            <div class="col-4"><label class="form-label" style="font-size:11px;">Crude Fat</label><input type="number" step="0.01" name="crude_fat" class="form-control" value="{{ f.crude_fat }}"></div>
            <div class="col-4"><label class="form-label" style="font-size:11px;">Crude Fiber</label><input type="number" step="0.01" name="crude_fiber" class="form-control" value="{{ f.crude_fiber }}"></div>
            <div class="col-4"><label class="form-label" style="font-size:11px;">Moisture</label><input type="number" step="0.01" name="moisture" class="form-control" value="{{ f.moisture }}"></div>
            <div class="col-4"><label class="form-label" style="font-size:11px;">Calcium</label><input type="number" step="0.01" name="calcium" class="form-control" value="{{ f.calcium }}"></div>
            <div class="col-4"><label class="form-label" style="font-size:11px;">Phosphorus</label><input type="number" step="0.01" name="phosphorus" class="form-control" value="{{ f.phosphorus }}"></div>
          </div>
          <div class="row g-2 mb-3">
            <div class="col-6"><label class="form-label">Remaining (kg)</label><input type="number" step="0.1" name="remaining_quantity" class="form-control" value="{{ f.remaining_quantity }}"></div>
            <div class="col-6"><label class="form-label">Expiration Date</label><input type="date" name="expiration_date" class="form-control" value="{{ f.expiration_date.strftime('%Y-%m-%d') if f.expiration_date else '' }}"></div>
          </div>
        </div>
        <div class="modal-footer" style="border-color:var(--border);">
          <button type="button" class="btn-ghost" data-bs-dismiss="modal">Cancel</button>
          <button type="submit" class="btn-farm">Save Changes</button>
        </div>
      </form>
    </div>
  </div>
</div>
{% endfor %}

<!-- Add Category Modal -->
<div class="modal fade" id="addCategoryModal" tabindex="-1">
  <div class="modal-dialog modal-dialog-centered">
    <div class="modal-content" style="background:var(--card-bg);border:1px solid var(--border);border-radius:16px;">
      <div class="modal-header" style="border-color:var(--border);">
        <h5 class="modal-title" style="font-weight:800;">Add Expense Category</h5>
        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
      </div>
      <form method="post" action="/owner/expense-category/add">
        <div class="modal-body">
          <div class="mb-1"><label class="form-label">Category Name</label><input name="category_name" class="form-control" placeholder="e.g. Utilities" required></div>
        </div>
        <div class="modal-footer" style="border-color:var(--border);">
          <button type="button" class="btn-ghost" data-bs-dismiss="modal">Cancel</button>
          <button type="submit" class="btn-farm">Add</button>
        </div>
      </form>
    </div>
  </div>
</div>

<!-- Add Water Modal -->
<div class="modal fade" id="addWaterModal" tabindex="-1">
  <div class="modal-dialog modal-dialog-centered">
    <div class="modal-content" style="background:var(--card-bg);border:1px solid var(--border);border-radius:16px;">
      <div class="modal-header" style="border-color:var(--border);">
        <h5 class="modal-title" style="font-weight:800;"><i class="fas fa-droplet me-2" style="color:#0369a1;"></i>Add Water Expense</h5>
        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
      </div>
      <form method="post" action="/owner/expense/water/add">
        <div class="modal-body">
          <div class="row g-2">
            <div class="col-6"><label class="form-label">Amount (₱)</label><input type="number" step="0.01" name="amount" class="form-control" required></div>
            <div class="col-6"><label class="form-label">Status</label>
              <select name="status" class="form-select"><option value="Pending">Pending</option><option value="Paid">Paid</option></select>
            </div>
          </div>
          <div class="mb-1 mt-2"><label class="form-label">Date</label><input type="date" name="expense_date" class="form-control" value="{{ today_str }}"></div>
        </div>
        <div class="modal-footer" style="border-color:var(--border);">
          <button type="button" class="btn-ghost" data-bs-dismiss="modal">Cancel</button>
          <button type="submit" class="btn-farm">Add</button>
        </div>
      </form>
    </div>
  </div>
</div>

<!-- Add Electricity Modal -->
<div class="modal fade" id="addElectricityModal" tabindex="-1">
  <div class="modal-dialog modal-dialog-centered">
    <div class="modal-content" style="background:var(--card-bg);border:1px solid var(--border);border-radius:16px;">
      <div class="modal-header" style="border-color:var(--border);">
        <h5 class="modal-title" style="font-weight:800;"><i class="fas fa-bolt me-2" style="color:#b45309;"></i>Add Electricity Expense</h5>
        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
      </div>
      <form method="post" action="/owner/expense/electricity/add">
        <div class="modal-body">
          <div class="row g-2">
            <div class="col-6"><label class="form-label">Amount (₱)</label><input type="number" step="0.01" name="amount" class="form-control" required></div>
            <div class="col-6"><label class="form-label">Status</label>
              <select name="status" class="form-select"><option value="Pending">Pending</option><option value="Paid">Paid</option></select>
            </div>
          </div>
          <div class="mb-1 mt-2"><label class="form-label">Date</label><input type="date" name="expense_date" class="form-control" value="{{ today_str }}"></div>
        </div>
        <div class="modal-footer" style="border-color:var(--border);">
          <button type="button" class="btn-ghost" data-bs-dismiss="modal">Cancel</button>
          <button type="submit" class="btn-farm">Add</button>
        </div>
      </form>
    </div>
  </div>
</div>

<!-- Add LPG Modal -->
<div class="modal fade" id="addLpgModal" tabindex="-1">
  <div class="modal-dialog modal-dialog-centered">
    <div class="modal-content" style="background:var(--card-bg);border:1px solid var(--border);border-radius:16px;">
      <div class="modal-header" style="border-color:var(--border);">
        <h5 class="modal-title" style="font-weight:800;"><i class="fas fa-fire me-2" style="color:#a16207;"></i>Add LPG Expense</h5>
        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
      </div>
      <form method="post" action="/owner/expense/lpg/add">
        <div class="modal-body">
          <div class="row g-2 mb-3">
            <div class="col-6"><label class="form-label">Amount (₱)</label><input type="number" step="0.01" name="amount" class="form-control" required></div>
            <div class="col-6"><label class="form-label">Provider</label><input name="lpg_provider" class="form-control" placeholder="e.g. Petron"></div>
          </div>
          <div class="row g-2">
            <div class="col-6"><label class="form-label">Status</label>
              <select name="status" class="form-select"><option value="Pending">Pending</option><option value="Paid">Paid</option></select>
            </div>
            <div class="col-6"><label class="form-label">Date</label><input type="date" name="expense_date" class="form-control" value="{{ today_str }}"></div>
          </div>
        </div>
        <div class="modal-footer" style="border-color:var(--border);">
          <button type="button" class="btn-ghost" data-bs-dismiss="modal">Cancel</button>
          <button type="submit" class="btn-farm">Add</button>
        </div>
      </form>
    </div>
  </div>
</div>

<!-- Add Labor Modal -->
<div class="modal fade" id="addLaborModal" tabindex="-1">
  <div class="modal-dialog modal-dialog-centered">
    <div class="modal-content" style="background:var(--card-bg);border:1px solid var(--border);border-radius:16px;">
      <div class="modal-header" style="border-color:var(--border);">
        <h5 class="modal-title" style="font-weight:800;"><i class="fas fa-people-carry-box me-2" style="color:#7c3aed;"></i>Add Labor Expense</h5>
        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
      </div>
      <form method="post" action="/owner/expense/labor/add">
        <div class="modal-body">
          <div class="row g-2">
            <div class="col-6"><label class="form-label">Amount (₱)</label><input type="number" step="0.01" name="amount" class="form-control" required></div>
            <div class="col-6"><label class="form-label">Status</label>
              <select name="status" class="form-select"><option value="Pending">Pending</option><option value="Paid">Paid</option></select>
            </div>
          </div>
          <div class="mb-1 mt-2"><label class="form-label">Date</label><input type="date" name="expense_date" class="form-control" value="{{ today_str }}"></div>
        </div>
        <div class="modal-footer" style="border-color:var(--border);">
          <button type="button" class="btn-ghost" data-bs-dismiss="modal">Cancel</button>
          <button type="submit" class="btn-farm">Add</button>
        </div>
      </form>
    </div>
  </div>
</div>

<!-- Add Other Expense Modal -->
<div class="modal fade" id="addOtherModal" tabindex="-1">
  <div class="modal-dialog modal-dialog-centered">
    <div class="modal-content" style="background:var(--card-bg);border:1px solid var(--border);border-radius:16px;">
      <div class="modal-header" style="border-color:var(--border);">
        <h5 class="modal-title" style="font-weight:800;"><i class="fas fa-sack-dollar me-2" style="color:#c2410c;"></i>Add Other Expense</h5>
        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
      </div>
      <form method="post" action="/owner/expense/other/add">
        <div class="modal-body">
          <div class="mb-3"><label class="form-label">Category</label>
            <select name="expense_category_id" class="form-select" required>
              {% for c in expense_categories %}{% if c.category_name|lower not in ['labor', 'water', 'electricity', 'lpg', 'vaccine', 'feed', 'chick', 'chicks'] %}<option value="{{ c.expense_category_id }}">{{ c.category_name }}</option>{% endif %}{% endfor %}
            </select>
          </div>
          <div class="row g-2">
            <div class="col-6"><label class="form-label">Amount (₱)</label><input type="number" step="0.01" name="amount" class="form-control" required></div>
            <div class="col-6"><label class="form-label">Status</label>
              <select name="status" class="form-select"><option value="Pending">Pending</option><option value="Paid">Paid</option></select>
            </div>
          </div>
          <div class="mb-1 mt-2"><label class="form-label">Date</label><input type="date" name="expense_date" class="form-control" value="{{ today_str }}"></div>
        </div>
        <div class="modal-footer" style="border-color:var(--border);">
          <button type="button" class="btn-ghost" data-bs-dismiss="modal">Cancel</button>
          <button type="submit" class="btn-farm">Add</button>
        </div>
      </form>
    </div>
  </div>
</div>

""" + _BASE_SCRIPT + """
<script>
function filterVitaminTable() {
  var term = document.getElementById('vitaminSearchInput').value.trim().toLowerCase();
  var rows = document.querySelectorAll('#vitaminTable tbody tr');
  rows.forEach(function(row) {
    var text = row.textContent.toLowerCase();
    row.style.display = text.indexOf(term) !== -1 ? '' : 'none';
  });
}

function filterMedicineTable() {
  var term = document.getElementById('medicineSearchInput').value.trim().toLowerCase();
  var rows = document.querySelectorAll('#medicineTable tbody tr');
  rows.forEach(function(row) {
    var text = row.textContent.toLowerCase();
    row.style.display = text.indexOf(term) !== -1 ? '' : 'none';
  });
}

function filterFeedTable() {
  var term = document.getElementById('feedSearchInput').value.trim().toLowerCase();
  var rows = document.querySelectorAll('#feedTable tbody tr');
  rows.forEach(function(row) {
    var text = row.textContent.toLowerCase();
    row.style.display = text.indexOf(term) !== -1 ? '' : 'none';
  });
}

function previewMgrReport() {
  var sel = document.getElementById('mgrReportBatchSelect');
  if (!sel.value) { alert('Please select a batch first.'); return; }
  var url = '/report/' + sel.value + '/print?fields=all';
  window.open(url, '_blank');
}

function printMgrReport() {
  previewMgrReport();
}
</script>
</body></html>
"""

# ─────────────────────────────────────────────────────────────────────────────
# WORKER DASHBOARD
# ─────────────────────────────────────────────────────────────────────────────
TEMPLATE_WORKER = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Worker Dashboard — FlockIQ</title>
""" + _BASE_STYLE + """
</head>
<body>
<script>(function(){const t=localStorage.getItem("theme");if(t==="dark")document.documentElement.classList.add("dark");})()</script>
<div id="mobileOverlay" class="mobile-overlay" onclick="toggleSidebar()"></div>
<div class="mobile-topbar">
  <button onclick="toggleSidebar()" style="background:none;border:none;color:var(--text);font-size:20px;"><i class="fas fa-bars"></i></button>
  <span style="font-family:'Inter',sans-serif;font-weight:800;font-size:16px;">FlockIQ</span>
  <button class="theme-toggle" onclick="toggleDark()"><i class="fas fa-moon"></i></button>
</div>
<div class="app-shell">

<nav id="sidebar" class="sidebar">
  <div class="sidebar-brand">
    <div class="brand-icon" style="background:linear-gradient(135deg,#15803d,#166534);">""" + logo_svg(22) + """</div>
    <div><div class="brand-text">FlockIQ</div><div class="brand-sub">Worker View</div></div>
  </div>
  <div class="sidebar-nav">
    <div class="nav-section-label">Worker Panel</div>
    <a onclick="showTab('wkr-overview', this)" class="nav-link active"><i class="fas fa-gauge"></i> Overview</a>
    <a onclick="showTab('wkr-submit', this)" class="nav-link"><i class="fas fa-pen-to-square"></i> Submit Daily Record</a>
    <a onclick="showTab('wkr-weekly', this)" class="nav-link"><i class="fas fa-calendar-week"></i> Submit Weekly Record</a>
  </div>
  <div class="sidebar-footer">
    <div style="display:flex;align-items:center;gap:10px;padding:8px 12px;margin-bottom:8px;">
      <div style="width:34px;height:34px;border-radius:50%;background:linear-gradient(135deg,#15803d,#166534);display:flex;align-items:center;justify-content:center;color:#fff;font-size:13px;"><i class="fas fa-hard-hat"></i></div>
      <div><div style="font-size:13px;font-weight:700;">{{ full_name }}</div><span class="role-badge role-worker">Worker</span></div>
    </div>
    <a href="/logout" class="logout-btn"><i class="fas fa-sign-out-alt"></i> Logout</a>
  </div>
</nav>

<div class="main-content">
  <div class="topbar">
    <span class="topbar-title">Worker Dashboard</span>
    <div class="topbar-actions">
      <button class="theme-toggle" onclick="toggleDark()"><i class="fas fa-moon"></i></button>
    </div>
  </div>
  <div class="page-body">

    {% with msgs = get_flashed_messages() %}{% if msgs %}
    {% for m in msgs %}
    <div class="alert alert-success alert-dismissible fade show alert-flash mb-3" role="alert">
      <i class="fas fa-check-circle me-2"></i>{{ m }}
      <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    </div>
    {% endfor %}{% endif %}{% endwith %}

    <div id="wkr-overview" class="tab-content active">
        <div class="hero-banner">
          <div style="position:relative;z-index:1;">
            <div style="font-size:13px;font-weight:600;opacity:0.85;margin-bottom:6px;">Worker Portal</div>
            <h2 style="font-family:'Inter',sans-serif;font-weight:800;font-size:24px;margin:0 0 14px;">{{ full_name }} <i class="fas fa-hard-hat" style="font-size:16px;opacity:0.8;"></i></h2>
            <div style="display:flex;flex-wrap:wrap;gap:8px;">
              {% if active_batch %}
              <div class="metric-pill"><i class="fas fa-layer-group"></i> Active: {{ active_batch.batch_name }}</div>
              {% endif %}
              <div class="metric-pill"><i class="fas fa-clipboard-list"></i> {{ my_records|length }} Recent Submissions</div>
            </div>
          </div>
          <div style="position:relative;z-index:1;">""" + logo_svg(90, 0.25) + """</div>
        </div>

        {% if active_batch %}
        <div class="card mb-4" style="border-left:4px solid #166534;">
          <div class="card-body-custom">
            <div style="display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:16px;">
              <div>
                <div style="font-size:11px;color:var(--muted);text-transform:uppercase;letter-spacing:.04em;">Current Active Batch</div>
                <div style="font-weight:800;font-size:18px;margin-top:4px;">{{ active_batch.batch_name }}</div>
                <div style="font-size:13px;color:var(--muted);">Day {{ active_batch.age_days }} of {{ active_batch.target_age_days }} · {{ "{:,}".format(active_batch.current_bird_count) }} birds remaining</div>
              </div>
              <div style="display:flex;gap:8px;">
                <button class="btn-farm" onclick="showTab('wkr-submit', document.querySelector('[onclick*=wkr-submit]'))"><i class="fas fa-pen-to-square me-1"></i> Daily Record</button>
                <button class="btn-ghost" onclick="showTab('wkr-weekly', document.querySelector('[onclick*=wkr-weekly]'))"><i class="fas fa-calendar-week me-1"></i> Weekly Record</button>
              </div>
            </div>
          </div>
        </div>
        {% endif %}

        <div class="card">
          <div class="card-header-custom">
            <div class="section-header" style="margin:0;">
              <div class="section-divider"></div>
              <h5><i class="fas fa-clock-rotate-left me-2" style="color:var(--accent);"></i>My Recent Submissions</h5>
            </div>
          </div>
          <div class="card-body-custom">
            <div class="table-responsive">
              <table class="table table-hover align-middle">
                <thead><tr><th>Batch</th><th>Date</th><th>Weight</th><th>Mortality</th><th>Status</th></tr></thead>
                <tbody>
                {% for r in my_records %}
                <tr>
                  <td style="font-weight:700;">{{ r.batch.batch_name if r.batch else '—' }}</td>
                  <td style="font-size:13px;color:var(--muted);">{{ r.record_date.strftime('%b %d, %Y') if r.record_date else '—' }}</td>
                  <td>{{ r.avg_weight_g }} g</td>
                  <td>{{ r.mortality }}</td>
                  <td>
                    {% if r.status == 'Verified' %}
                    <span class="status-pill status-paid"><i class="fas fa-check me-1"></i>Verified</span>
                    {% elif r.status == 'Rejected' %}
                    <span class="status-pill" style="background:#fee2e2;color:#991b1b;" title="{{ r.review_notes or '' }}"><i class="fas fa-xmark me-1"></i>Rejected</span>
                    {% else %}
                    <span class="status-pill status-pending"><i class="fas fa-hourglass-half me-1"></i>Pending</span>
                    {% endif %}
                  </td>
                </tr>
                {% else %}
                <tr><td colspan="5" class="text-center py-4" style="color:var(--muted);">No submissions yet.</td></tr>
                {% endfor %}
                </tbody>
              </table>
            </div>
          </div>
        </div>
    </div>

    <!-- ==================== SUBMIT DAILY RECORD ==================== -->
    <div id="wkr-submit" class="tab-content">
      <div class="card">
        <div class="card-header-custom">
          <div class="section-header" style="margin:0;">
            <div class="section-divider"></div>
            <h5><i class="fas fa-pen-to-square me-2" style="color:var(--accent);"></i>Submit Daily Record</h5>
          </div>
        </div>
        <div class="card-body-custom">
          {% if active_batch %}
          <div class="alert" style="background:#f0fdf4;color:#166534;border:1px solid #bbf7d0;font-size:13px;border-radius:10px;padding:10px 14px;margin-bottom:16px;">
            <i class="fas fa-info-circle me-1"></i>Recording for <strong>{{ active_batch.batch_name }}</strong>
          </div>
          <form id="workerRecordForm" method="post" action="/worker/record/add" onsubmit="return confirmRecordSubmit(event)">
            <div class="row g-3">

              <!-- Flock Batch (Automatic) -->
              <div class="col-md-6">
                <label class="form-label">Flock Batch <span style="color:var(--muted);font-weight:400;text-transform:none;">(automatic)</span></label>
                <input type="text" class="form-control autofield" value="{{ active_batch.batch_name }}" readonly>
              </div>

              <!-- Date (Automatic) -->
              <div class="col-md-6">
                <label class="form-label">Date <span style="color:var(--muted);font-weight:400;text-transform:none;">(automatic)</span></label>
                <input type="date" name="record_date" id="wkrDate" class="form-control autofield" value="{{ today_date }}" readonly>
              </div>

              <!-- Day Number (Automatic) -->
              <div class="col-md-4">
                <label class="form-label">Day Number <span style="color:var(--muted);font-weight:400;text-transform:none;">(automatic)</span></label>
                <input type="number" id="dayNumber" class="form-control autofield" value="{{ active_batch.age_days }}" readonly>
              </div>

              <!-- Mortality -->
              <div class="col-md-4">
                <label class="form-label">Mortality <span class="text-danger">*</span></label>
                <input type="number" name="mortality" id="wkrMortality" class="form-control" placeholder="0" value="0" min="0" required>
                <small style="color:var(--muted);">Number of deaths during the day</small>
              </div>

              <!-- Cause of Death -->
              <div class="col-md-4">
                <label class="form-label">Cause of Death</label>
                <input name="cause" id="wkrCause" class="form-control" placeholder="e.g. Heat stress">
              </div>

              <!-- Feed Type -->
              <div class="col-md-6">
                <label class="form-label">Feed Type <span class="text-danger">*</span></label>
                <select name="feed_category" id="wkrFeedCategory" class="form-select" required onchange="filterFeedNames()">
                  <option value="">— Select Feed Type —</option>
                  <option value="Chick Booster">Chick Booster (0–14 days)</option>
                  <option value="Grower Pellets">Grower Pellets (15–28 days)</option>
                  <option value="Finisher Pellets">Finisher Pellets (29+ days)</option>
                </select>
              </div>

              <!-- Feed Name -->
              <div class="col-md-6">
                <label class="form-label">Feed Name <span class="text-danger">*</span></label>
                <select name="feed_record_id" id="wkrFeedName" class="form-select" required>
                  <option value="">— Select Feed Type First —</option>
                </select>
              </div>

              <!-- Number of Feeds per Day (kg) -->
              <div class="col-md-6">
                <label class="form-label">Number of Feeds per Day (kg) <span class="text-danger">*</span></label>
                <input type="number" step="0.1" name="feed_consumed" id="wkrFeedConsumed" class="form-control" placeholder="e.g. 50" required>
                <small style="color:var(--muted);">This automatically reduces the feed inventory</small>
              </div>

              <!-- Average Bird Weight -->
              <div class="col-md-6">
                <label class="form-label">Average Bird Weight (grams) <span class="text-danger">*</span></label>
                <input type="number" step="0.1" name="avg_weight" id="wkrWeight" class="form-control" placeholder="e.g. 850" required>
              </div>

            </div>
            <button type="submit" class="btn-farm mt-4" style="padding:11px 26px;"><i class="fas fa-paper-plane me-2"></i>Submit Daily Record</button>
          </form>
          {% else %}
          <div class="text-center py-5" style="color:var(--muted);">
            <i class="fas fa-layer-group fa-2x mb-3 d-block"></i>
            No active flock batch. Ask your Owner to create one.
          </div>
          {% endif %}
        </div>
      </div>
    </div>

    <!-- ==================== SUBMIT WEEKLY RECORD ==================== -->
    <div id="wkr-weekly" class="tab-content">
      <div class="card">
        <div class="card-header-custom">
          <div class="section-header" style="margin:0;">
            <div class="section-divider"></div>
            <h5><i class="fas fa-calendar-week me-2" style="color:var(--accent);"></i>Submit Weekly Record</h5>
          </div>
        </div>
        <div class="card-body-custom">
          {% if active_batch %}
            {% if can_submit_weekly %}
            <div class="alert" style="background:#f0fdf4;color:#166534;border:1px solid #bbf7d0;font-size:13px;border-radius:10px;padding:10px 14px;margin-bottom:16px;">
              <i class="fas fa-info-circle me-1"></i>Recording weekly weights for <strong>{{ active_batch.batch_name }}</strong> — Week {{ current_week }}
            </div>
            <form method="post" action="/worker/weekly/add">
              <div class="row g-3">
                <div class="col-md-4">
                  <label class="form-label">Week Number <span class="text-danger">*</span></label>
                  <input type="number" name="week_number" class="form-control" value="{{ current_week }}" required>
                </div>
                <div class="col-md-4">
                  <label class="form-label">Total Weight of Sample (g) <span class="text-danger">*</span></label>
                  <input type="number" step="0.1" name="total_weight_sample" id="totalWeightSample" class="form-control" placeholder="e.g. 5000" required>
                  <small class="text-muted">Total weight of 50-100 birds in a basket</small>
                </div>
                <div class="col-md-4">
                  <label class="form-label">Number of Birds Weighed <span class="text-danger">*</span></label>
                  <input type="number" name="total_birds_weighed" id="totalBirdsWeighed" class="form-control" placeholder="e.g. 50" required>
                </div>
              </div>
              <div class="mt-3 p-3" style="background:var(--bg);border-radius:10px;border:1px solid var(--border);">
                <div style="font-size:12px;color:var(--muted);">Average Bird Weight (auto-calculated)</div>
                <div style="font-size:20px;font-weight:800;" id="avgWeightDisplay">— g</div>
              </div>
              <button type="submit" class="btn-farm mt-3" style="padding:11px 26px;"><i class="fas fa-paper-plane me-2"></i>Submit Weekly Record</button>
            </form>
            {% else %}
            <div class="text-center py-5" style="color:var(--muted);">
              <i class="fas fa-clock fa-3x mb-3 d-block"></i>
              <h5 style="font-weight:700;">Weekly record already submitted</h5>
              <p>Next submission available in 7 days.</p>
            </div>
            {% endif %}
          {% else %}
          <div class="text-center py-5" style="color:var(--muted);">
            <i class="fas fa-layer-group fa-2x mb-3 d-block"></i>
            No active flock batch.
          </div>
          {% endif %}
        </div>
      </div>
    </div>

  </div></div></div>

<div class="modal fade" id="submitConfirmModal" tabindex="-1" data-bs-backdrop="static">
  <div class="modal-dialog modal-dialog-centered">
    <div class="modal-content" style="background:var(--card-bg);border:1px solid var(--border);border-radius:16px;">
      <div class="modal-header" style="border-color:var(--border);">
        <h5 class="modal-title" style="font-weight:800;"><i class="fas fa-clipboard-check me-2" style="color:var(--accent);"></i>Confirm Daily Record</h5>
        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
      </div>
      <div class="modal-body">
        <p style="font-size:13px;color:var(--muted);margin-bottom:14px;">
          Please double-check the details below before submitting.
        </p>
        <div style="background:var(--bg);border-radius:10px;padding:14px;border:1px solid var(--border);" id="confirmDetails"></div>
      </div>
      <div class="modal-footer" style="border-color:var(--border);">
        <button type="button" class="btn-ghost" data-bs-dismiss="modal">Go Back & Edit</button>
        <button type="button" class="btn-farm" onclick="reallySubmit()"><i class="fas fa-paper-plane me-1"></i> Confirm Submit</button>
      </div>
    </div>
  </div>
</div>

""" + _BASE_SCRIPT + """
<script>
// ─────────────────────────────────────────────────────────────────────────
// Feed Type → Feed Name cascade for the Worker daily record form
// ─────────────────────────────────────────────────────────────────────────
var allFeedRecords = [
  {% for fr in feed_records %}
  { id: {{ fr.feed_record_id }}, category: "{{ fr.feed_category }}", name: "{{ fr.feed_name }}", remaining: {{ fr.remaining_quantity }} },
  {% endfor %}
];

function filterFeedNames() {
  var category = document.getElementById('wkrFeedCategory').value;
  var feedNameSelect = document.getElementById('wkrFeedName');
  
  feedNameSelect.innerHTML = '<option value="">— Select Feed Name —</option>';
  
  if (!category) {
    feedNameSelect.innerHTML = '<option value="">— Select Feed Type First —</option>';
    return;
  }
  
  var filtered = allFeedRecords.filter(function(f) { return f.category === category; });
  
  if (filtered.length === 0) {
    feedNameSelect.innerHTML = '<option value="">No feeds available for this category</option>';
    return;
  }
  
  filtered.forEach(function(f) {
    var opt = document.createElement('option');
    opt.value = f.id;
    opt.textContent = f.name + ' (' + f.remaining + ' kg available)';
    feedNameSelect.appendChild(opt);
  });
}

function confirmRecordSubmit(event) {
  event.preventDefault();
  const feedCategory = document.getElementById('wkrFeedCategory');
  const feedNameSelect = document.getElementById('wkrFeedName');
  const batchName = "{{ active_batch.batch_name if active_batch else '' }}";
  const feedCategoryText = feedCategory.selectedIndex > 0 ? feedCategory.options[feedCategory.selectedIndex].text.trim() : '(no feed type selected)';
  const feedNameText = feedNameSelect.selectedIndex > 0 ? feedNameSelect.options[feedNameSelect.selectedIndex].text.trim() : '(no feed name selected)';
  const recordDate = document.getElementById('wkrDate').value || '(no date)';
  const mortality = document.getElementById('wkrMortality').value || '0';
  const feedConsumed = document.getElementById('wkrFeedConsumed').value || '0';
  const avgWeight = document.getElementById('wkrWeight').value || '0';
  const cause = document.getElementById('wkrCause').value.trim();
  const dayNum = document.getElementById('dayNumber').value || '0';

  let html = '';
  html += '<div class="confirm-row"><span class="label">Batch</span><span class="value">' + batchName + '</span></div>';
  html += '<div class="confirm-row"><span class="label">Date</span><span class="value">' + recordDate + '</span></div>';
  html += '<div class="confirm-row"><span class="label">Day Number</span><span class="value">Day ' + dayNum + '</span></div>';
  html += '<div class="confirm-row"><span class="label">Mortality</span><span class="value">' + mortality + '</span></div>';
  html += '<div class="confirm-row"><span class="label">Feed Type</span><span class="value">' + feedCategoryText + '</span></div>';
  html += '<div class="confirm-row"><span class="label">Feed Name</span><span class="value">' + feedNameText + '</span></div>';
  html += '<div class="confirm-row"><span class="label">Feed Given</span><span class="value">' + feedConsumed + ' kg</span></div>';
  html += '<div class="confirm-row"><span class="label">Avg Bird Weight</span><span class="value">' + avgWeight + ' g</span></div>';
  if (cause) html += '<div class="confirm-row"><span class="label">Cause</span><span class="value">' + cause + '</span></div>';

  document.getElementById('confirmDetails').innerHTML = html;
  var modal = new bootstrap.Modal(document.getElementById('submitConfirmModal'));
  modal.show();
  return false;
}

function reallySubmit() {
  document.getElementById('workerRecordForm').submit();
}

// Weekly record average calculation
document.addEventListener('DOMContentLoaded', function() {
  var tw = document.getElementById('totalWeightSample');
  var tb = document.getElementById('totalBirdsWeighed');
  var disp = document.getElementById('avgWeightDisplay');
  if (tw && tb && disp) {
    function calc() {
      var w = parseFloat(tw.value) || 0;
      var b = parseInt(tb.value) || 0;
      var avg = b > 0 ? (w / b).toFixed(2) : 0;
      disp.textContent = avg + ' g';
    }
    tw.addEventListener('input', calc);
    tb.addEventListener('input', calc);
  }
});
</script>
</body></html>
"""

# ─────────────────────────────────────────────────────────────────────────────
# PRINTABLE PERFORMANCE REPORT — REDESIGNED UI
# ─────────────────────────────────────────────────────────────────────────────
TEMPLATE_PERFORMANCE_REPORT_PRINT = """<!doctype html>
<html><head><meta charset="utf-8"><title>Performance Report — FlockIQ</title>
<script src="https://cdn.jsdelivr.net/npm/html2pdf.js@0.10.1/dist/html2pdf.bundle.min.js"></script>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
  * { box-sizing: border-box; }
  body { font-family: 'Inter', Arial, sans-serif; font-size: 13px; color: #1c1917; margin: 0; background: #f4f6f8; }
  
  .report-container { max-width: 900px; margin: 30px auto; background: #fff; border-radius: 16px; box-shadow: 0 10px 40px rgba(0,0,0,0.1); overflow: hidden; }
  
  .report-header { background: linear-gradient(135deg, #166534 0%, #3f6212 100%); color: #fff; padding: 32px 40px; position: relative; overflow: hidden; }
  .report-header::after { content: ''; position: absolute; right: -40px; top: -40px; width: 200px; height: 200px; border-radius: 50%; background: rgba(255,255,255,0.08); }
  .report-header::before { content: ''; position: absolute; right: 80px; bottom: -60px; width: 150px; height: 150px; border-radius: 50%; background: rgba(255,255,255,0.06); }
  
  .header-brand { display: flex; align-items: center; gap: 16px; margin-bottom: 20px; position: relative; z-index: 1; }
  .header-logo { width: 56px; height: 56px; border-radius: 14px; background: rgba(255,255,255,0.15); display: flex; align-items: center; justify-content: center; }
  .header-title { font-size: 26px; font-weight: 800; letter-spacing: -0.5px; margin: 0; }
  .header-subtitle { font-size: 13px; opacity: 0.85; margin-top: 2px; }
  
  .report-title { font-size: 18px; font-weight: 700; letter-spacing: 2px; text-align: center; margin: 0; position: relative; z-index: 1; }
  .report-meta { text-align: center; font-size: 12px; opacity: 0.85; margin-top: 6px; position: relative; z-index: 1; }
  
  .report-body { padding: 36px 40px; }
  
  .section { margin-bottom: 28px; }
  .section-title { display: flex; align-items: center; gap: 10px; margin-bottom: 16px; }
  .section-divider { width: 4px; height: 22px; border-radius: 3px; background: linear-gradient(to bottom, #166534, #15803d); }
  .section-title h3 { font-size: 15px; font-weight: 800; margin: 0; color: #166534; }
  
  .info-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; }
  @media (max-width: 700px) { .info-grid { grid-template-columns: repeat(2, 1fr); } }
  @media (max-width: 500px) { .info-grid { grid-template-columns: 1fr; } }
  
  .info-card { background: #f8fafc; border: 1px solid #e5e7eb; border-radius: 10px; padding: 14px 16px; }
  .info-card .label { font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; color: #6b7280; margin-bottom: 4px; }
  .info-card .value { font-size: 16px; font-weight: 800; color: #1c1917; }
  .info-card .value.green { color: #15803d; }
  .info-card .value.red { color: #dc2626; }
  .info-card .value.blue { color: #0ea5e9; }
  .info-card .value.orange { color: #d97706; }
  
  .highlight-card { background: linear-gradient(135deg, #f0fdf4, #dcfce7); border-color: #bbf7d0; }
  .highlight-card .value { color: #166534; font-size: 20px; }
  
  .data-table { width: 100%; border-collapse: collapse; margin-top: 8px; }
  .data-table th { background: #f1f5f9; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; color: #6b7280; padding: 10px 14px; text-align: left; border-bottom: 2px solid #e5e7eb; }
  .data-table td { padding: 10px 14px; border-bottom: 1px solid #f1f5f9; font-size: 13px; }
  .data-table tr:last-child td { border-bottom: none; }
  .data-table tr:hover { background: #f8fafc; }
  .data-table .amount { text-align: right; font-weight: 700; }
  .data-table .pct { text-align: right; color: #6b7280; }
  .data-table tfoot th { background: #f0fdf4; color: #166534; font-weight: 800; }
  
  .remarks-box { background: #fffbeb; border: 1px solid #fde68a; border-radius: 10px; padding: 14px 18px; font-size: 13px; color: #92400e; margin-top: 16px; }
  .remarks-box i { margin-right: 6px; }
  
  .signature-section { margin-top: 50px; display: flex; justify-content: space-between; align-items: flex-end; }
  .signature-box { text-align: center; }
  .signature-line { width: 220px; border-bottom: 1px solid #1c1917; margin-bottom: 6px; }
  .signature-label { font-size: 12px; color: #6b7280; }
  
  .report-footer { background: #f8fafc; padding: 16px 40px; text-align: center; font-size: 11px; color: #9ca3af; border-top: 1px solid #e5e7eb; }
  
  .no-print { position: fixed; top: 20px; right: 20px; display: flex; gap: 10px; z-index: 1000; }
  .no-print button { padding: 10px 20px; font-weight: 700; font-size: 13px; cursor: pointer; border: none; border-radius: 10px; display: flex; align-items: center; gap: 8px; transition: all 0.15s; }
  .btn-print { background: linear-gradient(135deg, #166534, #15803d); color: #fff; box-shadow: 0 4px 12px rgba(22,101,52,0.3); }
  .btn-print:hover { opacity: 0.9; }
  .btn-pdf { background: #fff; color: #1c1917; border: 1px solid #e5e7eb; box-shadow: 0 4px 12px rgba(0,0,0,0.08); }
  .btn-pdf:hover { background: #f8fafc; }
  
  @media print {
    body { background: #fff; margin: 0; }
    .no-print { display: none !important; }
    .report-container { margin: 0; box-shadow: none; border-radius: 0; max-width: 100%; }
    .report-header { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
    .info-card { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
    .data-table th { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
  }
  
  @page { margin: 0.5in; size: letter; }
</style></head>
<body>

<div class="no-print">
  <button class="btn-print" onclick="window.print()">🖨️ Print Report</button>
  <button class="btn-pdf" onclick="saveReportPdf()">📄 Save PDF</button>
</div>

<div class="report-container" id="reportContent">
  <div class="report-header">
    <div class="header-brand">
      <div class="header-logo">
        <svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg" width="36" height="36">
          <ellipse cx="50" cy="66" rx="34" ry="28" fill="#FFCF3F"/>
          <circle cx="50" cy="34" r="23" fill="#FFDD5C"/>
          <path d="M50 34 L74 39 L50 46 Z" fill="#FF8A3D"/>
          <circle cx="43" cy="29" r="4" fill="#2B2118"/>
          <circle cx="57" cy="29" r="4" fill="#2B2118"/>
          <path d="M18 16 Q28 6 37 18 Q27 20 18 16 Z" fill="#FFB03F"/>
          <path d="M63 18 Q72 6 82 16 Q73 20 63 18 Z" fill="#FFB03F"/>
        </svg>
      </div>
      <div>
        <h1 class="header-title">AGRADECIDO CORP.</h1>
        <div class="header-subtitle">Unit 204 A7 Bldg Floro Subd., Zigzag Hills, Malhacan, Meycauayan City Bulacan</div>
      </div>
    </div>
    <h2 class="report-title">PERFORMANCE REPORT</h2>
    <div class="report-meta">
      {% if report.batch %}{{ report.batch.batch_name }}{% endif %}
      {% if report.end_date %} · Harvested {{ report.end_date }}{% endif %}
    </div>
  </div>

  <div class="report-body">
    <!-- Batch Overview -->
    <div class="section">
      <div class="section-title">
        <div class="section-divider"></div>
        <h3>Batch Overview</h3>
      </div>
      <div class="info-grid">
        {% if 'batch_name' in selected_fields %}
        <div class="info-card">
          <div class="label">Batch Name</div>
          <div class="value">{{ report.batch.batch_name if report.batch else '—' }}</div>
        </div>
        {% endif %}
        {% if 'age' in selected_fields %}
        <div class="info-card">
          <div class="label">Age</div>
          <div class="value">{{ report.age or '—' }} days</div>
        </div>
        {% endif %}
        {% if 'season' in selected_fields %}
        <div class="info-card">
          <div class="label">Season of Harvest</div>
          <div class="value">{{ report.season or '—' }}</div>
        </div>
        {% endif %}
        {% if 'start_date' in selected_fields %}
        <div class="info-card">
          <div class="label">Start Date</div>
          <div class="value">{{ report.batch.start_date.strftime('%b %d, %Y') if report.batch and report.batch.start_date else '—' }}</div>
        </div>
        {% endif %}
        {% if 'harvest_date' in selected_fields %}
        <div class="info-card">
          <div class="label">Harvest Date</div>
          <div class="value">{{ report.end_date or '—' }}</div>
        </div>
        {% endif %}
        {% if 'price_basis' in selected_fields %}
        <div class="info-card">
          <div class="label">Price Basis Used</div>
          <div class="value">{{ report.price_basis or 'DA' }} — ₱{{ "%.2f"|format(report.price_basis_value or 0) }}/kg</div>
        </div>
        {% endif %}
      </div>
    </div>

    <!-- Production Metrics -->
    <div class="section">
      <div class="section-title">
        <div class="section-divider"></div>
        <h3>Production Metrics</h3>
      </div>
      <div class="info-grid">
        {% if 'initial_count' in selected_fields %}
        <div class="info-card">
          <div class="label">Initial Count</div>
          <div class="value">{{ "{:,}".format(report.initial_count or 0) }}</div>
        </div>
        {% endif %}
        {% if 'harvest_count' in selected_fields %}
        <div class="info-card">
          <div class="label">Harvest Count</div>
          <div class="value">{{ "{:,}".format(report.harvest_count or 0) }}</div>
        </div>
        {% endif %}
        {% if 'mortality_pct' in selected_fields %}
        <div class="info-card">
          <div class="label">Mortality Rate</div>
          <div class="value red">{{ report.mortality_pct or '—' }}%</div>
        </div>
        {% endif %}
        {% if 'lw' in selected_fields %}
        <div class="info-card">
          <div class="label">Live Weight</div>
          <div class="value blue">{{ report.lw or '—' }} g</div>
        </div>
        {% endif %}
        {% if 'adg' in selected_fields %}
        <div class="info-card">
          <div class="label">ADG (Avg Daily Gain)</div>
          <div class="value green">{{ report.adg or '—' }} g/batch</div>
        </div>
        {% endif %}
        {% if 'fcr' in selected_fields %}
        <div class="info-card">
          <div class="label">FCR (Feed Conversion)</div>
          <div class="value orange">{{ report.fcr or '—' }}</div>
        </div>
        {% endif %}
      </div>
    </div>

    <!-- Feed & Vaccination Details -->
    {% if 'chick_booster' in selected_fields or 'grower_pellets' in selected_fields or 'finisher_pellets' in selected_fields or 'vaccine_day_12' in selected_fields or 'vaccine_day_16' in selected_fields or 'medicines' in selected_fields %}
    <div class="section">
      <div class="section-title">
        <div class="section-divider"></div>
        <h3>Feed & Health Management</h3>
      </div>
      <div class="info-grid">
        {% if 'chick_booster' in selected_fields %}
        <div class="info-card">
          <div class="label">Chick Booster</div>
          <div class="value">{{ report.chick_booster or '—' }}</div>
        </div>
        {% endif %}
        {% if 'grower_pellets' in selected_fields %}
        <div class="info-card">
          <div class="label">Grower Pellets</div>
          <div class="value">{{ report.grower_pellets or '—' }}</div>
        </div>
        {% endif %}
        {% if 'finisher_pellets' in selected_fields %}
        <div class="info-card">
          <div class="label">Finisher Pellets</div>
          <div class="value">{{ report.finisher_pellets or '—' }}</div>
        </div>
        {% endif %}
        {% if 'vaccine_day_12' in selected_fields %}
        <div class="info-card">
          <div class="label">Vaccine Day 12</div>
          <div class="value">{{ report.vaccine_day_12 or '—' }}</div>
        </div>
        {% endif %}
        {% if 'vaccine_day_16' in selected_fields %}
        <div class="info-card">
          <div class="label">Vaccine Day 16</div>
          <div class="value">{{ report.vaccine_day_16 or '—' }}</div>
        </div>
        {% endif %}
        {% if 'medicines' in selected_fields %}
        <div class="info-card">
          <div class="label">Medicines Administered</div>
          <div class="value">{{ report.medicines or '—' }}</div>
        </div>
        {% endif %}
      </div>
    </div>
    {% endif %}

    <!-- Financial Summary -->
    {% if 'expenses' in selected_fields or 'loss_gain' in selected_fields %}
    <div class="section">
      <div class="section-title">
        <div class="section-divider"></div>
        <h3>Financial Summary</h3>
      </div>
      <div class="info-grid">
        {% if 'expenses' in selected_fields %}
        <div class="info-card">
          <div class="label">Total Expenses</div>
          <div class="value">₱{{ "{:,.2f}".format(report.expenses) if report.expenses else '—' }}</div>
        </div>
        {% endif %}
        {% if 'loss_gain' in selected_fields %}
        <div class="info-card highlight-card">
          <div class="label">Net {{ 'Profit' if report.loss_gain and report.loss_gain >= 0 else 'Loss' }}</div>
          <div class="value" style="color:{{ '#166534' if report.loss_gain and report.loss_gain >= 0 else '#dc2626' }};">
            {{ '+' if report.loss_gain and report.loss_gain >= 0 else '' }}₱{{ "{:,.2f}".format(report.loss_gain) if report.loss_gain is not none else '—' }}
          </div>
        </div>
        {% endif %}
      </div>
    </div>
    {% endif %}

    <!-- Expense Breakdown -->
    {% if 'expense_types' in selected_fields and report.expense_types %}
    <div class="section">
      <div class="section-title">
        <div class="section-divider"></div>
        <h3>Expense Breakdown by Category</h3>
      </div>
      <table class="data-table">
        <thead>
          <tr>
            <th>Expense Category</th>
            <th style="text-align:right;">Amount</th>
            <th style="text-align:right;">% of Total</th>
          </tr>
        </thead>
        <tbody>
          {% for e in report.expense_types %}
          <tr>
            <td>{{ e.type }}</td>
            <td class="amount">₱{{ "{:,.2f}".format(e.amount) }}</td>
            <td class="pct">{{ e.pct }}%</td>
          </tr>
          {% endfor %}
        </tbody>
        <tfoot>
          <tr>
            <th>Total</th>
            <th class="amount">₱{{ "{:,.2f}".format(report.expense_types_total) }}</th>
            <th class="pct">100%</th>
          </tr>
        </tfoot>
      </table>
    </div>
    {% endif %}

    <!-- Remarks -->
    {% if 'remarks' in selected_fields and report.remarks %}
    <div class="remarks-box">
      <i>💬</i><strong>Remarks:</strong> {{ report.remarks }}
    </div>
    {% endif %}

    <!-- Signature -->
    <div class="signature-section">
      <div class="signature-box">
        <div class="signature-line"></div>
        <div class="signature-label">Farm Head / Manager</div>
      </div>
      <div class="signature-box">
        <div class="signature-line"></div>
        <div class="signature-label">Date</div>
      </div>
    </div>
  </div>

  <div class="report-footer">
    Generated by FlockIQ Poultry Farm Management System · {{ report.end_date or '' }}
  </div>
</div>

<script>
function saveReportPdf() {
  var batchName = "{{ (report.batch.batch_name if report.batch else 'report') | replace(' ', '_') }}";
  var opt = {
    margin: 0,
    filename: 'Performance_Report_' + batchName + '.pdf',
    image: { type: 'jpeg', quality: 0.98 },
    html2canvas: { scale: 2, useCORS: true },
    jsPDF: { unit: 'in', format: 'letter', orientation: 'portrait' }
  };
  html2pdf().set(opt).from(document.getElementById('reportContent')).save();
}
</script>
</body></html>
"""

# ─────────────────────────────────────────────────────────────────────────────
# EXPENSE HISTORY PAGE
# ─────────────────────────────────────────────────────────────────────────────
TEMPLATE_EXPENSE_HISTORY = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Past Batch Expenses</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap" rel="stylesheet">
<style>
  body{font-family:'Inter',sans-serif;background:#f4f6f8;color:#1f2937;}
  .wrap{max-width:1000px;margin:28px auto;padding:0 16px;}
  .cardx{background:#fff;border:1px solid #e5e7eb;border-radius:14px;padding:18px;margin-bottom:18px;}
  .kpi{background:#f8fafc;border:1px solid #e5e7eb;border-radius:10px;padding:10px 14px;}
  .kpi .l{font-size:11px;text-transform:uppercase;letter-spacing:.03em;color:#6b7280;}
  .kpi .v{font-size:18px;font-weight:800;}
  .pill{font-size:12px;font-weight:700;padding:2px 10px;border-radius:99px;}
  .paid{background:#dcfce7;color:#15803d;} .pending{background:#fef3c7;color:#b45309;}
</style></head>
<body><div class="wrap">
  <div class="d-flex align-items-center justify-content-between mb-3">
    <h4 style="font-weight:800;margin:0;"><i class="fas fa-clock-rotate-left me-2"></i>Past Batch Expenses</h4>
    <a href="{{ back_url }}" class="btn btn-outline-secondary btn-sm"><i class="fas fa-arrow-left me-1"></i> Back to dashboard</a>
  </div>

  {% if not batches %}
  <div class="cardx text-center" style="color:#6b7280;">No past batches yet. A batch appears here once a new one has started.</div>
  {% else %}
  <form method="get" class="cardx d-flex flex-wrap align-items-end gap-2">
    <div><label class="form-label mb-1" style="font-size:12px;font-weight:600;">Batch</label>
      <select name="batch_id" class="form-select" onchange="this.form.submit()" style="min-width:260px;">
        {% for b in batches %}<option value="{{ b.batch_id }}" {% if selected and b.batch_id == selected.batch_id %}selected{% endif %}>{{ b.batch_name }} - {{ b.start_date.strftime('%b %d, %Y') if b.start_date else '' }} ({{ b.flock_status }})</option>{% endfor %}
      </select></div>
    <noscript><button class="btn btn-primary">View</button></noscript>
  </form>

  {% if summary %}
  <div class="cardx">
    <div class="row g-2 mb-3">
      <div class="col-6 col-md-3"><div class="kpi"><div class="l">Total Expenses</div><div class="v">₱{{ "{:,.2f}".format(summary.total) }}</div></div></div>
      <div class="col-6 col-md-3"><div class="kpi"><div class="l">Cost / Bird</div><div class="v">{{ "₱%.2f"|format(summary.cost_per_bird) if summary.cost_per_bird is not none else '—' }}</div></div></div>
      <div class="col-6 col-md-3"><div class="kpi"><div class="l">Cost / Chick</div><div class="v">{{ "₱%.2f"|format(summary.cost_per_chick) if summary.cost_per_chick is not none else '—' }}</div></div></div>
      <div class="col-6 col-md-3"><div class="kpi"><div class="l">Cost / kg Live</div><div class="v">{{ "₱%.2f"|format(summary.cost_per_kg_live) if summary.cost_per_kg_live is not none else '—' }}</div></div></div>
    </div>
    <div class="row g-2">
      {% for label, key in [("Chicks","chicks"),("Feed","feed"),("Vaccine","vaccine"),("Water","water"),("Electricity","electricity"),("LPG","lpg"),("Labor","labor"),("Other","other")] %}
      <div class="col-6 col-md-3"><div class="kpi"><div class="l">{{ label }}</div><div class="v" style="font-size:15px;">₱{{ "{:,.2f}".format(summary.parts[key]) }}</div></div></div>
      {% endfor %}
    </div>
  </div>
  {% endif %}

  <div class="cardx">
    <h6 style="font-weight:800;">All expense entries</h6>
    <div class="table-responsive">
    <table class="table table-hover align-middle mb-0">
      <thead><tr><th>Date</th><th>Type</th><th>Description</th><th class="text-end">Amount</th><th>Status</th></tr></thead>
      <tbody>
      {% for r in rows %}
      <tr><td style="font-size:13px;color:#6b7280;">{{ r.date.strftime('%b %d, %Y') if r.date else '—' }}</td>
          <td style="font-weight:600;">{{ r.type }}</td><td style="font-size:13px;">{{ r.desc or '—' }}</td>
          <td class="text-end" style="font-weight:700;">₱{{ "{:,.2f}".format(r.amount) }}</td>
          <td><span class="pill {{ 'paid' if r.status == 'Paid' else 'pending' }}">{{ r.status or '—' }}</span></td></tr>
      {% else %}<tr><td colspan="5" class="text-center py-3" style="color:#6b7280;">No expenses recorded for this batch.</td></tr>{% endfor %}
      </tbody>
    </table>
    </div>
  </div>
  {% endif %}
</div></body></html>
"""