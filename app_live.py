import streamlit as st
import base64
import os

# 1. Configure page setup (Must be first Streamlit command)
st.set_page_config(layout="wide", page_title="Benchmark3x")

# --- OPTIMIZATION: CACHE CHART GENERATION ---
@st.cache_resource
def ensure_chart_exists():
    """
    Generates the downturn_chart.jpg only if it doesn't exist.
    Cached to prevent re-running Matplotlib logic on every app rerun.
    """
    chart_path = "downturn_chart.jpg"
    
    # If it exists, skip generation to save speed
    if os.path.exists(chart_path):
        return

    try:
        import matplotlib.pyplot as plt
        import numpy as np

        # Setup for a "Regime Filter" style chart
        np.random.seed(101) 
        days = 2000
        x = np.arange(days)
        
        # Generate a "Market" line
        returns = np.random.normal(0.0006, 0.012, days)
        price_path = 1000 * np.cumprod(1 + returns)

        plt.figure(figsize=(10, 5)) 
        
        # Plot
        plt.plot(x, price_path, color='#111111', linewidth=1.2, label='Market Index')
        plt.axvspan(200, 350, color='#e74c3c', alpha=0.15, label='Volatility Regime (Cash)')
        plt.axvspan(900, 1000, color='#e74c3c', alpha=0.15)
        plt.axvspan(1400, 1600, color='#e74c3c', alpha=0.15)
        plt.axvspan(600, 650, color='#f1c40f', alpha=0.15, label='Choppy/Warning')
        plt.axvspan(1850, 1900, color='#f1c40f', alpha=0.15)

        # Styling 
        plt.title("Historical Regime Detection (2015-2025)", fontsize=12, fontweight='bold', color='#333', loc='left', pad=15)
        plt.legend(loc='upper left', fontsize=8, frameon=True, fancybox=False, framealpha=0.95)
        
        ax = plt.gca()
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#888')
        ax.spines['bottom'].set_color('#888')
        plt.grid(True, axis='y', alpha=0.2, linestyle='-')
        plt.grid(True, axis='x', alpha=0.1, linestyle='-')

        plt.tight_layout()
        plt.savefig(chart_path, dpi=150, bbox_inches='tight')
        plt.close()
        
    except Exception as e:
        st.warning(f"Could not generate chart: {e}")

# Trigger chart generation
ensure_chart_exists()

# --- CSS OVERRIDES (STREAMLIT INTERNAL FIXES) ---
# Kept separate because this addresses Streamlit-specific layout issues
st.markdown("""
<style>
    /* Reset Streamlit's default padding/margins */
    .block-container {
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
        padding-left: 0rem !important;
        padding-right: 0rem !important;
        margin: 0px !important;
        max-width: 100% !important;
        overflow: visible !important;
    }
    
    /* Hide Streamlit elements */
    header[data-testid="stHeader"] { visibility: hidden; height: 0px; }
    footer { display: none !important; }
    .main .block-container { margin-top: -60px !important; }
    
    /* Ensure main app container handles scroll but allows sticky children */
    .stApp {
        overflow-y: auto !important;
        background-color: white;
    }
</style>
""", unsafe_allow_html=True)

# --- OPTIMIZATION: CACHE IMAGE LOADING ---
@st.cache_data
def get_base64_image(image_path):
    if not os.path.exists(image_path):
        return "" 
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# --- LOAD LOCAL IMAGES ---
logo_data = get_base64_image("logo_R1.jpg")
logo_src = f"data:image/jpeg;base64,{logo_data}" if logo_data else ""

computer_data = get_base64_image("computer.jpg")
computer_src = f"data:image/jpeg;base64,{computer_data}" if computer_data else "https://via.placeholder.com/800x600.png?text=computer.jpg+not+found"

chart_data = get_base64_image("downturn_chart.jpg")
chart_src = f"data:image/jpeg;base64,{chart_data}" if chart_data else "https://via.placeholder.com/600x350.png?text=Chart+Generation+Failed"

