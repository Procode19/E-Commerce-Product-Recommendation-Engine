# Recommendation Engine Architecture

## Overview
This project is built as a modular E-Commerce Product Recommendation Engine. The system processes:
- product metadata
- user search, view, cart, and purchase events
- item similarity and category signals

It then generates personalized recommendations with ranking and exploration controls.

## Input
- product list
- item categories
- user purchase history
- search history
- cart items
- product ratings

## Processing
- store product metadata in hash maps
- keep user interaction lists by user id
- compute item co-occurrence from user sessions
- build similarity scores using tags, category, and co-occurrence
- generate candidate sets from recent activity and popular items
- rank candidate items with a scoring function
- apply exploration and cold-start fallback

## Output
- top N recommended products
- similar products for a given item
- category-aware suggestions
- report output for demo and GitHub

## Architecture Diagram
```
User / CLI
   |
   v
[Dataset Loader] -> products, users, interactions
   |
   v
[Recommendation Engine]
   |-- product catalog by id and category
   |-- user history by user id
   |-- item co-occurrence graph
   |-- item similarity map
   |-- popularity counts
   |
   v
[Candidate Generation]
   |-- recent item similarity
   |-- profile-based category items
   |-- popular fallback
   |-- search-based candidates
   |
   v
[Ranking & Output]
   |-- score with personalization + similarity + popularity
   |-- heap-based top N selection
   |-- exploration injection
   |-- report generation
```

## Data Structure Explanation
- Product catalog: dictionary keyed by `item_id`
- Users: dictionary keyed by `user_id`
- Category index: category string -> list of `item_id`
- Popularity counter: item_id -> integer score
- Co-occurrence graph: nested counters for item pairs
- Similarity map: item_id -> candidate_id -> similarity score
- Search profile: word frequency counts per user

## DSA Concepts Used
- HashMap / dictionary for fast lookup
- Arrays / lists for product catalogs and user events
- Sorting for similarity ranking
- Priority queue (`heapq`) to get top recommendations
- Set operations for candidate filtering and cold-start handling
- Graph-style co-occurrence counts for similar products
