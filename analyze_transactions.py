import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Set style for better visualizations
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 8)

print("=" * 80)
print("TRANSACTION DATA ANALYSIS")
print("=" * 80)

# Load the CSV file
df = pd.read_csv('bo Kopie.csv')

print("\n1. RAW DATA STRUCTURE")
print("-" * 80)
print(f"Total rows in raw CSV: {len(df)}")
print(f"Total columns: {len(df.columns)}")
print(f"Column names: {list(df.columns)}")

# The data has odd/even columns - let's extract transactions properly
transactions = []

for idx, row in df.iterrows():
    # Extract odd transaction (columns with "odd" prefix)
    if pd.notna(row['odd']) and row['odd'] != '':
        transactions.append({
            'timestamp': row['odd'],
            'transaction_id': row['odd 2'],
            'status': row['odd 3'],
            'customer_name': row['odd 4'],
            'amount_str': row['odd 5'],
            'reference': row['odd 6']
        })

    # Extract even transaction (columns with "even" prefix)
    if pd.notna(row['even']) and row['even'] != '':
        transactions.append({
            'timestamp': row['even'],
            'transaction_id': row['even 2'],
            'status': row['even 3'],
            'customer_name': row['even 4'],
            'amount_str': row['even 5'],
            'reference': row['even 6']
        })

# Create proper dataframe
df_clean = pd.DataFrame(transactions)

# Clean and convert data types
df_clean['timestamp'] = pd.to_datetime(df_clean['timestamp'])
df_clean['amount'] = df_clean['amount_str'].str.replace(' EUR', '').astype(float)
df_clean['date'] = df_clean['timestamp'].dt.date
df_clean['hour'] = df_clean['timestamp'].dt.hour
df_clean['day_of_week'] = df_clean['timestamp'].dt.day_name()
df_clean['week'] = df_clean['timestamp'].dt.isocalendar().week

print("\n2. CLEANED DATA OVERVIEW")
print("-" * 80)
print(f"Total transactions: {len(df_clean)}")
print(f"Date range: {df_clean['timestamp'].min()} to {df_clean['timestamp'].max()}")
print(f"Duration: {(df_clean['timestamp'].max() - df_clean['timestamp'].min()).days} days")

print("\n3. TRANSACTION STATUS BREAKDOWN")
print("-" * 80)
status_counts = df_clean['status'].value_counts()
for status, count in status_counts.items():
    percentage = (count / len(df_clean)) * 100
    print(f"{status:15s}: {count:4d} ({percentage:5.2f}%)")

print("\n4. FINANCIAL SUMMARY")
print("-" * 80)
print(f"Total transaction value: €{df_clean['amount'].sum():,.2f}")
print(f"Average transaction: €{df_clean['amount'].mean():,.2f}")
print(f"Median transaction: €{df_clean['amount'].median():,.2f}")
print(f"Largest transaction: €{df_clean['amount'].max():,.2f}")
print(f"Smallest transaction: €{df_clean['amount'].min():,.2f}")
print(f"Standard deviation: €{df_clean['amount'].std():,.2f}")

# Financial breakdown by status
print("\n5. FINANCIAL BREAKDOWN BY STATUS")
print("-" * 80)
for status in df_clean['status'].unique():
    status_df = df_clean[df_clean['status'] == status]
    total = status_df['amount'].sum()
    count = len(status_df)
    avg = status_df['amount'].mean()
    print(f"{status:15s}: Total: €{total:11,.2f} | Count: {count:4d} | Avg: €{avg:8,.2f}")

print("\n6. TOP 10 CUSTOMERS BY TRANSACTION VALUE")
print("-" * 80)
customer_totals = df_clean.groupby('customer_name').agg({
    'amount': ['sum', 'count', 'mean']
}).round(2)
customer_totals.columns = ['Total_Amount', 'Transaction_Count', 'Avg_Amount']
customer_totals = customer_totals.sort_values('Total_Amount', ascending=False)
print(customer_totals.head(10))

