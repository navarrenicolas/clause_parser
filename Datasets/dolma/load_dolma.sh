DATA_DIR='./dolma_sample/'
PARALLEL_DOWNLOADS='10'
DOLMA_VERSION='v1_6-sample'

git clone git@hf.co:datasets/allenai/dolma

mkdir -p "${DATA_DIR}"

cat "dolma/urls/${DOLMA_VERSION}.txt" | xargs -n 1 -P "${PARALLEL_DOWNLOADS}" wget -q -P "$DATA_DIR"
