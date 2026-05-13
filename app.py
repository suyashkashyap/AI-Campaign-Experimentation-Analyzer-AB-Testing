
import streamlit as st
import pandas as pd
import numpy as np
from statsmodels.stats.proportion import proportions_ztest

# ======================================================
# PAGE CONFIG
# ======================================================

st.set_page_config(
    page_title="AI Campaign Experimentation Analyzer",
    layout="wide"
)

# ======================================================
# TITLE
# ======================================================

st.title("AI-Assisted Campaign Experimentation Analyzer")

st.markdown("""
This application helps you:

- Upload A/B testing campaign CSV file
- Calculate marketing funnel metrics
- Compare Test vs Control
- Calculate Lift %
- Run Statistical Significance Testing @90%
- Identify Winning Creative
- Generate AI-ready experiment insights
""")

# ======================================================
# FILE UPLOAD
# ======================================================

uploaded_file = st.file_uploader(
    "Upload Campaign CSV File",
    type=["csv"]
)

# ======================================================
# MAIN LOGIC
# ======================================================

if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)

    st.subheader("Uploaded Raw Data")

    st.dataframe(df)

    # ==================================================
    # CALCULATED METRICS
    # ==================================================

    df['Open Rate'] = df['opn'] / df['snd']

    df['Click Rate'] = df['clk'] / df['snd']

    df['Unsub Rate'] = df['unsub'] / df['snd']

    df['App Rate'] = np.where(
        df['clk'] == 0,
        0,
        df['app'] / df['clk']
    )

    df['Response Rate'] = df['app'] / df['snd']

    df['Offer Rate'] = np.where(
        df['app'] == 0,
        0,
        df['offer'] / df['app']
    )

    df['Take Rate'] = np.where(
        df['offer'] == 0,
        0,
        df['listings'] / df['offer']
    )

    df['$LPM'] = df['listing_amount'] / df['snd']

    df['ALS'] = np.where(
        df['listings'] == 0,
        0,
        df['listing_amount'] / df['listings']
    )

    df['#LPM'] = df['listings'] / df['snd']

    st.subheader("Calculated Metrics")

    st.dataframe(df)

    # ==================================================
    # STAT SIG FUNCTION
    # ==================================================

    ALPHA = 0.10

    def proportion_significance_test(success_test,
                                     total_test,
                                     success_control,
                                     total_control):

        try:

            count = np.array([
                success_test,
                success_control
            ])

            nobs = np.array([
                total_test,
                total_control
            ])

            stat, p_value = proportions_ztest(
                count,
                nobs
            )

            significant = p_value < ALPHA

            return round(p_value, 4), significant

        except:
            return None, False

    # ==================================================
    # IDENTIFY TEST/CONTROL VALUES
    # ==================================================

    tc_values = [
        str(x).strip().upper()
        for x in df['tc_flag'].unique()
    ]

    if 'CONTROL' in tc_values and 'TEST' in tc_values:

        control_value = 'CONTROL'
        test_value = 'TEST'

    elif 'C' in tc_values and 'T' in tc_values:

        control_value = 'C'
        test_value = 'T'

    else:

        st.error("tc_flag values not recognized.")
        st.stop()

    # ==================================================
    # AB TESTING
    # ==================================================

    results = []

    segments = df['segment'].dropna().unique()

    for seg in segments:

        seg_df = df[df['segment'] == seg]

        if seg_df['tc_flag'].nunique() < 2:
            continue

        control = seg_df[
            seg_df['tc_flag'].astype(str).str.upper()
            == control_value
        ]

        test = seg_df[
            seg_df['tc_flag'].astype(str).str.upper()
            == test_value
        ]

        if control.empty or test.empty:
            continue

        control = control.iloc[0]
        test = test.iloc[0]

        metrics = [

            ('Open Rate', 'opn', 'snd'),

            ('Click Rate', 'clk', 'snd'),

            ('Unsub Rate', 'unsub', 'snd'),

            ('Response Rate', 'app', 'snd'),

            ('Offer Rate', 'offer', 'app'),

            ('Take Rate', 'listings', 'offer'),

            ('#LPM', 'listings', 'snd')

        ]

        for metric_name, numerator, denominator in metrics:

            p_value, significant = proportion_significance_test(

                test[numerator],
                test[denominator],

                control[numerator],
                control[denominator]

            )

            test_metric = test[metric_name]

            control_metric = control[metric_name]

            if control_metric != 0:

                lift = (
                    (test_metric - control_metric)
                    / control_metric
                ) * 100

            else:
                lift = 0

            winner = (
                'Test'
                if test_metric > control_metric
                else 'Control'
            )

            results.append({

                'Segment': seg,

                'Metric': metric_name,

                'Control': round(control_metric, 4),

                'Test': round(test_metric, 4),

                'Lift %': round(lift, 2),

                'P Value': p_value,

                'Stat Significant @90%': significant,

                'Winner': winner

            })

    result_df = pd.DataFrame(results)

    # ==================================================
    # SHOW RESULTS
    # ==================================================

    st.subheader("A/B Testing Results")

    st.dataframe(result_df)

    # ==================================================
    # WINNING METRICS
    # ==================================================

    st.subheader("Winning Metrics")

    winners = result_df[
        result_df['Stat Significant @90%'] == True
    ]

    if len(winners) > 0:

        for _, row in winners.iterrows():

            st.success(

                f"""
                Segment: {row['Segment']}
                | Metric: {row['Metric']}
                | Winner: {row['Winner']}
                | Lift: {row['Lift %']}%
                """

            )

    else:

        st.warning(
            "No statistically significant winners found."
        )

    # ==================================================
    # DOWNLOAD OUTPUT
    # ==================================================

    csv = result_df.to_csv(index=False).encode('utf-8')

    st.download_button(

        label="Download AB Test Results",

        data=csv,

        file_name="AB_Test_Results.csv",

        mime="text/csv"

    )

# ======================================================
# FUTURE GPT INTEGRATION
# ======================================================

st.markdown("---")

st.header("Future GPT Integration")

st.markdown("""

Future versions can integrate ChatGPT APIs to:

- Suggest increasing audience size
- Recommend better subject lines
- Suggest CTA optimization
- Recommend stopping weak tests
- Generate stakeholder summaries
- Generate executive readouts
- Predict campaign performance
- Suggest high-performing segments

Example Integration:

```python
from openai import OpenAI

client = OpenAI(api_key='YOUR_API_KEY')

response = client.chat.completions.create(
    model='gpt-4o-mini',
    messages=[
        {
            'role': 'user',
            'content': f'Analyze AB test results: {result_df}'
        }
    ]
)

print(response.choices[0].message.content)
```

""")
