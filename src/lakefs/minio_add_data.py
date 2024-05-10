from minio import Minio


def main():
    client = Minio(
        "127.0.0.1:9000",
        secure=False,
        access_key="minioadmin",
        secret_key="minioadmin",
    )

    source_file = "../mlops_ods/dataset/2015-street-tree-census-tree-data.csv"

    bucket_name = "mlops-data-bucket"
    destination_file = "2015-street-tree-census-tree-data.csv"

    found = client.bucket_exists(bucket_name)
    if not found:
        client.make_bucket(bucket_name)
        print("Created bucket", bucket_name)
    else:
        print("Bucket", bucket_name, "already exists")

    client.fput_object(
        bucket_name,
        destination_file,
        source_file,
    )
    print(
        source_file,
        "successfully uploaded as object",
        destination_file,
        "to bucket",
        bucket_name,
    )


if __name__ == "__main__":
    main()
