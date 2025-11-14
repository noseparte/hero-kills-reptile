import requests
import concurrent.futures
import json

# Base URL with placeholder for UID
BASE_URL = "http://10.7.88.185:8080/gameservice/RepairOnline?funcName=testMonopoly&func=mock&targetServer=3000&zoneId=3000&uid={}&activityId=480000&num=300"

# List of UIDs to process - could also read from file
UID_LIST = [
    1749200975400103000,
    1749200975400203000,
    1749200975400303000,
    1749200975400403000,
    1749200975400503000,
    1749200975400603000,
    1749200975400703000,
    1749200975400803000,
    1749200975400903000,
    1749200975401003000,
    1749200975401103000,
    1749200975401203000,
    1749200975401303000,
    1749200975401403000,
    1749200975401503000,
    1749200975401603000,
    1749200975401703000,
    1749200975401803000,
    1749200975401903000,
    1749200975402003000
    # Add more UIDs as needed
]


def make_request(uid):
    """Make HTTP request with specific UID"""
    url = BASE_URL.format(uid)
    try:
        response = requests.get(url)
        print(f"Raw response for UID {uid}: {response.content}")  # Debug print

        # Clean the response
        if response.status_code == 200:
            # Decode bytes to string and clean
            content_str = response.content.decode('utf-8')
            cleaned_content = content_str.replace('s3000=', '').replace('<br>', '')

            try:
                # Parse the JSON if available
                json_data = json.loads(cleaned_content)
                return {
                    'uid': uid,
                    'response': json_data
                }
            except json.JSONDecodeError:
                # If not JSON, return the cleaned string
                return {
                    'uid': uid,
                    'response': cleaned_content
                }

        # Handle non-200 status
        return {
            'uid': uid,
            'error': f"HTTP {response.status_code}",
            'response_content': response.content.decode('utf-8')
        }

    except Exception as e:
        return {
            'uid': uid,
            'error': str(e),
            'exception_type': type(e).__name__
        }

def batch_process():
    """Process UIDs in parallel batches"""
    results = []

    # Using thread pool for parallel requests (adjust max_workers as needed)
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        # Submit all requests
        future_to_uid = {executor.submit(make_request, uid): uid for uid in UID_LIST}

        # Collect results as they complete
        for future in concurrent.futures.as_completed(future_to_uid):
            uid = future_to_uid[future]
            try:
                result = future.result()
                results.append(result)
                print(f"Processed UID {uid} successfully")
            except Exception as e:
                results.append({'uid': uid, 'error': str(e)})
                print(f"Error processing UID {uid}: {str(e)}")

    # Save results to file
    with open('results.json', 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\nCompleted processing {len(results)} UIDs. Results saved to results.json")


if __name__ == "__main__":
    batch_process()