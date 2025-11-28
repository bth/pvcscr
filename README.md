# pvcscr: Privacy Screen

Adds an overlay window that darkens the screen except for the area around the mouse cursor.

## Download

Get the latest version for **Windows** or **Linux** on https://github.com/bth/pvcscr/releases

No installation required, just download and execute the binary:
* **pvcscr-windows.exe** for Windows
* **pvcscr-linux** for Linux (x86_64)

## Build

1. Clone this repo
```bash
git clone https://github.com/bth/pvcscr.git
cd pvcscr
```
2. Create a virtual env:
```bash
make env
```
3. Activate virtual env:
  * On Linux:
  ```bash
  source .venv/bin/activate
  ```
  * On Windows:
  ```bash
  .venv/bin/activate.bat
  ```
4. Install dependencies:
```bash
make install
```
5. Run the application:
```bash
make run
```
6. Create binary:
```bash
make create-bin
```
