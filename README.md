# StayHidden

**StayHidden** is a Python tool that scans websites for hidden HTML elements — like forms, buttons, or inputs hidden using CSS or HTML attributes.

## Features
- Detects elements hidden using:
  - `display:none`
  - `visibility:hidden`
  - `[hidden]` attribute
  - `input[type='hidden']`
- Colorful console output (thanks to `colorama`)
- Progress bar for scanning (`tqdm`)
- Logs all results to `stayhidden_log.txt`

## Requirements

pip install playwright colorama tqdm
python3 -m playwright install

python3 stayhidden.py


Enter any website URL (like `https://example.com`), and StayHidden will show you the number of hidden elements found.

---

##  Example Output

[+] Starting scan for: https://example.com
[*] Scanning page elements...

[✓] Found 2 hidden elements

[1] Hidden Element:
<span style="display:none;">Secret Text</span> 

##  Logs
All results are stored in `stayhidden_log.txt` with timestamps.
