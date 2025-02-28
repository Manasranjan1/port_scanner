# Python Port Scanner

A multi-threaded port scanner written in Python that allows scanning of single or multiple IP addresses for open ports.

## Features

- Multi-threaded scanning for improved performance
- Support for scanning multiple targets simultaneously
- Service identification for open ports
- IP address validation
- User-friendly colored output
- Configurable port range scanning
- Timeout handling and error management

## Requirements
To run this script, you need the following:

Python 3.x
The socket library, which is usually included with Python by default.

## Usage

1. Run the script:
```bash
python main.py
```
2. When prompted:
   - Enter target IP address(es) - for multiple targets, separate them with commas
   - Enter the number of ports to scan (1-65535)

Example:

```bash
[*] Enter Targets To Scan(split them by ,): 192.168.1.1, 192.168.1.2
[*] Enter How Many Ports You Want To Scan: 1000
```

## Features Explained

- **IP Validation**: Automatically validates IP addresses before scanning
- **Service Detection**: Attempts to identify services running on open ports
- **Multi-threading**: Uses 100 concurrent threads for faster scanning
- **Progress Tracking**: Shows scan duration and number of open ports found
- **Error Handling**: Gracefully handles network errors and invalid inputs

## Output

The scanner provides color-coded output:
- Green: Open ports and their services
- Blue: Scan status messages
- Red: Error messages
- Yellow: Interrupt messages

## Technical Details

- Default timeout: 0.5 seconds per port
- Thread count: 100 concurrent threads
- Supports all ports from 1 to 65535

## Safety Notice

This tool is for educational and authorized testing purposes only. Always ensure you have permission to scan the target systems.


## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Author

Manas Ranjan



