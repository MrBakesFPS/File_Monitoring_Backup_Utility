'''
    Tyson Koopman-Baker
    CS-170
    fmb.py

    This utility monitors a list of given file paths from a
    text document in the same directory as this program:

        'monitor_list.txt'

    And backs the files up periodically.
    If the above file does not exist, run fmb.py again.

    Example file types:
    
        Literal: 'C:\\Users\\Name\\documents\\python.txt'
        Relative to program: 'python.txt'

    The original idea came from a file integrity monitor program
    by Jared Medeiros called 'Python FIM' and remastered by
    me, to include a backup add on and updates to the original
    FIM project by Medeiros
'''
import hashlib
import time
from modules import backup
from pathlib import Path

def is_int(data: str) -> bool:
    try:
        int(data)
    except:
        return False
    return True

def calculate_file_hash(file_path: Path) -> str:
    '''
    Returns a file data's hash as a string

    Parameters:
        file_path: The file path being monitored

    Returns:
        The hash string of the file being monitored
    '''
    hash_object = hashlib.sha256()
    hash_object.update(file_path.read_bytes())
    return hash_object.hexdigest()

def snapshot(path: Path) -> dict:
    '''
    Returns a dictionary of hash strings for
    a file, or for every file inside a directory

    Parameters:
        path: The file path being monitored
        
    Returns:
        A dictionary of hash strings to path keys
    '''
    hashes = {}
    if path.is_file():
        hashes[path] = calculate_file_hash(path)
    elif path.is_dir():
        for file_path in path.rglob('*'):
            if file_path.is_file():
                try:
                    hashes[file_path] = calculate_file_hash(file_path)
                except OSError:
                    pass
    return hashes

def log_change(message: str) -> None:
    '''
    Logs any changes to a file or directory
    to a separate log file in a log directory

    Parameters:
        message: The report message for the monitor updates
    '''
    log_directory = Path('log')
    log_directory.mkdir(exist_ok=True)
    log_path = log_directory / 'file_changes.log'
    with log_path.open(mode='a', encoding='utf-8') as log_file:
        log_file.write(f"{time.ctime()}: {message}\n")

def report(message: str) -> None:
    '''
    Reports any changes to the console window
    and to a separate log file

    Parameters:
        message: The report message for monitor updates
    '''
    print(message)
    log_change(message)

def create_backup(src_path: Path) -> None:
    '''
    Creates a backup of a file or directory
    from a give source path

    Parameters:
        src_path: the source path being backed up
    '''
    dest_path = backup.create_dest(src_path)
    backup.try_backup(src_path, dest_path)
    print()

def monitor_files(paths_to_monitor: list, mod_check: int = 5) -> None:
    '''
    Monitors any changes from a list of paths
    and reports them to the console and a log

    Parameters:
        paths_to_monitor: A list of file paths to monitor
        mod_check: The number to check if a backup should initialize
    '''
    previous = {} # Dictionary for previous paths
    first_run = True
    mod_base = 0
    mod_count = 0

    while True:
        current = {} # Dictionary for current paths
        for path in paths_to_monitor:
            if path.exists():
                current.update(snapshot(path))
            else:
                print(f"Path does not exist: {path}")
                
        if mod_count - mod_base >= mod_check:
            mod_base = mod_count

        if first_run:
            print(f"Initial scan: tracking {len(current)} file(s):")
            for path in paths_to_monitor:
                print(path)
            print()
            first_run = False
        else:
            for file_path, h in current.items():
                if file_path not in previous:
                    mod_count = mod_count + 1
                    report(f"File added: {file_path}")
                elif previous[file_path] != h:
                    mod_count = mod_count + 1
                    report(f"File modified: {file_path}")
            for file_path in previous:
                if file_path not in current:
                    mod_count = mod_count + 1
                    report(f"File removed: {file_path}")

        previous = current
        for path in paths_to_monitor:
            if mod_count - mod_base >= mod_check:
                create_backup(path)
        time.sleep(5)

if __name__ == '__main__':
    print("=======================================================")
    print("    File Monitoring Backup Utility -- Tyson Koopman            ")
    print("=======================================================")
    print()
    print("This utility monitors a list of given file paths from a")
    print("text document in the same directory as this program: ")
    print()
    print("\t'monitor_list.txt'")
    print()
    print("And backs the files up periodically.")
    print("If the above file does not exist, run fmb.py again.")
    print()
    print("Example file types:")
    print()
    print("\tLiteral: 'C:\\Users\\Name\\documents\\python.txt'")
    print("\tRelative to program: 'python.txt'")
    print()
    print("=======================================================")
    print()
    print("           Use 'CTRL' + 'C' to stop program!           ")
    print()
    print("=======================================================")
    print()
    paths_to_monitor = []
    monitor_list = Path('monitor_list.txt')
    if monitor_list.exists():
        with monitor_list.open(mode='r', encoding='utf-8') as file:
            for line in file.readlines():
                paths_to_monitor.append(Path(line))
    else:
        monitor_list.touch()

    if len(paths_to_monitor) == 0:
        print("Please add a path per line to the monitor_list.txt file!")
        print()
        user_input = input("Press 'enter' to continue: ")
    else:
        try:
            user_input = input("How many file modifications will be allowed before initiating a backup?: ")
            if not is_int(user_input):
                user_input = input("How many file modifications will be allowed before initiating a backup?: ")
            monitor_files(paths_to_monitor, int(user_input))
        except KeyboardInterrupt:
            print("\nMonitor stopped.")
            print()
            user_input = input("Press 'enter' to continue: ")
        
