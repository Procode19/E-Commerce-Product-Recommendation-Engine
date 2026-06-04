from pathlib import Path
from src.data_setup import create_sample_interactions, load_sample_products, load_sample_users
from src.recommender import RecommendationEngine


def main():
    engine = RecommendationEngine()
    products = load_sample_products()
    users = load_sample_users()
    interactions = create_sample_interactions(products, users)

    engine.load_products(products)
    engine.load_users(users)
    engine.load_interactions(interactions)

    print("\nE-Commerce Product Recommendation Engine")
    print("=======================================")
    while True:
        print("\nMenu:")
        print("1. Show product catalog")
        print("2. Show sample user summary")
        print("3. Get recommendations for a user")
        print("4. Save recommendation report")
        print("5. Exit")
        choice = input("Choose an option (1-5): ").strip()

        if choice == "1":
            print(engine.print_product_catalog())
        elif choice == "2":
            user_id = input("Enter user id (e.g. U001): ").strip() or "U001"
            print(engine.print_user_summary(user_id))
        elif choice == "3":
            user_id = input("Enter user id (e.g. U001): ").strip() or "U001"
            recent_item = input("Enter recent item id (optional, e.g. P002): ").strip() or None
            k = int(input("Top N recommendations (default 5): ").strip() or "5")
            explore = float(input("Exploration probability 0.0-0.5 (default 0.1): ").strip() or "0.1")
            recommendations = engine.recommend(user_id=user_id, k=k, recent_item=recent_item, explore=explore)
            print(f"\nTop {k} recommendations for {user_id}:")
            for rank, item in enumerate(recommendations, start=1):
                product = engine.products[item["item_id"]]
                print(
                    f"{rank}. {product.title} ({product.item_id}) | category={product.category} | brand={product.brand} | price=${product.price:.2f} | score={item['score']:.2f}"
                )
        elif choice == "4":
            user_id = input("Enter user id to save report (e.g. U001): ").strip() or "U001"
            recent_item = input("Enter recent item id (optional): ").strip() or None
            k = int(input("Top N recommendations in report (default 10): ").strip() or "10")
            explore = float(input("Exploration probability 0.0-0.5 (default 0.1): ").strip() or "0.1")
            report_text = engine.generate_report(user_id=user_id, recent_item=recent_item, k=k, explore=explore)
            report_path = Path("outputs") / f"recommendation_report_{user_id}.txt"
            report_path.write_text(report_text, encoding="utf-8")
            print(f"Saved recommendation report to {report_path}")
        elif choice == "5":
            print("Exiting the recommendation engine demo. Goodbye!")
            break
        else:
            print("Invalid selection. Please choose 1-5.")


if __name__ == "__main__":
    main()
