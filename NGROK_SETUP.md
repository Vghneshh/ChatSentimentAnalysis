# Public Access via ngrok

Use ngrok to expose the local sentiment server running on port 7860.

## 1. Get Your Authtoken
1. Sign up / log in at https://dashboard.ngrok.com/
2. Navigate to "Getting Started" → copy your authtoken.

## 2. Ensure `ngrok.exe` Exists
Place `ngrok.exe` in the project root (`ChatSentimentAnalysis` directory). If missing, download from https://ngrok.com/download (Windows zip) and extract the executable here.

## 3. Start Your Local Server
You need the server running before starting the tunnel.

```powershell
# From project root
& .\.venv\Scripts\Activate.ps1
python server.py
```

## 4. Apply Authtoken & Launch Tunnel (PowerShell)
```powershell
# Replace YOUR_TOKEN_HERE with the real token
powershell -File .\scripts\setup_ngrok.ps1 -AuthToken "YOUR_TOKEN_HERE" -Port 7860
```

Or run (Batch file / CMD):
```cmd
scripts\setup_ngrok.bat YOUR_TOKEN_HERE 7860
```

## 5. Copy Public URL
After launch, ngrok prints a forwarding URL like:
```
Forwarding                    https://abc123.ngrok-free.app -> http://127.0.0.1:7860
```
Use the HTTPS URL for sharing.

## 6. Verifying
Visit the public URL in a browser; you should see the sentiment UI. Try an example input and confirm it matches local results.

## 7. Common Issues
| Problem | Cause | Fix |
|---------|-------|-----|
| `failed to set authtoken` | Bad or expired token | Re-copy token from dashboard |
| Blank page | Server not running | Start `python server.py` first |
| 502 errors | Server crashed | Check local terminal logs; restart server |
| Tunnel closes immediately | Port blocked | Ensure firewall allows outbound, pick another port (e.g. 8080) |

## 8. Changing Port
If you start the server on a different port (e.g. 8080):
```powershell
python server.py  # modify to listen on 8080 if you change code
powershell -File .\scripts\setup_ngrok.ps1 -AuthToken "YOUR_TOKEN" -Port 8080
```

## 9. Security Notes
- Don’t commit your authtoken. Keep it secret.
- Anyone with the URL can access the UI while tunnel is active.
- Press Ctrl+C in the ngrok window to terminate.

## 10. Troubleshooting Checklist
1. `ngrok.exe` in root? (`dir ngrok.exe`)
2. Server running locally? (visit http://127.0.0.1:7860)
3. Authtoken applied without error?
4. Forwarding URL shows in console?
5. Public URL reachable externally?

If all 5 are yes, you’re live.
