from multiprocessing import cpu_count
DATASETS = ["base", "research"]

rule all:
    input:
        expand("src/resources/model_{dataset}.bin", dataset=DATASETS),
        expand("src/resources/model_bigger_{dataset}.bin", dataset=DATASETS)
    threads: cpu_count() // 2

rule model_fit_large:
    input:
        "src/mlops_ods/dataset/preproc_data_{dataset}.csv"
    output:
        "src/resources/model_bigger_{dataset}.bin"
    script:
        "src/mlops_ods/snakemake_scripts/model_fit_bigger.py"

rule model_fit:
    input:
        "src/mlops_ods/dataset/preproc_data_{dataset}.csv"
    output:
        "src/resources/model_{dataset}.bin"
    script:
        "src/mlops_ods/snakemake_scripts/model_fit.py"

rule preprocess_data:
    input:
        "src/mlops_ods/dataset/2015-street-tree-census-tree-data.csv"
    output:
        "src/mlops_ods/dataset/preproc_data_base.csv"
    script:
        "src/mlops_ods/snakemake_scripts/preprocess_data_base.py"

rule preprocess_data_research:
    input:
        "src/mlops_ods/dataset/2015-street-tree-census-tree-data.csv"
    output:
        "src/mlops_ods/dataset/preproc_data_research.csv"
    script:
        "src/mlops_ods/snakemake_scripts/preprocess_data_research.py"

rule read_data:
    input:
        "src/mlops_ods/dataset/"
    output:
        "src/mlops_ods/dataset/2015-street-tree-census-tree-data.csv"
    shell:
        """
        if [ ! -f {output} ]; then
            kaggle datasets download -d new-york-city/ny-2015-street-tree-census-tree-data -p {input} --unzip;
        else
            echo "Dataset already exists";
        fi
        """
