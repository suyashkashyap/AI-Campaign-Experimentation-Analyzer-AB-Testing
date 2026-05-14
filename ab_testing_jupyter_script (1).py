
import pandas as pd
import numpy as np
from statsmodels.stats.proportion import proportions_ztest

# ============================================
# FILE PATH
# ============================================

file_path = r"E:\AI 2026\AI_AB_TEST\Email_Campaign_Data_Sample_v2.xlsx"

# ============================================
# LOAD DATA
# ============================================

df = pd.read_excel(file_path)

print("Data Loaded Successfully")
print(df.head())

# ============================================
# CALCULATED METRICS
# ============================================

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

print("\nCalculated Metrics Added Successfully")

# ============================================
# STATISTICAL SIGNIFICANCE FUNCTION
# ============================================

ALPHA = 0.10  # 90% Confidence


def proportion_significance_test(success_test,
                                 total_test,
                                 success_control,
                                 total_control):

    try:

        count = np.array([success_test, success_control])

        nobs = np.array([total_test, total_control])

        stat, p_value = proportions_ztest(count, nobs)

        significant = p_value < ALPHA

        return round(p_value, 4), significant

    except:
        return None, False


# ============================================
# AB TESTING SEGMENT WISE
# ============================================

results = []

segments = df['segment'].unique()

for seg in segments:

    seg_df = df[df['segment'] == seg]

    if seg_df['creative_type'].nunique() < 2:
        continue

    control = seg_df[seg_df['creative_type'] == 'Control']
    test = seg_df[seg_df['creative_type'] == 'Test']

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
            lift = ((test_metric - control_metric) / control_metric) * 100
        else:
            lift = 0

        winner = 'Test' if test_metric > control_metric else 'Control'

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

# ============================================
# FINAL OUTPUT
# ============================================

result_df = pd.DataFrame(results)

print("\nAB Testing Completed Successfully")

print("\n==============================")
print("AB TEST RESULTS")
print("==============================")

print(result_df)

# ============================================
# WINNING METRICS
# ============================================

print("\n==============================")
print("WINNING METRICS")
print("==============================")

winners = result_df[
    result_df['Stat Significant @90%'] == True
]

if len(winners) > 0:

    for _, row in winners.iterrows():

        print(
            f"Segment: {row['Segment']} | "
            f"Metric: {row['Metric']} | "
            f"Winner: {row['Winner']} | "
            f"Lift: {row['Lift %']}%"
        )

else:
    print("No statistically significant winners found.")

# ============================================
# SAVE OUTPUT
# ============================================

output_path = r"E:\AI 2026\AI_AB_TEST\AB_Testing_Output.xlsx"

with pd.ExcelWriter(output_path, engine='openpyxl') as writer:

    df.to_excel(writer,
                sheet_name='Calculated_Metrics',
                index=False)

    result_df.to_excel(writer,
                       sheet_name='AB_Test_Results',
                       index=False)

print(f"\nOutput File Saved Successfully")
print(f"Location: {output_path}")

# ============================================
# FUTURE GPT INTEGRATION IDEA
# ============================================

print("\n==============================")
print("FUTURE GPT INTEGRATION")
print("==============================")

print("""
Future GPT integration can:
- Suggest better subject lines
- Recommend increasing audience size
- Recommend stopping weak tests
- Suggest CTA optimization
- Generate executive summaries
- Predict future campaign performance

Example Integration:
Use OpenAI GPT API and pass AB testing output dataframe
to generate AI recommendations.
""")
