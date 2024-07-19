OUT_DIRECTORY = "/scratch/dolma/data"

# URLs for cc_en_head
cc_en_head_base_url = "https://huggingface.co/datasets/allenai/dolma/resolve/main/data/common-crawl/cc_en_head/cc_en_head-"
cc_en_head_url_list = [f"{cc_en_head_base_url}{str(i).zfill(4)}.json.gz\n  dir={OUT_DIRECTORY}/cc_en_head\n  out=cc_en_head-{str(i).zfill(4)}.json.gz" for i in range(612)]

# URLs for cc_en_middle
cc_en_middle_base_url = "https://huggingface.co/datasets/allenai/dolma/resolve/main/data/common-crawl/cc_en_middle/cc_en_middle-"
cc_en_middle_url_list = [f"{cc_en_middle_base_url}{str(i).zfill(4)}.json.gz\n  dir={OUT_DIRECTORY}/cc_en_middle\n  out=cc_en_middle-{str(i).zfill(4)}.json.gz" for i in range(777)]

# URLs for cc_en_tail
cc_en_tail_base_url = "https://huggingface.co/datasets/allenai/dolma/resolve/main/data/common-crawl/cc_en_tail/cc_en_tail-"
cc_en_tail_url_list = [f"{cc_en_tail_base_url}{str(i).zfill(4)}.json.gz\n  dir={OUT_DIRECTORY}/cc_en_tail\n  out=cc_en_tail-{str(i).zfill(4)}.json.gz" for i in range(1493)]

# URLs for s2_v3
s2_v3_base_url = "https://huggingface.co/datasets/allenai/dolma/resolve/main/data/peS2o/s2_v3-"
s2_v3_url_list = [f"{s2_v3_base_url}{str(i).zfill(4)}.json.gz\n  dir={OUT_DIRECTORY}/peS2o\n  out=s2_v3-{str(i).zfill(4)}.json.gz" for i in range(42)]

# URLs for The Stack
stack_base_url = "https://huggingface.co/datasets/allenai/dolma/resolve/main/data/stack-code/"
stack_url_list = []
for lang, num_files in sorted(LANG_TO_FILES.items()):
        for i in range(num_files):
                stack_url_list.append(f"{stack_base_url}{lang}/v3-{str(i).zfill(4)}.json.gz\n  dir={OUT_DIRECTORY}/stack-code/{lang}\n  out=v3-{str(i).zfill(4)}.json.gz")

# Combine all URL lists
all_url_list = cc_en_head_url_list + cc_en_middle_url_list + cc_en_tail_url_list + s2_v3_url_list + stack_url_list

out = open("files.txt", "a")
# Print the combined list of URLs
for i, url in enumerate(all_url_list):
    out.write(url + "\n")
                    