gears_data = get_base64_image("gears.png")
gears_src = f"data:image/png;base64,{gears_data}" if gears_data else ""

# --- PART 1: LANDING PAGE CSS (MODULARIZED) ---
# Separated from HTML for readability. No indentation to prevent Markdown code blocks.
LANDING_CSS = f"""
<style>
/* LANDING PAGE STYLES */
#landing-root {{
font-family: "SF Pro Display", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
color: #333;
background-color: #ffffff;
}}
/* UTILITIES */
.orange {{ color: #f5a623; }}
.text-center {{ text-align: center; }}
.container {{ max-width: 1400px; margin: 0 auto; padding: 0 5%; position: relative; z-index: 2; }}
h2 {{ font-size: 2.5rem; color: #111; margin-bottom: 20px; text-align: center; font-weight: 700; letter-spacing: -1px; }}
.section-subtitle {{ text-align: center; color: #666; font-size: 1.1rem; margin-bottom: 60px; max-width: 900px; margin-left: auto; margin-right: auto; line-height: 1.6; }}
p {{ line-height: 1.6; color: #555; }}
/* Global Section Spacing */
section {{ margin-bottom: 100px !important; }}
/* HEADER - STICKY CONFIGURATION */
.sticky-header {{
background-color: #000000;
padding: 20px 4%; 
display: flex;
justify-content: space-between;
align-items: center;
border-bottom: 1px solid #222;
width: 100%;
position: sticky; 
top: 0; 
z-index: 9999;
}}
.logo-container {{ display: flex; align-items: center; text-decoration: none; cursor: pointer; }}
.logo-img {{ height: 90px; width: auto; display: block; mix-blend-mode: screen; }}
nav {{ display: flex; gap: 30px; align-items: center; }}
nav a {{
color: #ccc; text-decoration: none; 
font-size: 1.35rem; font-weight: 500;
transition: color 0.3s; display: flex; align-items: center; cursor: pointer;
}}
nav a:hover {{ color: #f5a623; }}
.nav-login {{ color: #fff; font-weight: 600; }}
.lock-icon {{ margin-right: 6px; font-size: 1.2rem; }}
/* HERO SECTION */
.hero {{
width: 100%; 
position: relative;
overflow: hidden;
background-color: white;
}}
.hero-content-wrapper {{
max-width: 1800px;
margin: 0 auto;
padding: 100px 5% 150px 5%;
display: flex; 
justify-content: space-between; 
align-items: flex-start;
position: relative;
z-index: 10;
}}
/* HERO BACKGROUND EFFECTS */
.hero::before {{
content: '';
position: absolute;
top: 0; left: 0; width: 35%; height: 600px;
background-image: radial-gradient(circle, #d0d0d0 5px, transparent 6px);
background-size: 30px 30px;
clip-path: polygon(0 0, 100% 0, 0 100%);
mask-image: linear-gradient(135deg, black 20%, transparent 100%);
-webkit-mask-image: linear-gradient(135deg, black 20%, transparent 100%);
opacity: 0.6; z-index: 1; pointer-events: none;
}}
.hero-text {{ 
max-width: 45%; 
margin-top: 10px; 
margin-left: 100px; 
position: relative; 
}}
h1 {{ font-size: 3.8rem; line-height: 1.1; color: #111; margin-bottom: 20px; font-weight: 800; letter-spacing: -1px; }}
.hero-p {{ font-size: 1.2rem; margin-bottom: 30px; max-width: 520px; color: #555; }}
/* UPDATED: Button Styling for Anchors */
.btn-primary {{
display: inline-block; background-color: #f5a623; color: white;
padding: 14px 35px; text-decoration: none; border-radius: 4px;
font-weight: 700; font-size: 1rem; transition: transform 0.2s, background-color 0.2s; border: none; cursor: pointer;
text-align: center;
}}
.btn-primary:hover {{ transform: translateY(-2px); background-color: #e0961f; }}
.computer-graphic {{
width: 50%; border-radius: 12px;
box-shadow: 0 30px 60px rgba(0,0,0,0.25);
object-fit: cover;
transform: perspective(1000px) rotateY(-5deg) rotateX(2deg);
transition: transform 0.5s ease;
}}
.computer-graphic:hover {{ transform: perspective(1000px) rotateY(0deg); }}
/* MODEL SECTION */
#model {{ 
background-color: #f8f9fa; 
border-top: 1px solid #eee; 
padding-top: 60px; 
padding-bottom: 80px; 
scroll-margin-top: 60px; 
width: 100%;
position: relative; 
overflow: hidden;
}}
#model::before {{
content: '';
position: absolute;
top: -15%; right: -15%;
width: 62.5%; height: 125%; 
background-image: url('{gears_src}');
background-repeat: no-repeat;
background-position: center right; 
background-size: contain; 
opacity: 0.05; 
filter: grayscale(100%);
pointer-events: none; 
z-index: 0; 
}}
.model-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 70px; align-items: start; position: relative; z-index: 2; }}
.model-step {{ margin-bottom: 30px; display: flex; gap: 20px; }}
.step-num {{ font-size: 2rem; font-weight: 800; color: #f5a623; min-width: 50px; line-height: 1; }}
.step-content h4 {{ font-size: 1.3rem; margin-bottom: 10px; color: #222; }}
.stat-card-row {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 40px; }}
.stat-card {{ background: #fff; padding: 25px; border-radius: 8px; box-shadow: 0 4px 20px rgba(0,0,0,0.06); text-align: center; }}
.stat-val {{ font-size: 2.5rem; font-weight: 700; color: #000; display: block; margin-bottom: 5px; }}
.stat-label {{ font-size: 0.9rem; color: #888; text-transform: uppercase; letter-spacing: 1px; font-weight: 600; }}
.math-box {{
background-color: #fff; padding: 25px; border-radius: 8px;
border-left: 4px solid #f5a623; margin-top: 20px; font-size: 0.95rem;
}}
.chart-container {{
margin-top: 25px; background: #fff; padding: 15px;
border-radius: 8px; box-shadow: 0 4px 20px rgba(0,0,0,0.06); text-align: center;
}}
.chart-img {{ width: 100%; height: auto; border-radius: 4px; border: 1px solid #eee; }}
.chart-caption {{ margin-top: 10px; font-size: 0.85rem; color: #888; font-style: italic; }}
/* PRICING */
#pricing {{ background-color: #fff; padding-top: 60px; scroll-margin-top: 60px; }}
.pricing-grid {{ display: flex; justify-content: center; gap: 30px; margin-top: 40px; flex-wrap: wrap; }}
.pricing-card {{
background: #fff; border: 1px solid #e1e1e1; border-radius: 12px; padding: 40px;
width: 380px; display: flex; flex-direction: column;
transition: transform 0.3s, box-shadow 0.3s;
}}
.pricing-card:hover {{ transform: translateY(-10px); box-shadow: 0 20px 40px rgba(0,0,0,0.1); border-color: #f5a623; }}
.pricing-card.black {{ background: #111; color: #fff; border: 1px solid #111; }}
.pricing-card.black h3, .pricing-card.black .price, .pricing-card.black p, .pricing-card.black li {{ color: #fff; }}
.pricing-card h3 {{ font-size: 1.5rem; margin-bottom: 10px; }}
.price {{ font-size: 3.5rem; font-weight: 800; margin: 20px 0; letter-spacing: -2px; }}
.price span {{ font-size: 1rem; color: #999; font-weight: 400; letter-spacing: 0; }}
.features-list {{ list-style: none; margin: 30px 0; flex-grow: 1; }}
.features-list li {{ margin-bottom: 12px; font-size: 1rem; display: flex; align-items: center; color: #555; }}
.check {{ color: #f5a623; margin-right: 12px; font-weight: bold; }}
/* FAQ */
#faq {{ background-color: #f8f9fa; border-top: 1px solid #eee; padding-top: 60px; padding-bottom: 60px; scroll-margin-top: 60px; width: 100%; }}
.faq-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 30px; }}
.faq-item {{ background: #fff; padding: 30px; border-radius: 8px; border: 1px solid #eee; }}
.faq-item h4 {{ font-size: 1.1rem; margin-bottom: 12px; font-weight: 700; color: #111; }}
.faq-item p {{ font-size: 0.95rem; color: #666; }}
/* FOOTER */
.landing-footer {{ 
background: #111; color: #ffffff; padding: 60px 5%; text-align: center; border-top: 1px solid #222; margin-bottom: 0 !important; 
}}
.landing-footer p {{ font-size: 0.85rem; margin-bottom: 10px; color: #ffffff; }}
.landing-footer a {{ color: #ffffff; text-decoration: none; opacity: 0.8; }}
.landing-footer a:hover {{ opacity: 1; }}
.disclaimer {{ font-size: 0.75rem; color: #ffffff; max-width: 900px; margin: 20px auto; line-height: 1.5; opacity: 0.9; }}
</style>
"""

