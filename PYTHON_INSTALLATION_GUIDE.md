# Python Installation Guide - Where to Install

## Important: You Don't Need to "Save" Anything!

The **project is already in the right place:**
- `C:\Users\ADMIN\Documents\ChatSentimentAnalysis-master`

You just need to **install Python** on your computer.

## Where Python Should Be Installed

### Default Installation Location

When you install Python 3.6, it will typically install to:
- **`C:\Python36\`** (if installed for all users)
- **`C:\Users\ADMIN\AppData\Local\Programs\Python\Python36\`** (if installed for current user)

**You don't need to choose a specific location** - the installer will handle it.

## Installation Steps

### Step 1: Download Python 3.6

1. Go to: https://www.python.org/downloads/release/python-360/
2. Download: **Windows x86-64 executable installer**
3. File will be named: `python-3.6.0-amd64.exe` (or similar)

### Step 2: Run the Installer

1. **Double-click the downloaded file**
2. **IMPORTANT:** Check the box **"Add Python 3.6 to PATH"** at the bottom
3. Click **"Install Now"**
4. Wait for installation to complete

### Step 3: Verify Installation

**Close and reopen your terminal/PowerShell**, then run:

```bash
python --version
```

You should see: `Python 3.6.x`

## If Python is Not Found After Installation

### Option 1: Restart Terminal

Close and reopen your PowerShell/Command Prompt. The PATH needs to refresh.

### Option 2: Add Python to PATH Manually

1. Search for "Environment Variables" in Windows
2. Click "Edit the system environment variables"
3. Click "Environment Variables" button
4. Under "System variables", find "Path" and click "Edit"
5. Click "New" and add:
   - `C:\Python36` (or wherever Python installed)
   - `C:\Python36\Scripts`
6. Click "OK" on all windows
7. **Close and reopen your terminal**

### Option 3: Use Full Path

If Python is installed but not in PATH, you can use the full path:

```bash
# Find where Python is installed
C:\Python36\python.exe --version

# Or if in AppData
C:\Users\ADMIN\AppData\Local\Programs\Python\Python36\python.exe --version
```

## After Python is Installed

Once `python --version` works, you can:

1. **Navigate to project directory:**
   ```bash
   cd C:\Users\ADMIN\Documents\ChatSentimentAnalysis-master
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Or run setup script:**
   ```bash
   python setup_project.py
   ```

## Quick Check

Run these commands to check if Python is installed:

```bash
# Check Python version
python --version

# Check pip (Python package installer)
pip --version

# Check where Python is installed
where python
```

## Summary

- **Project location:** Already correct (`C:\Users\ADMIN\Documents\ChatSentimentAnalysis-master`)
- **Python location:** Install to default location (usually `C:\Python36`)
- **Important:** Check "Add Python to PATH" during installation
- **After install:** Close and reopen terminal, then verify with `python --version`

## Need Help?

If Python is still not found after installation:
1. Check if Python is actually installed (look in `C:\Python36` or `C:\Users\ADMIN\AppData\Local\Programs\Python\`)
2. Make sure you checked "Add Python to PATH"
3. Restart your terminal
4. Try adding Python to PATH manually (see Option 2 above)

Let me know if you need help finding where Python installed or adding it to PATH!




