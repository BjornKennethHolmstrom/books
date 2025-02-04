#!/bin/bash

# Step 1: Ensure the script runs from the correct directory
BOOK_DIR=$(pwd)
PDF_DIR="$BOOK_DIR/pdfs"
URLS_FILE="$BOOK_DIR/urls.txt"
FINAL_PDF="$BOOK_DIR/Globalize - Natural Steps Toward a Thriving World Government.pdf"
COVER_PDF="$BOOK_DIR/book-cover.pdf"

# Step 2: Start mdbook serve (if not already running)
MDBOOK_PORT=3000
if ! nc -z localhost $MDBOOK_PORT; then
    echo "Starting mdbook serve..."
    mdbook serve --open &
    MDBOOK_PID=$!
    sleep 2  # Wait for mdbook to start
fi

node export_mdbook.js

# Step 5: Merge all PDFs (Cover + Chapters)
echo "Merging PDFs into final book..."
if command -v pdfunite &> /dev/null; then
    pdfunite "$COVER_PDF" "$PDF_DIR"/*.pdf "$FINAL_PDF"
elif command -v pdftk &> /dev/null; then
    pdftk "$COVER_PDF" "$TOC_PDF" "$PDF_DIR"/*.pdf cat output "$FINAL_PDF"
else
    echo "Error: No PDF merging tool found. Install pdfunite or pdftk."
    exit 1
fi

echo "✅ Export complete: $FINAL_PDF"

# Step 6: Stop mdbook server (if started by this script)
if [[ -n "$MDBOOK_PID" ]]; then
    echo "Stopping mdbook server..."
    kill "$MDBOOK_PID"
fi

exit 0

