from concurrent import futures
import datetime
import json


import pandas as pd
import boto3

BUCKET_NAME = "plow-positions"


def to_dataframe(filepath):
    client = boto3.client("s3")
    response = client.get_object(Bucket=BUCKET_NAME, Key=filepath)
    data = json.loads(response["Body"].read().decode("utf-8"))
    return pd.DataFrame(
        [
            {
                "longitude": row["longitude"],
                "latitude": row["latitude"],
                "timestamp": row["timestamp"],
                "plow_id": row["vehicleName"],
            }
            for plow in data
            for row in plow["statuses"]
        ],
        columns=["longitude", "latitude", "timestamp", "plow_id"],
    )


def main():
    client = boto3.client("s3")
    paginator = client.get_paginator("list_objects_v2")
    response_iterator = paginator.paginate(Bucket=BUCKET_NAME)

    df = pd.DataFrame()
    marker = None
    for response in response_iterator:
        # Process the list of objects in each response
        keys = [obj["Key"] for obj in response.get("Contents", [])]
        with futures.ThreadPoolExecutor(max_workers=10) as executor:
            dfs = [df, *executor.map(to_dataframe, keys)]
            df = pd.concat(dfs)
            df.drop_duplicates(inplace=True)
        latest = datetime.datetime.fromtimestamp(df["timestamp"].max() / 1000)
        print(f"{latest} done - {len(df)} rows total")
        df.to_csv("plow_positions.csv", index=False)


if __name__ == "__main__":
    main()
