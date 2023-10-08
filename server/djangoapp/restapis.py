import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions
import time

# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))


def get_request(url, **kwargs):
    # If argument contain API KEY
    api_key = kwargs.get("api_key")
    print("GET from {} ".format(url))
    try:
        if api_key:
            params = dict()
            params["text"] = kwargs["text"]
            params["version"] = kwargs["version"]
            params["features"] = kwargs["features"]
            params["return_analyzed_text"] = kwargs["return_analyzed_text"]
            response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
                                    auth=HTTPBasicAuth('apikey', api_key))
        else:
            # Call get method of requests library with URL and parameters
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")

    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)

    return json_data



# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)

def post_request(url, json_payload, **kwargs):
    print(json_payload)
    print("POST from {} ".format(url))
    try:
        response=requests.post(url, params=kwargs, json=json_payload)
    except:
        print("Network exception occurred")
    status_code=response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data


# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list

def get_dealers_from_cf(url, **kwargs):
    results = []
    state = kwargs.get("state")

    if state:
    # Call get_request with a URL parameter
        json_result = get_request(url, state=state)
    else:
        json_result = get_request(url)

    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result
        print("Dealers: " + str(json_result))
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results

def get_dealer_by_id_from_cf(url, dealerId):
    json_result=get_request(url, id=dealerId)
    print(json_result)
    if json_result:
        dealer = json_result[0]
        dealer_obj = CarDealer(
            address=dealer["address"], 
            city=dealer["city"], 
            full_name=dealer["full_name"], 
            id=dealer["id"], 
            lat=dealer["lat"], 
            long=dealer["long"], 
            short_name=dealer["short_name"], 
            st=dealer["st"], 
            zip=dealer["zip"])
        return dealer_obj
    else:
        print('Some error occurred')  
                                  
    

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list

def get_dealer_reviews_from_cf(url, dealerId):
    results = []
    json_result=get_request(url, id=dealerId)
    print(json_result) 
    if json_result:
        reviews = json_result["data"]["docs"]
        for review in reviews:
            if review['purchase']:
                review_obj = DealerReview(
                    dealership=review['dealership'], 
                    purchase=review['purchase'], 
                    purchase_date=review['purchase_date'], 
                    name=review['name'], 
                    review=review['review'], 
                    car_make=review['car_make'], 
                    car_model=review['car_model'], 
                    car_year=review['car_year'], 
                    id=review['id'], 
                    sentiment = 'sentiment')
            else:
                review_obj = DealerReview(
                    dealership=review['dealership'], 
                    purchase=review['purchase'], 
                    purchase_date=None, 
                    name=review['name'], 
                    review=review['review'], 
                    car_make=None, 
                    car_model=None, 
                    car_year=None, 
                    id=review['id'], 
                    sentiment = 'sentiment')
            review_obj.sentiment = analyze_review_sentiments(review_obj.review)
            results.append(review_obj)
            print("Sentiments: ", review_obj.sentiment)
            print("Results: ", results)
    return results  


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative

def analyze_review_sentiments(review):
    url = "https://api.au-syd.natural-language-understanding.watson.cloud.ibm.com/instances/e442f507-38ee-47f7-a5ac-a7bc98bbcbce" 
    api_key = "0_48aqZD1FWKvwR887KGqtKYskzuXCN7yofOfe-kQoSJ" 
    authenticator = IAMAuthenticator(api_key) 
    natural_language_understanding = NaturalLanguageUnderstandingV1(version='2021-08-01',authenticator=authenticator) 
    natural_language_understanding.set_service_url(url) 
    response = natural_language_understanding.analyze(text=review,features=Features(sentiment=SentimentOptions(targets=[review]))).get_result() 
    label=json.dumps(response, indent=2) 
    label = response['sentiment']['document']['label'] 
    return(label) 
    


