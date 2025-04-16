# Use a Windows base image
FROM mcr.microsoft.com/windows/servercore:ltsc2022

SHELL ["powershell", "-Command"]

# --- Install Chocolatey for easy package management ---
RUN Set-ExecutionPolicy Bypass -Scope Process -Force ; \
    [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072 ; \
    iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))

# --- Install Python ---
RUN choco install -y python --version=3.10.11

# Update PATH
ENV PATH="C:\\Python310;C:\\Python310\\Scripts;${PATH}"

# --- Install ADB and dependencies ---
RUN choco install -y adb

# --- Install pip packages ---
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# --- Copy the project files ---
WORKDIR C:/app
COPY . .

# Set default command
CMD ["python", "main.py"]
