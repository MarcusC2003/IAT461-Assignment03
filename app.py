# Part B — Neighborhood Similarity Explorer

import pandas as pd
import plotly.express as px
import streamlit as st
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

st.set_page_config(page_title="Vancouver Business Licence Neighborhoods", layout="wide")


@st.cache_data
def load_data():
    df = pd.read_csv("licences_clean.csv")
    return df


@st.cache_data
def build_composition_matrix(df, min_count):
    area_counts = df["localarea"].value_counts()
    keep_areas = area_counts[area_counts >= min_count].index

    df_areas = df[df["localarea"].isin(keep_areas)]
    composition = (
        pd.crosstab(df_areas["localarea"], df_areas["businesstype_grouped"], normalize="index") * 100
    )
    centroids = df_areas.groupby("localarea")[["lat", "lon"]].mean()
    return composition, area_counts.reindex(composition.index), centroids.reindex(composition.index)


df = load_data()

# ignores very small neighborhoods 
MIN_BUSINESS_COUNT = 50

st.title("B2 — Interactive Neighborhood Clustering")
st.write(
    "Each neighborhood (`localarea`) is represented by its mix of business types "
    "(% of businesses in that area belonging to each `businesstype_grouped` category). "
    f"Areas with fewer than {MIN_BUSINESS_COUNT} businesses are excluded to avoid noisy percentages."
)

k = st.sidebar.slider("Number of clusters (K)", min_value=2, max_value=10, value=4)

composition, area_counts, centroids = build_composition_matrix(df, MIN_BUSINESS_COUNT)

X_composition = StandardScaler().fit_transform(composition.values)

kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
cluster_labels = kmeans.fit_predict(X_composition)

pca = PCA(n_components=2, random_state=42)
coords = pca.fit_transform(X_composition)

plot_df = pd.DataFrame(
    {
        "localarea": composition.index,
        "pca1": coords[:, 0],
        "pca2": coords[:, 1],
        "cluster": cluster_labels.astype(str),
        "business_count": area_counts.values,
        "lat": centroids["lat"].values,
        "lon": centroids["lon"].values,
    }
)

fig = px.scatter(
    plot_df,
    x="pca1",
    y="pca2",
    color="cluster",
    size="business_count",
    size_max=70,
    hover_name="localarea",
    title=f"Areas in PCA space (K={k})",
)
fig.update_traces(marker=dict(sizemin=8))
fig.update_layout(
    xaxis_title=f"PC1 ({pca.explained_variance_ratio_[0]:.1%} var)",
    yaxis_title=f"PC2 ({pca.explained_variance_ratio_[1]:.1%} var)",
)
st.plotly_chart(fig, width='stretch')

st.subheader("Composition matrix")
st.dataframe(composition.style.background_gradient(cmap="Blues", axis=1).format("{:.1f}"))

st.header("B3 — Geographic view")
map_fig = px.scatter_map(
    plot_df,
    lat="lat",
    lon="lon",
    color="cluster",
    size="business_count",
    size_max=60,
    hover_name="localarea",
    zoom=10,
    height=600,
    title=f"Area centroids colored by cluster (K={k})",
)
map_fig.update_traces(marker=dict(sizemin=8))
map_fig.update_layout(mapbox_style="open-street-map", margin=dict(l=0, r=0, t=40, b=0))
st.plotly_chart(map_fig, width='stretch')

st.header("B4 — Cluster membership")
for c in sorted(plot_df["cluster"].unique(), key=int):
    members = plot_df.loc[plot_df["cluster"] == c, "localarea"].tolist()
    st.write(f"**Cluster {c}** ({len(members)} areas): {', '.join(members)}")

st.subheader("Dominant business types per cluster")
composition_with_cluster = composition.copy()
composition_with_cluster["cluster"] = cluster_labels
cluster_profile = composition_with_cluster.groupby("cluster").mean()
top3_per_cluster = cluster_profile.apply(lambda row: row.nlargest(3).index.tolist(), axis=1)
st.dataframe(top3_per_cluster.rename("top_3_business_types"))
