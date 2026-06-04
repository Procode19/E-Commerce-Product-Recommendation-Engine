import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from src.data_setup import load_sample_products

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="AI Product Recommendation Engine",
    page_icon="🛍️",
    layout="wide"
)

st.title("🛍️ E-Commerce Product Recommendation Engine")

st.markdown("""
### Smart Product Recommendation System

Paste an Amazon or Flipkart product URL and get similar recommendations using:

✅ TF-IDF Similarity  
✅ Content-Based Filtering  
✅ Product Metadata (Title, Category, Brand)  
""")

st.divider()

# -----------------------------
# LOAD DATA
# -----------------------------
products = load_sample_products()
df = pd.DataFrame(products)

# -----------------------------
# FETCH PRODUCT TITLE
# -----------------------------
def get_product_title(url):
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        title = None

        # Amazon
        amazon_title = soup.find(id="productTitle")
        if amazon_title:
            title = amazon_title.get_text(strip=True)

        # Flipkart
        if not title:
            flipkart_title = soup.find("span", {"class": "VU-ZEz"})
            if flipkart_title:
                title = flipkart_title.get_text(strip=True)

        return title

    except Exception:
        return None

# -----------------------------
# RECOMMENDATION ENGINE
# -----------------------------
def recommend_products(input_title):

    all_titles = df["title"].astype(str).tolist()

    corpus = [input_title] + all_titles

    tfidf = TfidfVectorizer(stop_words="english")
    vectors = tfidf.fit_transform(corpus)

    similarity = cosine_similarity(vectors[0:1], vectors[1:])
    scores = similarity.flatten()

    recommendation_df = df.copy()
    recommendation_df["score"] = scores

    recommendations = recommendation_df.sort_values(
        by="score",
        ascending=False
    ).head(5)

    return recommendations

# -----------------------------
# INPUT URL
# -----------------------------
url = st.text_input("🔗 Paste Product URL (Amazon / Flipkart)")

if st.button("🚀 Get Recommendations"):

    if not url:
        st.warning("Please enter a URL")

    else:
        with st.spinner("Analyzing product..."):
            product_title = get_product_title(url)

        if not product_title:
            st.error("Could not fetch product title")
        else:
            st.success("Product Found!")

            st.subheader("📌 Detected Product")
            st.write(product_title)

            st.divider()

            st.subheader("🎯 Recommended Products")

            recommendations = recommend_products(product_title)

            for _, row in recommendations.iterrows():

                with st.container():
                    col1, col2 = st.columns([1, 4])

                    with col1:
                        st.image(
                            "https://cdn-icons-png.flaticon.com/512/263/263142.png",
                            width=80
                        )

                    with col2:
                        st.markdown(f"### {row['title']}")
                        st.write(f"**Category:** {row['category']}")
                        st.write(f"**Brand:** {row['brand']}")
                        st.write(f"**Price:** ₹{row['price']}")
                        st.write(f"⭐ Rating: {row['rating']}")

                        score = min(float(row["score"]), 1.0)
                        st.progress(score)
                        st.write(f"Similarity Score: {round(score, 2)}")

                st.divider()

# -----------------------------
# DATASET VIEW
# -----------------------------
st.subheader("📦 Product Dataset")
st.dataframe(df)

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("---")
st.markdown("Made with ❤️ using Python + Streamlit")