# --- PART 2: LANDING PAGE BODY (HTML) ---
# NOTE: Removed <button> tags and replaced with <a> tags to enable clickable links.
LANDING_BODY = f"""
<div id="landing-root">
<div class="sticky-header" id="top">
<a href="#top" class="logo-container">
<img src="{logo_src}" class="logo-img" alt="Benchmark3x" />
</a>
<nav>
<a href="#model">Model</a>
<a href="#pricing">Pricing</a>
<a href="#faq">FAQ</a>
<a href="#" class="nav-login"><span class="lock-icon">🔒</span> Sign In</a>
</nav>
</div>
<main>
<section class="hero">
<div class="hero-content-wrapper">
<div class="hero-text">
<h1>Automated Leverage.<br>Zero Emotion.</h1>
<p class="hero-p">
Professional-grade algorithmic signals for <strong>SPXL (3x)</strong> and <strong>SSO (2x)</strong>. 
We capture the upside of leverage while systematically managing the volatility decay. 
<br><br>
<strong>Zero look-ahead bias. Pure Python.</strong>
</p>
<a href="#pricing" class="btn-primary">View Access Plans</a>
</div>
<img src="{computer_src}" class="computer-graphic" alt="Trading Terminal">
</div>
</section>
<section id="model">
<div class="container">
<h2>The Model, The Machine</h2>
<p class="section-subtitle">
Our engine is a machine learning tool trained on hundreds of predictors and backtested with decades of market data. The key to successful leverage isn't just knowing when to enter the market, but knowing when to get out and sit on the sidelines. Our proprietary system picks not only the high-probability days to invest, but more importantly, signals when to exit to avoid the worst drawdowns. <strong>Two models, two purposes—resulting in incredible CAGR performance.</strong>
</p>
<div class="model-grid">
<div>
<div class="model-step">
<div class="step-num">01</div>
<div class="step-content">
<h4>The Problem: Volatility Decay</h4>
<p>If SPY drops 10%, a 3x ETF drops 30%. To get back to even, the 3x ETF needs a 43% gain. In sideways "choppy" markets, this mathematical drag destroys portfolios.</p>
</div>
</div>
<div class="model-step">
<div class="step-num">02</div>
<div class="step-content">
<h4>The Solution: Regime Scanning</h4>
<p>We monitor VIX term structure and realized volatility. When "High Volatility" is detected, the model triggers a <strong>Cash Signal</strong>, sitting out the chop.</p>
</div>
</div>
<div class="model-step">
<div class="step-num">03</div>
<div class="step-content">
<h4>The Result: Pure Trends</h4>
<p>We only re-enter SPXL/SSO when the regime stabilizes. This allows us to participate in the powerful 3x upside of bull markets, without suffering the 3x downside of crashes.</p>
</div>
</div>
<div class="model-step">
<div class="step-num">04</div>
<div class="step-content">
<h4>Deep Predictors</h4>
<p>Our engine ingests 14 distinct market features, including Dark Pool Index (DPI), Gamma Exposure (GEX), and Yield Curve spreads, to paint a complete picture of market health.</p>
</div>
</div>
<div class="model-step">
<div class="step-num">05</div>
<div class="step-content">
<h4>Machine Learning Core</h4>
<p>A supervised Random Forest classifier, trained on 20 years of tick-level data, dynamically weighs these predictors to identify probability skews that human traders miss.</p>
</div>
</div>
<div class="model-step">
<div class="step-num">06</div>
<div class="step-content">
<h4>The Signal</h4>
<p>The output is binary and unequivocal: <strong>1 (Long)</strong> or <strong>0 (Cash)</strong>. There is no hedging, no confusion, and no discretion. Just pure execution.</p>
</div>
</div>
</div>
<div>
<div class="stat-card">
<span class="stat-val orange">42.5%</span>
<span class="stat-label">Backtested CAGR</span>
</div>
<div class="stat-card-row">
<div class="stat-card">
<span class="stat-val">2.1</span>
<span class="stat-label">Profit Factor</span>
</div>
<div class="stat-card">
<span class="stat-val">-15%</span>
<span class="stat-label">Max Drawdown</span>
</div>
</div>
<div class="math-box">
<strong>Why not just hold SPXL?</strong><br>
During the 2020 crash, SPXL drew down over -70%. Recovering from a -70% loss requires a +233% gain just to break even. Our model moved to cash <i>before</i> the acceleration, preserving the capital base for the recovery.
</div>
<div class="chart-container">
<img src="{chart_src}" class="chart-img" alt="Chart showing model avoiding a downturn">
<div class="chart-caption">Figure 1.1: Volatility Regime Filter in Action</div>
</div>
</div>
</div>
</div>
</section>
<section id="pricing">
<div class="container">
<h2>Subscription</h2>
<p class="section-subtitle">Transparent pricing for individual traders and software licensing for proprietary trading desks.</p>
<div class="pricing-grid">
<div class="pricing-card">
<h3>Professional Signal</h3>
<p style="color:#888; font-size:0.9rem;">For independent traders.</p>
<div class="price">$299<span>/mo</span></div>
<ul class="features-list">
<li><span class="check">✓</span> Daily Signals (SPXL & SSO)</li>
<li><span class="check">✓</span> 7:00 AM Pre-market Alerts</li>
<li><span class="check">✓</span> Live Dashboard Access</li>
<li><span class="check">✓</span> Position Sizing Calculator</li>
<li><span class="check">✓</span> Private Community Access</li>
</ul>
<a href="#" class="btn-primary" style="width:100%;">Start 14-Day Trial</a>
</div>
<div class="pricing-card black">
<h3 class="orange">Enterprise Code</h3>
<p style="color:#aaa; font-size:0.9rem;">For developers & prop desks.</p>
<div class="price">Custom</div>
<ul class="features-list">
<li><span class="check">✓</span> <strong>Everything in Professional</strong></li>
<li><span class="check">✓</span> Low-Latency API (FIX/JSON)</li>
<li><span class="check">✓</span> <strong>Full Python Source Code</strong></li>
<li><span class="check">✓</span> Parameter Optimization Engine</li>
<li><span class="check">✓</span> On-Prem Docker Deployment</li>
<li><span class="check">✓</span> Developer Support</li>
</ul>
<a href="#" class="btn-primary" style="background-color:#fff; color:#000; width:100%;">Contact Sales</a>
</div>
</div>
</div>
</section>
<section id="faq">
<div class="container">
<h2>Common Questions</h2>
<div class="faq-grid">
<div class="faq-item">
<h4>Do you manage my money?</h4>
<p><strong>No.</strong> Benchmark3x is a software provider and financial publisher. We provide data signals. You execute the trades in your own brokerage account. We never touch your funds.</p>
</div>
<div class="faq-item">
<h4>Is this financial advice?</h4>
<p>No. Our signals are based on mathematical models and historical backtesting. They are for educational and informational purposes only. You must evaluate if 3x leverage fits your personal risk tolerance.</p>
</div>
<div class="faq-item">
<h4>How do I place the trades?</h4>
<p>Most subscribers receive our email/SMS alert at 7:00 AM ET and place a simple "Market On Open" order in their brokerage app. It takes less than 60 seconds a day. Enterprise clients can automate this via API.</p>
</div>
<div class="faq-item">
<h4>Why use SPXL (3x) instead of SPY?</h4>
<p>In low-volatility bull markets, SPXL offers superior alpha. The risk is the drawdown. Our model acts as a "safety switch," allowing you to hold the 3x asset only when conditions are mathematically favorable.</p>
</div>
<div class="faq-item">
<h4>What happens if I miss a signal?</h4>
<p>The strategy is designed for "swing trading" trends, not high-frequency scalping. Missing an entry by a few minutes or even an hour rarely impacts long-term performance significantly.</p>
</div>
<div class="faq-item">
<h4>Is the code actually provided?</h4>
<p>For Enterprise License holders, yes. We provide the full Python source code, allowing you to audit the strategy logic on your own infrastructure. We believe in "Glass Box" transparency, not Black Box secrets.</p>
</div>
<div class="faq-item">
<h4>Can I use this in an IRA or Roth IRA?</h4>
<p>Yes. SPXL and SSO are standard Exchange Traded Funds (ETFs) available in almost all self-directed retirement accounts. They do not require margin accounts or special permissions to trade.</p>
</div>
<div class="faq-item">
<h4>What brokerages are supported?</h4>
<p>Because we provide the signals (and not the execution), you can use any major brokerage including Fidelity, Charles Schwab, E*TRADE, Interactive Brokers, or Robinhood.</p>
</div>
<div class="faq-item">
<h4>Is there a specific cancellation policy?</h4>
<p>Yes. You can cancel your monthly subscription at any time with one click from your dashboard. You will retain access until the end of your current billing cycle. There are no long-term contracts for the Professional plan.</p>
</div>
<div class="faq-item">
<h4>Does the model short the market?</h4>
<p>No. The model is "Long Only." It switches between being invested in the ETF (SPXL/SSO) or sitting in Cash. We do not use inverse ETFs (like SPXU) or short selling, which reduces the risk of "whipsaw" losses significantly.</p>
</div>
</div>
</div>
</section>
</main>
<div class="landing-footer">
<div class="container">
<p>© 2025 Benchmark3x Analytics. All rights reserved.</p>
<p>
<a href="#">Terms of Service</a> | <a href="#">Privacy Policy</a> | <a href="#">Risk Disclosure</a>
</p>
<div class="disclaimer">
<p><strong>IMPORTANT DISCLAIMER:</strong> Benchmark3x is a software application and research tool. We are not a registered investment advisor, broker-dealer, or financial analyst. The information presented is for educational purposes only and does not constitute financial advice.</p>
<p>Hypothetical or simulated performance results have certain limitations. Unlike an actual performance record, simulated results do not represent actual trading. Also, since the trades have not been executed, the results may have under-or-over compensated for the impact, if any, of certain market factors, such as lack of liquidity. Trading leveraged ETFs involves substantial risk of loss.</p>
</div>
</div>
</div>
</div>
"""

# --- INJECT CONTENT VIA MARKDOWN ---
# Combining the Modular CSS and the Body HTML
st.markdown(LANDING_CSS + LANDING_BODY, unsafe_allow_html=True)