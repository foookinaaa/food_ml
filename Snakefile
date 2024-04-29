DATASETS = ["base", "research"]

rule all:
    input:
        expand("src/resources/model_{dataset}.bin", dataset=DATASETS)

rule model_fit_base:
    input:
        "src/mlops_ods/dataset/preproc_data_base.csv"
    output:
        "src/resources/model_base.bin"
    script:
        "src/mlops_ods/snakemake_scripts/model_fit.py"

rule model_fit_research:
    input:
        "src/mlops_ods/dataset/preproc_data_research.csv"
    output:
        "src/resources/model_research.bin"
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
