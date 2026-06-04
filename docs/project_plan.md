# Project Implementation Plan

## Phase 1: Setup
- create repository folders and main Python files
- install Python 3.9+
- confirm the project runs with `python main.py`
- Expected output: CLI menu prints successfully
- Common mistakes: using unavailable package imports or wrong relative imports

## Phase 2: Product dataset creation
- add sample product metadata in `data/sample_products.json`
- include fields `item_id`, `title`, `category`, `brand`, `price`, `tags`, `rating`
- Expected output: product catalog loads and prints correctly
- Common mistakes: inconsistent item ids or missing categories

## Phase 3: User interaction data creation
- define sample users in `data/sample_users.json`
- generate interaction events: `search`, `view`, `add_cart`, `purchase`
- Expected output: engine builds user histories and popularity counts
- Common mistakes: using event types not handled by the engine

## Phase 4: HashMap-based data storage
- load products into dictionaries keyed by `item_id`
- store categories in a separate hashmap
- store users in a hashmap keyed by `user_id`
- Expected output: constant-time lookup for product and user information
- Common mistakes: nested loops instead of maps for lookups

## Phase 5: Similarity score calculation
- compute item-item co-occurrence from user sessions
- calculate tag and category similarity for each product pair
- Expected output: similar item list for a chosen item
- Common mistakes: forgetting to ignore self-similarity

## Phase 6: Sorting/ranking products
- rank candidates by a computed score
- use sort or `heapq.nlargest` to keep top N results
- Expected output: top recommendations ordered by score
- Common mistakes: not filtering out already purchased items correctly

## Phase 7: Priority queue for top recommendations
- use `heapq.nlargest` to select the top-K recommendation candidates
- Expected output: efficient ranking even with many candidates
- Common mistakes: scanning too many low-quality items without pruning

## Phase 8: Recommendation output generation
- build the final recommendation response
- add cold-start fallback and exploration control
- Expected output: stable recommendations plus occasional exploratory items
- Common mistakes: repeated or empty candidate lists

## Phase 9: Report generation
- write recommendation reports to `outputs/recommendation_report_{user_id}.txt`
- include summary, top categories, and top N items
- Expected output: human-readable report file saved to disk
- Common mistakes: forgetting to create the `outputs` folder or write permissions

## Phase 10: GitHub upload
- commit code and documentation
- add README, docs, and sample data
- push to GitHub with descriptive commit messages
- Expected output: clean repo with a clear project portfolio
- Common mistakes: committing generated binary files or temporary files
