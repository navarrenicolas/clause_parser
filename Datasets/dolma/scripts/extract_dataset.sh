DATA_DIR='./dolma/dolma_sample/'
TEXT_DIR='./dolma/dolma_text/'
ENTRIES_PER_EXTRACTION='1000'

mkdir -p "${TEXT_DIR}"

echo "Extracting text"
for file in "${DATA_DIR}"*; do ./rust/extract_json/target/debug/extract_json -- $file "${TEXT_DIR}" "${ENTRIES_PER_EXTRACTION}"; done


