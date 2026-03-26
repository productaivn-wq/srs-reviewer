$prompts = @(
    "US-29_prompt.txt",
    "US-33_prompt.txt",
    "US-35_prompt.txt",
    "US-36_prompt.txt"
)

foreach ($prompt in $prompts) {
    $promptName = $prompt.Replace("_prompt.txt", "")
    Write-Host "Running Claude evaluation for $promptName..."
    
    # We ask Claude to just output the pure JSON for the evaluation
    $cmd = "Read srs_docs/ready_prompts/$prompt and strictly follow the system instruction at the top. Output ONLY the raw JSON string of the evaluation. Do not use any markdown formatting or provide any explanation text."
    
    # We pipe the output directly to a file
    $outputFile = "reviews/${promptName}_review.json"
    claude -p $cmd > $outputFile
    
    Write-Host "Saved evaluation for $promptName to $outputFile"
}

Write-Host "All evaluations completed."
