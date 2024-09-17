python -m venv venv

venv/Scripts/Activate.ps1

pip install -r .\requirements.txt

# Define the function and alias

$functionName = "RunTheOffice"
$aliasName = "TheOffice"
$currentPath = (Get-Location)

$functionCode = @"
Function $functionName {
    Set-Location '$currentPath'
    ./venv/Scripts/Activate.ps1
    python .\main.py
    deactivate
}
"@

$aliasCode = "Set-Alias $aliasName $functionName"

# Path to the PowerShell profile
$profilePath = $PROFILE

# Check if the profile exists, if not, create it
if (-not (Test-Path $profilePath)) {
    # Create the directory for the profile if necessary
    $profileDir = Split-Path $profilePath
    if (-not (Test-Path $profileDir)) {
        New-Item -Path $profileDir -ItemType Directory -Force
    }
    
    # Create an empty profile file
    New-Item -Path $profilePath -ItemType File -Force
}

# Append the function to the profile (only if it's not already present)
if (-not (Select-String -Path $profilePath -Pattern $functionName)) {
    Add-Content -Path $profilePath -Value $functionCode
}

# Append the alias to the profile (only if it's not already present)
if (-not (Select-String -Path $profilePath -Pattern "Set-Alias $aliasName")) {
    Add-Content -Path $profilePath -Value $aliasCode
}
