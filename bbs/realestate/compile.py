import gzip
import json

import boto3


def main():
    client = boto3.client("s3")
    response = client.list_objects_v2(
        Bucket="kjschiroo-realtor-scrape",
        Prefix="real_estate_snapshots/processed/",
        Delimiter="/",
    )
    most_recent = response["CommonPrefixes"][-1]["Prefix"]

    paginator = client.get_paginator("list_objects_v2")
    pages = paginator.paginate(
        Bucket="kjschiroo-realtor-scrape",
        Prefix=most_recent,
    )
    records = []
    for page in pages:
        for obj in page["Contents"]:
            print(obj["Key"])
            response = client.get_object(
                Bucket="kjschiroo-realtor-scrape",
                Key=obj["Key"],
            )
            result = json.loads(
                gzip.decompress(response["Body"].read()).decode("utf-8")
            )
            records.extend(result)
    with open("real_estate_snapshots.json", "w") as f:
        json.dump(records, f)
