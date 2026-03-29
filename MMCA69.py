import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def simulate_virality(N, initial_viewers, beta, gamma, decay, days):

    S = N - initial_viewers
    I = initial_viewers
    R = 0

    S_list = []
    I_list = []
    R_list = []

    for t in range(days):

        new_viewers = beta * S * I / N
        dropped = gamma * I

        new_viewers *= np.exp(-decay * t)

        S -= new_viewers
        I += new_viewers - dropped
        R += dropped

        S_list.append(S)
        I_list.append(I)
        R_list.append(R)

    return S_list, I_list, R_list


st.set_page_config(page_title="Movie Trailer Virality", layout="centered")

st.title("🎬 Movie Trailer Virality Prediction")
st.write("MMCA Project: Growth-Decay + SIR Model")

st.sidebar.header("⚙️ Input Parameters")

N = st.sidebar.slider("Total Audience", 10000, 500000, 100000)
N = st.sidebar.number_input("Edit Total Audience", 10000, 500000, N, step=1000)

initial_viewers = st.sidebar.slider("Initial Viewers", 10, 1000, 100)
initial_viewers = st.sidebar.number_input("Edit Initial Viewers", 10, 1000, initial_viewers, step=10)

beta = st.sidebar.slider("Social Sharing Rate (β)", 0.0, 1.0, 0.3)
beta = st.sidebar.number_input("Edit β", 0.0, 1.0, beta, step=0.01, format="%.2f")

gamma = st.sidebar.slider("Drop Rate (γ)", 0.0, 1.0, 0.1)
gamma = st.sidebar.number_input("Edit γ", 0.0, 1.0, gamma, step=0.01, format="%.2f")

decay = st.sidebar.slider("Virality Decay", 0.0, 0.1, 0.01)
decay = st.sidebar.number_input("Edit Decay", 0.0, 0.1, decay, step=0.001, format="%.3f")

days = st.sidebar.slider("Simulation Days", 10, 120, 60)
days = st.sidebar.number_input("Edit Days", 10, 120, days, step=1)

st.markdown("""
## 📌 Project Overview

This simulation predicts **movie trailer virality** using a **Growth-Decay + SIR model**.

It analyzes how:
- Social sharing rate  
- Viewer drop rate  
- Virality decay  
- Initial audience  

affect trailer popularity over time.

The goal is to identify **peak popularity** and **viral spread behavior**.
""")

st.subheader("🔍 Key System Insights")

reproduction = beta / gamma if gamma != 0 else 0
peak_estimate = initial_viewers * reproduction

col1, col2 = st.columns(2)

with col1:
    st.info(f"""
**📊 Viral Reproduction Factor**  
{reproduction:.2f}

Higher value means stronger virality.
""")

with col2:
    st.info(f"""
🔥 Estimated Peak Viewers  
{int(peak_estimate)}

Expected maximum popularity
""")

st.success(f"""
💡 Interpretation:

- R < 1 → Trailer fades quickly  
- R ≈ 1 → Moderate popularity  
- R > 1 → Trailer becomes viral  

Current viral factor is **{reproduction:.2f}**
""")

S_list, I_list, R_list = simulate_virality(
    N, initial_viewers, beta, gamma, decay, days
)

st.subheader("📈 Trailer Virality Over Time")

fig, ax = plt.subplots()

ax.plot(S_list, label="Susceptible Viewers")
ax.plot(I_list, label="Active Sharers")
ax.plot(R_list, label="Dropped Viewers")

ax.set_xlabel("Days")
ax.set_ylabel("Number of Viewers")

ax.legend()

st.pyplot(fig)

peak_viewers = max(I_list)
peak_day = I_list.index(peak_viewers)

st.success(f"🔥 Peak occurs on Day: {peak_day}")
st.write(f"👥 Peak Active Viewers: {int(peak_viewers)}")

st.subheader("📊 Viewer Engagement Distribution")

fig2, ax2 = plt.subplots()
ax2.hist(I_list, bins=20)
ax2.set_xlabel("Active Viewers")
ax2.set_ylabel("Frequency")

st.pyplot(fig2)

st.subheader("📘 Mathematical Model")

st.latex(r"S_{t+1} = S_t - \beta \frac{S_t I_t}{N}")
st.latex(r"I_{t+1} = I_t + \beta \frac{S_t I_t}{N} - \gamma I_t")
st.latex(r"R_{t+1} = R_t + \gamma I_t")

st.markdown("""
**Where:**

• S = Susceptible viewers  
• I = Active sharers  
• R = Dropped viewers  
• β = Social sharing rate  
• γ = Drop rate  
• N = Total audience  
""")

st.subheader("⚙️ Viral Strength Calculation")

R0 = beta / gamma if gamma != 0 else 0

st.latex(r"R_0 = \frac{\beta}{\gamma} = %.2f" % R0)

st.markdown(f"""
**Step-by-step calculation:**

R₀ = β / γ  
R₀ = {beta} / {gamma}  
R₀ = **{R0:.2f}**
""")

if R0 > 1:
    st.success("✅ Trailer likely to go VIRAL")
else:
    st.warning("⚠️ Trailer may not go viral")

st.subheader("📌 Conclusion")

st.write(f"""
🔹 **1. Virality Curve**

- Active viewers increase due to social sharing  
- After peak, viewers decrease due to decay  
- Peak occurs on day **{peak_day}**

🔹 **2. Viewer Distribution**

- Most engagement happens near peak period  
- Early and late engagement is lower  
- Typical viral growth-decay pattern observed  

🔹 **Final Observation**

The trailer reaches **{int(peak_viewers)} peak viewers**.  
Higher sharing rate increases virality while decay reduces long-term engagement.
""")