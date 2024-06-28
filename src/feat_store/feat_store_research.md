# Feast: feature store
create_sample_df: create sample of dataframe (because it's faster load to storage) with only necessary columns
```commandline
docker pull cassandra:latest
docker run --name cass_cluster -p 9042:9042 cassandra:latest
docker exec -it cass_cluster cqlsh
```
inside cassandra:
```sql
SHOW HOST;
CREATE KEYSPACE IF NOT EXISTS feast_keyspace
WITH REPLICATION = {
    'class' : 'SimpleStrategy',
    'replication_factor' : 1
    };
DESC KEYSPACES;
```
```commandline
feast init feat_store -t cassandra
cd src/feat_store/feature_repo
feast apply
```
```sql
select * from feast_keyspace.feat_store_tree_data_stats;
select * from feast_keyspace.feat_store_tree_data_stats_fresh;
```