print("\n7. TOP 10 MOST FREQUENT CUSTOMERS")
print("-" * 80)
customer_frequency = df_clean['customer_name'].value_counts().head(10)
for name, count in customer_frequency.items():
    total_amount = df_clean[df_clean['customer_name'] == name]['amount'].sum()
    print(f"{name:40s}: {count:3d} transactions, Total: €{total_amount:,.2f}")

print("\n8. DAILY TRANSACTION SUMMARY")
print("-" * 80)
daily_summary = df_clean.groupby('date').agg({
    'amount': ['sum', 'count', 'mean']
}).round(2)
daily_summary.columns = ['Total_Amount', 'Count', 'Avg_Amount']
print(daily_summary)

print("\n9. TIME-BASED PATTERNS")
print("-" * 80)
hourly_dist = df_clean.groupby('hour').size()
print("Transactions by hour of day:")
for hour, count in hourly_dist.items():
    print(f"  {hour:02d}:00 - {count:3d} transactions")

print("\n10. AMOUNT DISTRIBUTION")
print("-" * 80)
print("Transaction value ranges:")
bins = [0, 1000, 2000, 3000, 4000, 5000, 10000]
labels = ['€0-1k', '€1k-2k', '€2k-3k', '€3k-4k', '€4k-5k', '€5k+']
df_clean['amount_range'] = pd.cut(df_clean['amount'], bins=bins, labels=labels)
range_counts = df_clean['amount_range'].value_counts().sort_index()
for range_label, count in range_counts.items():
    percentage = (count / len(df_clean)) * 100
    print(f"  {range_label:10s}: {count:4d} ({percentage:5.2f}%)")

# Save cleaned data
df_clean.to_csv('transactions_cleaned.csv', index=False)
print("\n" + "=" * 80)
print("Cleaned data saved to: transactions_cleaned.csv")
print("=" * 80)

# Create visualizations
print("\nGenerating visualizations...")

# Figure 1: Transaction value over time
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# 1. Daily transaction value
daily_amounts = df_clean.groupby('date')['amount'].sum()
axes[0, 0].plot(daily_amounts.index, daily_amounts.values, marker='o', linewidth=2, markersize=6)
axes[0, 0].set_title('Daily Transaction Volume', fontsize=14, fontweight='bold')
axes[0, 0].set_xlabel('Date')
axes[0, 0].set_ylabel('Total Amount (EUR)')
axes[0, 0].grid(True, alpha=0.3)
axes[0, 0].tick_params(axis='x', rotation=45)

# 2. Transaction status distribution
status_data = df_clean['status'].value_counts()
colors = ['#2ecc71', '#e74c3c', '#3498db', '#f39c12']
axes[0, 1].pie(status_data.values, labels=status_data.index, autopct='%1.1f%%',
               colors=colors, startangle=90)
axes[0, 1].set_title('Transaction Status Distribution', fontsize=14, fontweight='bold')

# 3. Amount distribution histogram
axes[1, 0].hist(df_clean['amount'], bins=50, edgecolor='black', alpha=0.7, color='#3498db')
axes[1, 0].set_title('Transaction Amount Distribution', fontsize=14, fontweight='bold')
axes[1, 0].set_xlabel('Amount (EUR)')
axes[1, 0].set_ylabel('Frequency')
axes[1, 0].grid(True, alpha=0.3)

# 4. Hourly transaction pattern
hourly_counts = df_clean.groupby('hour').size()
axes[1, 1].bar(hourly_counts.index, hourly_counts.values, color='#9b59b6', alpha=0.7)
axes[1, 1].set_title('Transactions by Hour of Day', fontsize=14, fontweight='bold')
axes[1, 1].set_xlabel('Hour')
axes[1, 1].set_ylabel('Number of Transactions')
axes[1, 1].grid(True, alpha=0.3, axis='y')
axes[1, 1].set_xticks(range(0, 24))

