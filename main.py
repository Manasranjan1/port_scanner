# Import required libraries
import socket
import termcolor
from socket import gaierror
import sys
import threading
from queue import Queue
import time

def validate_ip(ip):
	"""Validate if the given string is a valid IP address"""
	try:
		socket.inet_aton(ip.strip())
		return True
	except socket.error:
		return False

def scan_port(target, port, open_ports):
	"""
	Attempt to connect to a specific port on the target host
	Args:
		target: IP address to scan
		port: Port number to check
		open_ports: List to store discovered open ports
	"""
	try:
		# Create a new socket object
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.settimeout(0.5)  # Set connection timeout to 0.5 seconds
		result = sock.connect_ex((target, port))
		
		if result == 0:  # Port is open
			try:
				# Try to get the service name for the port
				service = socket.getservbyport(port)
				print(termcolor.colored(f"[+] Port {port} is open - Service: {service}", 'green'))
				open_ports.append(port)
			except:
				# If service name cannot be determined
				print(termcolor.colored(f"[+] Port {port} is open - Service: unknown", 'green'))
				open_ports.append(port)
		sock.close()
			
	except socket.timeout:
		pass  # Ignore timeouts
	except gaierror:
		print(termcolor.colored("[!] Host resolution failed", 'red'))
		sys.exit()
	except Exception as e:
		pass  # Ignore other exceptions

def threader(target, q, open_ports):
	"""
	Worker function for threads that continuously scans ports from the queue
	Args:
		target: IP address to scan
		q: Queue containing ports to scan
		open_ports: Shared list to store discovered open ports
	"""
	while True:
		port = q.get()
		scan_port(target, port, open_ports)
		q.task_done()

def scan(target, ports):
	"""
	Main scanning function that coordinates the port scanning process
	Args:
		target: IP address to scan
		ports: Number of ports to scan (1 to specified number)
	"""
	# Validate IP address before scanning
	if not validate_ip(target):
		print(termcolor.colored(f"[!] Invalid IP address: {target}", 'red'))
		return
		
	print(termcolor.colored(f'\n[*] Starting Scan For {target}', 'blue'))
	
	q = Queue()
	open_ports = []
	
	# Create and start worker threads
	thread_count = 100  # Number of concurrent threads
	for _ in range(thread_count):
		t = threading.Thread(target=threader, args=(target, q, open_ports))
		t.daemon = True
		t.start()
	
	start_time = time.time()
	
	# Add all ports to be scanned to the queue
	for port in range(1, ports + 1):
		q.put(port)
	
	# Wait for all ports to be scanned
	q.join()
	
	# Print scan summary
	duration = time.time() - start_time
	print(termcolor.colored(f"\n[*] Scan completed in {duration:.2f} seconds", 'blue'))
	print(termcolor.colored(f"[*] Found {len(open_ports)} open ports", 'green'))

# Main execution block
try:
	# Get user input for targets and port range
	targets = input("[*] Enter Targets To Scan(split them by ,): ")
	ports = input("[*] Enter How Many Ports You Want To Scan: ")
	
	# Validate port range
	if not ports.isdigit() or int(ports) <= 0 or int(ports) > 65535:
		print(termcolor.colored("[!] Invalid port range. Please enter a number between 1 and 65535", 'red'))
		sys.exit()
		
	ports = int(ports)
	
	# Handle single or multiple targets
	if ',' in targets:
		print(termcolor.colored("[*] Scanning Multiple Targets", 'green'))
		for ip_addr in targets.split(','):
			scan(ip_addr.strip(), ports)
	else:
		scan(targets, ports)
		
except KeyboardInterrupt:
	print(termcolor.colored("\n[!] Scan interrupted by user", 'yellow'))
	sys.exit()
