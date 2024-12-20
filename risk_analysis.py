import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import networkx as nx

# Streamlit app for new risk analysis
def risk_analysis_app():
    st.title("Ny Riskanalys")

    # Step 1: Generate Synthetic Data
    np.random.seed(42)

    # Synthetic membership data
    membership_data = pd.DataFrame({
        'förening_id': np.arange(1, 101),
        'medlemmar': np.random.poisson(50, 100),  # Poisson distribution for normal distribution of members
        'kostnad': np.random.normal(5000, 1000, 100)  # Normally distributed costs
    })

    # Synthetic activity logs
    activity_logs = pd.DataFrame({
        'förening_id': np.random.choice(membership_data['förening_id'], 300),
        'aktivitet': np.random.choice(['sport', 'kultur', 'utbildning'], 300),
        'deltagare': np.random.poisson(20, 300)
    })

    # Synthetic text data for reports
    reports = pd.DataFrame({
        'förening_id': membership_data['förening_id'],
        'rapport': [
            "Föreningen deltog i olika aktiviteter med medlemmar och extern finansiering." if i % 10 != 0 else
            "This is a fake report with inconsistent data and irrelevant information."
            for i in range(100)
        ]
    })

    # Synthetic relationships data
    edges = [(np.random.choice(membership_data['förening_id']),
              np.random.choice(membership_data['förening_id'])) for _ in range(200)]

    # Step 2: Anomaly Detection
    model = IsolationForest(contamination=0.1, random_state=42)
    membership_data['anomaly_score'] = model.fit_predict(membership_data[['medlemmar', 'kostnad']])
    anomalies = membership_data[membership_data['anomaly_score'] == -1]

    # Display anomalies
    st.subheader("Avvikelser i föreningsdata")
    st.write(anomalies)

    # Step 3: NLP Analysis
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(reports['rapport'])
    pca = PCA(n_components=2)
    tfidf_pca = pca.fit_transform(tfidf_matrix.toarray())

    # Step 4: Graph Analysis
    G = nx.Graph()
    G.add_edges_from(edges)

    # Step 5: Visualization
    st.subheader("Visualiseringar")

    # Plot anomaly detection
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    scatter = ax1.scatter(membership_data['medlemmar'], membership_data['kostnad'], 
                           c=membership_data['anomaly_score'], cmap='coolwarm')
    ax1.set_title('Anomaly Detection: Members vs Costs')
    ax1.set_xlabel('Number of Members')
    ax1.set_ylabel('Reported Costs')
    fig1.colorbar(scatter, label='Anomaly Score')
    st.pyplot(fig1)

    # Plot NLP Analysis
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    ax2.scatter(tfidf_pca[:, 0], tfidf_pca[:, 1], c='blue')
    ax2.set_title('Text Analysis of Reports')
    ax2.set_xlabel('PCA Component 1')
    ax2.set_ylabel('PCA Component 2')
    st.pyplot(fig2)

    # Plot relationship analysis
    fig3, ax3 = plt.subplots(figsize=(10, 6))
    nx.draw(G, node_size=50, with_labels=False, ax=ax3)
    ax3.set_title('Relationship Analysis of Associations')
    st.pyplot(fig3)

if __name__ == "__main__":
    st.sidebar.title("Navigering")
    selected_page = st.sidebar.radio("Välj analys", ["Ny Riskanalys"])

    if selected_page == "Ny Riskanalys":
        risk_analysis_app()