plt.tight_layout()
plt.savefig('transaction_analysis_overview.png', dpi=300, bbox_inches='tight')
print("Saved: transaction_analysis_overview.png")

# Figure 2: Top customers analysis
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Top 15 customers by value
top_customers = df_clean.groupby('customer_name')['amount'].sum().sort_values(ascending=False).head(15)
axes[0].barh(range(len(top_customers)), top_customers.values, color='#e74c3c', alpha=0.7)
axes[0].set_yticks(range(len(top_customers)))
axes[0].set_yticklabels([name[:30] for name in top_customers.index], fontsize=9)
axes[0].set_xlabel('Total Transaction Value (EUR)')
axes[0].set_title('Top 15 Customers by Total Value', fontsize=14, fontweight='bold')
axes[0].grid(True, alpha=0.3, axis='x')

# Top 15 customers by frequency
top_freq = df_clean['customer_name'].value_counts().head(15)
axes[1].barh(range(len(top_freq)), top_freq.values, color='#3498db', alpha=0.7)
axes[1].set_yticks(range(len(top_freq)))
axes[1].set_yticklabels([name[:30] for name in top_freq.index], fontsize=9)
axes[1].set_xlabel('Number of Transactions')
axes[1].set_title('Top 15 Most Frequent Customers', fontsize=14, fontweight='bold')
axes[1].grid(True, alpha=0.3, axis='x')

plt.tight_layout()
plt.savefig('customer_analysis.png', dpi=300, bbox_inches='tight')
print("Saved: customer_analysis.png")

# Figure 3: Time series analysis
fig, axes = plt.subplots(2, 1, figsize=(16, 10))

# Daily transaction count and value
daily_stats = df_clean.groupby('date').agg({
    'amount': ['sum', 'count']
})

ax1 = axes[0]
ax2 = ax1.twinx()
ax1.bar(daily_stats.index, daily_stats[('amount', 'count')], alpha=0.5, color='#3498db', label='Count')
ax2.plot(daily_stats.index, daily_stats[('amount', 'sum')], color='#e74c3c', marker='o',
         linewidth=2, markersize=6, label='Total Value')
ax1.set_xlabel('Date')
ax1.set_ylabel('Transaction Count', color='#3498db')
ax2.set_ylabel('Total Value (EUR)', color='#e74c3c')
ax1.tick_params(axis='y', labelcolor='#3498db')
ax2.tick_params(axis='y', labelcolor='#e74c3c')
ax1.tick_params(axis='x', rotation=45)
axes[0].set_title('Daily Transaction Count vs Total Value', fontsize=14, fontweight='bold')
ax1.grid(True, alpha=0.3)

# Cumulative transaction value
df_clean_sorted = df_clean.sort_values('timestamp')
df_clean_sorted['cumulative_amount'] = df_clean_sorted['amount'].cumsum()
axes[1].plot(df_clean_sorted['timestamp'], df_clean_sorted['cumulative_amount'],
            linewidth=2, color='#2ecc71')
axes[1].fill_between(df_clean_sorted['timestamp'], df_clean_sorted['cumulative_amount'],
                     alpha=0.3, color='#2ecc71')
axes[1].set_title('Cumulative Transaction Value Over Time', fontsize=14, fontweight='bold')
axes[1].set_xlabel('Date')
axes[1].set_ylabel('Cumulative Amount (EUR)')
axes[1].grid(True, alpha=0.3)
axes[1].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig('time_series_analysis.png', dpi=300, bbox_inches='tight')
print("Saved: time_series_analysis.png")

print("\n" + "=" * 80)
print("ANALYSIS COMPLETE!")
print("=" * 80)
print("\nGenerated files:")
print("  1. transactions_cleaned.csv - Cleaned transaction data")
print("  2. transaction_analysis_overview.png - Main overview dashboard")
print("  3. customer_analysis.png - Customer insights")
print("  4. time_series_analysis.png - Time-based trends")
print("=" * 80)
