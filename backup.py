'''
    Tyson Koopman-Baker
    CS-170
    Backup.py

    This utility backs up a file or directory from a given
    literal or relative file path, and creates a backup of
    that file or directory into the same path location
'''
import shutil
from pathlib import Path
from datetime import datetime

def todays_date() -> str:
    '''returns today’s date as YYYY_MM_DD'''
    todayYYYYMMDD = datetime.now().strftime("%Y_%m_%d")
    return todayYYYYMMDD

def current_time() -> str:
    '''returns current time as HH:MM:SS'''
    timeHHMMSS = datetime.now().strftime("%H:%M:%S")
    return timeHHMMSS  

def get_src() -> Path:
    '''
    Retrieves an existing source directory from user

    Returns:
        The full source path provided by user input
    '''
    print()
    user_input = input("Please enter the source path you would like to backup\n> ")
    
    if Path(user_input).is_absolute():
        src_path = Path(user_input)
    else:
        src_path = Path.cwd() / user_input

    while not src_path.exists():
        print()
        user_input = input("Location not found! Please try again! \nPlease enter the source path you would like to backup\n> ")
        if Path(user_input).is_absolute():
            src_path = Path(user_input)
        else:
            src_path = Path.cwd() / user_input
            
    return src_path

def create_dest(src_path: Path) -> Path:
    '''
    Creates a backup destination path based on a given source path

    Parameters:
        src_path: The source path name for the backup

    Returns:
        The destination path of the backup
    '''
    path_ext = 1
    dest_path = src_path.parent / Path(f'{src_path.stem} backup_{todays_date()}{src_path.suffix}')

    while dest_path.exists():
        path_ext = path_ext + 1
        dest_path = src_path.parent / Path(f'{src_path.stem} backup_{todays_date()}_{path_ext}{src_path.suffix}')
        
    return dest_path

def try_backup(src_path: Path, dest_path: Path) -> None:
    '''
    Tries to back up a source path to a destination path
    If failed, ask user to try again or cancel
    If failed 3 times, cancel the backup

    Parameters:
        src_path: The source path of the item(s) being backed up
        dest_path: The destination of the backup item(s)
    '''
    try_backup = True
    failed_attempts = 0
    while try_backup == True:
        try:
            if src_path.is_dir():
                shutil.copytree(src_path, dest_path)
                read_me_path = dest_path / Path('_READ_ME.txt')
            else:
                shutil.copy(src_path, dest_path)
                read_me_path = dest_path.parent / Path(f'{dest_path.stem}_READ_ME.txt')
                
            with read_me_path.open(mode='w', encoding='utf-8') as file:
                file.write(f"Backup created by 'Backup Utility' on {todays_date()} at {current_time()}")
            print()
            with read_me_path.open(mode='r', encoding='utf-8') as file:
                text = file.read()
                print(text)
            try_backup = False
        except:
            failed_attempts = failed_attempts + 1
            user_input = input("Unknown Error Occured... Try again? (Y/N): ").upper()
            while user_input != "Y" and user_input != "N":
                user_input = input("Unknown Error Occured... Try again? (Y/N): ").upper()
                
            if user_input == "N" or failed_attempts > 2:
                try_backup = False
                print()
                print("Backup cancelled")

if __name__ == '__main__':
    print("=======================================================")
    print("            Backup Utility -- Tyson Koopman            ")
    print("=======================================================")
    print()
    print("This utility backs up a file or directory from a given")
    print("literal or relative file path, and creates a backup of")
    print("that file or directory into the same path location")
    print()
    print("\tLiteral: 'C:\\Users\\Name\\documents\\python.txt'")
    print("\tRelative to program: 'python.txt'")
    print()
    print("=======================================================")
    
    src_path = get_src()
    dest_path = create_dest(src_path)

    print()
    print("Backing up " + str(src_path))
    print("        to " + str(dest_path))

    print()
    user_input = input("Continue? (Y/N): ").upper()
    while user_input != "Y" and user_input != "N":
        user_input = input("Continue? (Y/N): ").upper()

    if user_input == "Y":
        try_backup(src_path, dest_path)
    else:
        print()
        print("Backup cancelled")

    print()
    user_input = input("Press enter to continue: ")
    print()
    print("=======================================================")
    print("            Backup Utility -- Tyson Koopman            ")
    print("=======================================================")
    print()
