import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


st.set_page_config(
    page_title="Customer Segmentation Dashboard",
    layout="wide"
)

st.title("🛍️ Customer Segmentation Dashboard")
st.write("Analyze customer groups using Machine Learning")

df = pd.read_csv("Mall_Customers.csv")


st.subheader("📄 Dataset")

st.dataframe(df)


df.dropna(inplace=True)


X = df[['Age', 'Annual Income (k$)', 'Spending Score (1-100)']]


scaler = StandardScaler()

X_scaled = scaler.fit_transform(X)
st.subheader("📈 Elbow Method")

wcss = []

for i in range(1, 11):
    kmeans = KMeans(
        n_clusters=i,
        random_state=42,
        n_init=10
    )

    kmeans.fit(X_scaled)

    wcss.append(kmeans.inertia_)

fig1, ax1 = plt.subplots(figsize=(8,5))

ax1.plot(range(1,11), wcss, marker='o')

ax1.set_title("Elbow Method")
ax1.set_xlabel("Number of Clusters")
ax1.set_ylabel("WCSS")

st.pyplot(fig1)


st.sidebar.header("⚙️ Clustering Settings")

clusters = st.sidebar.slider(
    "Select Number of Clusters",
    2,
    10,
    5
)


kmeans = KMeans(
    n_clusters=clusters,
    random_state=42,
    n_init=10
)

df['Cluster'] = kmeans.fit_predict(X_scaled)


st.subheader("📊 Dashboard KPIs")

col1, col2, col3 = st.columns(3)

col1.metric("Total Customers", len(df))
col2.metric("Clusters", clusters)
col3.metric("Average Spending Score", round(df['Spending Score (1-100)'].mean(), 2))


st.subheader("🎯 Customer Segments")

fig2, ax2 = plt.subplots(figsize=(10,7))

sns.scatterplot(
    x='Annual Income (k$)',
    y='Spending Score (1-100)',
    hue='Cluster',
    palette='Set1',
    data=df,
    s=100,
    ax=ax2
)


centroids = scaler.inverse_transform(kmeans.cluster_centers_)

ax2.scatter(
    centroids[:,1],
    centroids[:,2],
    s=300,
    c='black',
    marker='X',
    label='Centroids'
)

ax2.set_title("Customer Segmentation")
ax2.set_xlabel("Annual Income")
ax2.set_ylabel("Spending Score")

ax2.legend()

st.pyplot(fig2)


st.subheader("📌 Cluster Summary")

cluster_summary = df.groupby('Cluster').mean(numeric_only=True)

st.dataframe(cluster_summary)


st.subheader("📊 Customers in Each Cluster")

cluster_count = df['Cluster'].value_counts()

fig3, ax3 = plt.subplots(figsize=(7,5))

cluster_count.plot(
    kind='bar',
    ax=ax3
)

ax3.set_title("Customer Count by Cluster")
ax3.set_xlabel("Cluster")
ax3.set_ylabel("Number of Customers")

st.pyplot(fig3)


csv = df.to_csv(index=False).encode('utf-8')

st.download_button(
    label="⬇️ Download Segmented Data",
    data=csv,
    file_name='segmented_customers.csv',
    mime='text/csv'
)


st.success("Customer Segmentation Dashboard Created Successfully!")