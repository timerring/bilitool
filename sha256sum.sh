#!/bin/bash

if [ $# -ne 1 ]; then
    echo "Usage: $0 <directory>"
    exit 1
fi

directory=$1

if [! -d "$directory" ]; then
    echo "Error: Directory $directory does not exist."
    exit 1
fi

files=()

while IFS= read -r -d $'\0' file; do
    files+=("$file")
done < <(find "$directory" -type f -print0)

for file in "${files[@]}"; do
    result=$(shasum -a 256 $file)
    echo "$result" | tee "$file.sha256"
done
