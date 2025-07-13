# research.py
import sys
import json
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

def get_keyword_ideas(client, customer_id, keywords, location_ids, language_id):
    keyword_plan_idea_service = client.get_service("KeywordPlanIdeaService")

    keyword_seed = client.get_type("KeywordSeed")
    keyword_seed.keywords.extend(keywords)

    request = client.get_type("GenerateKeywordIdeasRequest")
    request.customer_id = customer_id
    request.language = f"languages/{language_id}"
    request.geo_target_constants.extend([f"geoTargetConstants/{loc_id}" for loc_id in location_ids])
    request.keyword_seed = keyword_seed

    try:
        response = keyword_plan_idea_service.generate_keyword_ideas(request=request)
        for idea in response:
            print(f"- {idea.text} | Monthly Searches: {idea.keyword_idea_metrics.avg_monthly_searches} | "
                  f"CPC: {idea.keyword_idea_metrics.average_cpc.micros / 1_000_000:.2f} USD")
    except GoogleAdsException as ex:
        print("Request failed due to GoogleAdsException:", ex)
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python research.py 'keyword1,keyword2,...'")
        sys.exit(1)

    keywords = [kw.strip() for kw in sys.argv[1].split(",")]
    location_ids = ["2840"]  # United States
    language_id = "1000"     # English

    client = GoogleAdsClient.load_from_storage("google-ads.yaml")
    customer_id = client.login_customer_id or client.configuration.login_customer_id

    print(f"🔍 Searching keyword ideas for: {keywords}")
    get_keyword_ideas(client, customer_id, keywords, location_ids, language_id)
