import streamlit as st
import streamlit.components.v1 as components
import base64
import os

# 1. Configure page setup
st.set_page_config(layout="wide", page_title="Benchmark3x")

# 2. NUCLEAR CSS HACK: Force-remove all Streamlit padding
st.markdown("""
    <style>
        .block-container {
            padding-top: 0rem !important;
            padding-bottom: 0rem !important;
            padding-left: 0rem !important;
            padding-right: 0rem !important;
            margin: 0px !important;
            max-width: 100% !important;
        }
        header[data-testid="stHeader"] {
            visibility: hidden;
            height: 0px;
        }
        .main .block-container {
            margin-top: -60px !important; 
        }
        footer {display: none !important;}
        iframe {
            width: 100% !important;
        }
    </style>
    """, unsafe_allow_html=True)

# --- HELPER: Load Local Image to Base64 ---
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

# --- HTML & CSS TEMPLATE ---
# We use standard string concatenation/replacement to avoid f-string syntax errors.
landing_page_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Benchmark3x</title>
    <style>
        /* GLOBAL RESET */
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: "SF Pro Display", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
        html { scroll-behavior: smooth; }
        body { background-color: #ffffff; color: #333; overflow-x: hidden; }
        
        /* UTILITIES */
        .orange { color: #f5a623; }
        .text-center { text-align: center; }
        
        /* SECTION PADDING - INCREASED TO ~2 INCHES (160px) */
        .container { max-width: 1400px; margin: 0 auto; padding: 160px 5%; }
        
        h2 { font-size: 3rem; color: #111; margin-bottom: 30px; text-align: center; font-weight: 700; letter-spacing: -1px; }
        .section-subtitle { text-align: center; color: #666; font-size: 1.25rem; margin-bottom: 80px; max-width: 800px; margin-left: auto; margin-right: auto; line-height: 1.6; }
        p { line-height: 1.6; color: #555; }

        /* --- HEADER (Sticky) --- */
        header {
            background-color: #000000;
            padding: 15px 4%;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid #222;
            width: 100%;
            position: sticky; top: 0; z-index: 1000;
        }
        .logo-container { display: flex; align-items: center; text-decoration: none; cursor: pointer; }
        .logo-img { height: 90px; width: auto; display: block; mix-blend-mode: screen; }
        
        nav { display: flex; gap: 40px; align-items: center; }
        
        /* MENU TEXT INCREASED 25% */
        nav a {
            color: #ccc; text-decoration: none; font-size: 1.4rem; font-weight: 500;
            transition: color 0.3s; display: flex; align-items: center; cursor: pointer;
        }
        nav a:hover { color: #f5a623; }
        .nav-login { color: #fff; font-weight: 600; }
        .lock-icon { margin-right: 8px; font-size: 1.2rem; }

        /* --- HERO SECTION --- */
        .hero {
            display: flex; 
            justify-content: space-between; 
            align-items: flex-start;
            /* Top padding clears header, Bottom padding creates the 2 inch gap before next section */
            padding: 80px 5% 100px 5%;
            max-width: 1800px; 
            margin: 0 auto;
            height: auto;
        }
        
        .hero-text { 
            max-width: 45%; 
            margin-top: 15px; 
        }
        
        h1 { font-size: 3.8rem; line-height: 1.1; color: #111; margin-bottom: 25px; font-weight: 800; letter-spacing: -1px; }
        .hero-p { font-size: 1.2rem; margin-bottom: 35px; max-width: 520px; color: #555; }
        
        .btn-primary {
            display: inline-block; background-color: #f5a623; color: white;
            padding: 14px 35px; text-decoration: none; border-radius: 4px;
            font-weight: 700; font-size: 1rem; transition: transform 0.2s, background-color 0.2s; border: none; cursor: pointer;
        }
        .btn-primary:hover { transform: translateY(-2px); background-color: #e0961f; }

        /* --- COMPUTER GRAPHIC --- */
        .computer-graphic {
            width: 50%;
            border-radius: 12px;
            box-shadow: 0 30px 60px rgba(0,0,0,0.25);
            object-fit: cover;
            transform: perspective(1000px) rotateY(-5deg) rotateX(2deg);
            transition: transform 0.5s ease;
        }
        .computer-graphic:hover { transform: perspective(1000px) rotateY(0deg); }

        /* --- MODEL SECTION (Was 'Logic') --- */
        /* Extra padding for spacing */
        #model { background-color: #f8f9fa; border-top: 1px solid #eee; padding-top: 160px; padding-bottom: 160px; scroll-margin-top: 60px; }
        
        .model-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 80px; align-items: start; }
        .model-step { margin-bottom: 45px; display: flex; gap: 25px; }
        .step-num { 
            font-size: 2.2rem; font-weight: 800; color: #e0e0e0; min-width: 50px; line-height: 1;
        }
        .step-content h4 { font-size: 1.4rem; margin-bottom: 12px; color: #222; }
        .step-content p { font-size: 1.1rem; color: #555; }
        
        .stat-card-row { display: grid; grid-template-columns: 1fr 1fr; gap: 25px; margin-top: 40px; }
        .stat-card { background: #fff; padding: 30px; border-radius: 8px; box-shadow: 0 4px 20px rgba(0,0,0,0.06); text-align: center; }
        .stat-val { font-size: 2.8rem; font-weight: 700; color: #000; display: block; margin-bottom: 5px; }
        .stat-label { font-size: 0.95rem; color: #888; text-transform: uppercase; letter-spacing: 1px; font-weight: 600; }
        
        .math-box {
            background-color: #fff;
            padding: 30px;
            border-radius: 8px;
            border-left: 5px solid #f5a623;
            margin-top: 30px;
            font-size: 1rem;
            line-height: 1.6;
            box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        }

        /* --- PRICING SECTION --- */
        #pricing { background-color: #fff; padding-top: 160px; padding-bottom: 160px; scroll-margin-top: 60px; }
        .pricing-grid { display: flex; justify-content: center; gap: 50px; margin-top: 60px; flex-wrap: wrap; }
        .pricing-card {
            background: #fff; border: 1px solid #e1e1e1; border-radius: 12px; padding: 50px;
            width: 420px; display: flex; flex-direction: column;
            transition: transform 0.3s, box-shadow 0.3s;
        }
        .pricing-card:hover { transform: translateY(-10px); box-shadow: 0 20px 40px rgba(0,0,0,0.1); border-color: #f5a623; }
        .pricing-card.black { background: #111; color: #fff; border: 1px solid #111; }
        .pricing-card.black h3, .pricing-card.black .price, .pricing-card.black p, .pricing-card.black li { color: #fff; }
        
        .pricing-card h3 { font-size: 1.8rem; margin-bottom: 10px; }
        .price { font-size: 3.5rem; font-weight: 800; margin: 25px 0; letter-spacing: -2px; }
        .price span { font-size: 1rem; color: #999; font-weight: 400; letter-spacing: 0; }
        .features-list { list-style: none; margin: 30px 0; flex-grow: 1; }
        .features-list li { margin-bottom: 18px; font-size: 1.1rem; display: flex; align-items: center; color: #555; }
        .check { color: #f5a623; margin-right: 15px; font-weight: bold; }

        /* --- FAQ SECTION --- */
        #faq { background-color: #f8f9fa; border-top: 1px solid #eee; padding-top: 160px; padding-bottom: 160px; scroll-margin-top: 60px; }
        .faq-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 50px; }
        .faq-item { background: #fff; padding: 40px; border-radius: 8px; border: 1px solid #eee; }
        .faq-item h4 { font-size: 1.3rem; margin-bottom: 15px; font-weight: 700; color: #111; }
        .faq-item p { font-size: 1.05rem; color: #666; line-height: 1.7; }

        /* --- FOOTER --- */
        footer { background: #111; color: #666; padding: 80px 5%; text-align: center; border-top: 1px solid #222; }
        footer p { font-size: 0.9rem; margin-bottom: 10px; }
        footer a { color: #888; text-decoration: none; }
        .disclaimer { font-size: 0.8rem; color: #555; max-width: 900px; margin: 30px auto; line-height: 1.6; }
    </style>
</head>
<body>
    <header id="top">
        <a href="#top" class="logo-container">
            <img src="{LOGO_SRC}" class="logo-img" alt="Benchmark3x" />
        </a>
        <nav>
            <a href="#model">Model</a>
            <a href="#pricing">Pricing</a>
            <a href="#faq">FAQ</a>
            <a href="#" class="nav-login"><span class="lock-icon">🔒</span> Sign In</a>
        </nav>
    </header>

    <main>
        <section class="hero">
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
            <img src="{COMPUTER_SRC}" class="computer-graphic" alt="Trading Terminal">
        </section>

        <section id="model" class="container">
            <h2>The Benchmark3x Model</h2>
            <p class="section-subtitle">
                A multi-factor quantitative engine designed to navigate the complexities of leveraged ETFs. 
                We move beyond simple "volatility decay" concerns by actively filtering market regimes.
            </p>
            
            <div class="model-grid">
                <div>
                    <div class="model-step">
                        <div class="step-num">01</div>
                        <div class="step-content">
                            <h4>Multi-Factor Inputs</h4>
                            <p>The model ingests a diverse array of market health indicators, including the VIX futures term structure (Contango/Backwardation), realized volatility variance (HV10 vs HV20), and price trend momentum. It is not reliant on a single indicator.</p>
                        </div>
                    </div>
                    <div class="model-step">
                        <div class="step-num">02</div>
                        <div class="step-content">
                            <h4>Regime Classification</h4>
                            <p>Using these inputs, the engine classifies the current market into one of two states: <strong>Stable Bull</strong> (suitable for leverage) or <strong>High Stress</strong> (cash preservation). This binary classification removes ambiguity.</p>
                        </div>
                    </div>
                    <div class="model-step">
                        <div class="step-num">03</div>
                        <div class="step-content">
                            <h4>Signal Output</h4>
                            <p>When the regime is favorable, the model issues a "Risk On" signal to allocate to SPXL or SSO. When volatility metrics breach safety thresholds, it issues a "Risk Off" signal to move to Cash/Treasuries immediately.</p>
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
                        <strong>Why Regime Filtering Matters</strong><br>
                        Leveraged ETFs amplify returns daily. In a "choppy" market where the S&P 500 goes sideways, a 3x ETF loses value mathematically. Our model's primary job is to identify these choppy regimes and step aside, re-entering only when the probability of a sustained trend is high.
                    </div>
                </div>
            </div>
        </section>

        <section id="pricing" class="container">
            <h2>Software Licenses</h2>
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
                    <button class="btn-primary" style="width:100%;">Start 14-Day Trial</button>
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
                    <button class="btn-primary" style="background-color:#fff; color:#000; width:100%;">Contact Sales</button>
                </div>
            </div>
        </section>

        <section id="faq" class="container">
            <h2>Common Questions</h2>
            <div class="faq-grid">
                <div class="faq-item">
                    <h4>How exactly do I trade the signal?</h4>
                    <p>Trading is simple and takes less than 2 minutes a day. 
                    <br>1. Check your email/dashboard at <strong>7:00 AM ET</strong>.
                    <br>2. If the signal says "BUY SPXL", log into your brokerage.
                    <br>3. Place a "Market on Open" (MOO) order for the ETF.
                    <br>4. The trade executes automatically at 9:30 AM. No intraday monitoring required.</p>
                </div>
                <div class="faq-item">
                    <h4>Do you manage my money?</h4>
                    <p><strong>No.</strong> Benchmark3x is purely a software and data provider. We provide the analytics and signals. You maintain full control and custody of your funds at your own brokerage. We never touch your capital.</p>
                </div>
                <div class="faq-item">
                    <h4>Is this financial advice?</h4>
                    <p>No. Our signals are generated by mathematical algorithms based on historical data. They are for educational and informational purposes. You must decide if trading leveraged ETFs fits your personal risk tolerance and financial situation.</p>
                </div>
                <div class="faq-item">
                    <h4>How does the model handle drawdowns?</h4>
                    <p>Drawdowns are managed via the Regime Filter. If volatility metrics spike (signaling a potential crash), the model moves to Cash. Historically, this has kept drawdowns significantly lower than a "buy and hold" approach, but losses can still occur.</p>
                </div>
                <div class="faq-item">
                    <h4>What is the typical holding period?</h4>
                    <p>This is a swing-trading strategy. In strong bull markets, the model may hold a position for weeks or months. In volatile chop, it may switch between Cash and Equity multiple times a month to protect gains.</p>
                </div>
                <div class="faq-item">
                    <h4>Is the code actually provided?</h4>
                    <p>For Enterprise License holders, yes. We provide the full Python source code, allowing you to audit the strategy logic on your own infrastructure. We believe in "Glass Box" transparency, not Black Box secrets.</p>
                </div>
            </div>
        </section>
    </main>

    <footer>
        <p>© 2025 Benchmark3x Analytics. All rights reserved.</p>
        <p>
            <a href="#">Terms of Service</a> | <a href="#">Privacy Policy</a> | <a href="#">Risk Disclosure</a>
        </p>
        <div class="disclaimer">
            <p><strong>IMPORTANT DISCLAIMER:</strong> Benchmark3x is a software application and research tool. We are not a registered investment advisor, broker-dealer, or financial analyst. The information presented is for educational purposes only and does not constitute financial advice.</p>
            <p>Hypothetical or simulated performance results have certain limitations. Unlike an actual performance record, simulated results do not represent actual trading. Also, since the trades have not been executed, the results may have under-or-over compensated for the impact, if any, of certain market factors, such as lack of liquidity. Trading leveraged ETFs involves substantial risk of loss.</p>
        </div>
    </footer>

    <script>
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                document.querySelector(this.getAttribute('href')).scrollIntoView({
                    behavior: 'smooth'
                });
            });
        });
    </script>
</body>
</html>
"""

# Replace placeholders with actual image data
landing_page_html = landing_page_html.replace("{LOGO_SRC}", logo_src)
landing_page_html = landing_page_html.replace("{COMPUTER_SRC}", computer_src)

# Render with scrolling allowed
components.html(landing_page_html, height=3500, scrolling=True)