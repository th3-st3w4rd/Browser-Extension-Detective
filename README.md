# Browser Extension Dextective (BED)

Blue Team utility used to find local browser extension IDs on a local PC.  It will only search for the current user that you are signed in with.  There is an option to search for the extesnions online, internet connection needed, or to continue in Offline mode.

Online mode returns extesnion ID #s and the extensions' names (if found).

Offline mode returns only the extension ID #s with "n/a" as the value.

## Supported OS

- Windows 11 Pro

## Supported Browser Extensions

- Chrome

## Future Goals

- [x] Include support to run on Windows.
- [ ] Include support to run on Mac.
- [ ] Include support to run on Linux.
- [ ] Include support to search for Safari extensions.
- [ ] Include support to search for Fire Fox extensions.
- [ ] Include support to search for Edge extensions.
- [x] Add function to search the current users of the current device.
- [x] Add command switch to search all users of the current device.
- [ ] Add command switch to point to a particular drive or mount point.

## Usage
usage: main.py [-h] [-i] [-a] [-c]  
options:  
  -h, --help       show this help message and exit  
  -i, --internet   Searches the internet for extension stores.  
  -a, --all-users  Searches all potential accounts on target.  
  -c, --chrome     Searches locally for Google Chrome extensions.  
