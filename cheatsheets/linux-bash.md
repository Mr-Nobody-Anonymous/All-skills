# 🐧 Linux Systems & Bash Cheatsheet

```bash
# File & Directory Operations
rg -i "search_pattern" src/                 # Fast recursive regex search
fd -e py                                    # Find all python files
tar -czvf archive.tar.gz /path/to/dir       # Compress directory with gzip
chmod 755 script.sh && chown user:group f   # Modify permissions & ownership

# Process & Resource Management
ps aux | grep node                          # List running node processes
top / htop                                  # Interactive process monitor
df -h && du -sh *                           # Disk usage human-readable
free -h                                     # RAM and swap memory usage
kill -9 <PID>                               # Force kill process

# Networking & Diagnostics
ss -tulpn                                   # Active listening ports and sockets
curl -Iv https://api.example.com            # Inspect HTTP headers and TLS cert
ip a / ifconfig                             # Network interfaces and IP addresses
```
