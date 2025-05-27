#!/bin/bash

# Script commit từng file một với message là tên file

# Lấy danh sách các file đã thay đổi (Modified, Added, Untracked)
FILES=$(git status --porcelain | grep '^[ ?MUA]' | cut -c 4-)

for FILE in $FILES
do
    # Lấy tên file (không gồm path)
    BASENAME=$(basename "$FILE")

    # Thêm file vào staging
    git add "$FILE"

    # Commit với message là tên file
    git commit -m "$BASENAME"
done