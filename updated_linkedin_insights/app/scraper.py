def scrape_linkedin_page(page_id: str):
    return {
        "page_id": page_id,
        "name": page_id.capitalize(),
        "url": f"https://www.linkedin.com/company/{page_id}/",
        "description": "LinkedIn company page description",
        "industry": "Technology",
        "followers": 25000,
        "headcount": 120,
        "posts": [
            {
                "content": f"Sample post {i}",
                "comments": [{"text": "Nice post"}]
            }
            for i in range(1, 16)
        ],
        "employees": [
            {"name": "John Doe", "role": "Software Engineer"},
            {"name": "Jane Smith", "role": "Product Manager"}
        ]
    }
