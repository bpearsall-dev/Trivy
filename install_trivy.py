import os
import platform
import subprocess

def download_and_install_trivy():
    os_type = platform.system().lower()
    architecture = platform.machine().lower()

    if os_type == "linux":
        try:
            with open('/etc/os-release') as f:
                os_release_info = f.read().lower()
        except FileNotFoundError:
            print("Unable to determine Linux distribution.")
            return

        if "ubuntu" in os_release_info:
            if "arm" in architecture:
                download_url = "https://github.com/aquasecurity/trivy/releases/download/v0.53.0/trivy_0.53.0_Linux-ARM64.deb"
            else:  # Default to x86_64
                download_url = "https://github.com/aquasecurity/trivy/releases/download/v0.53.0/trivy_0.53.0_Linux-64bit.deb"
            package_type = "deb"
        elif "amazon" in os_release_info:
            if "arm" in architecture:
                download_url = "https://github.com/aquasecurity/trivy/releases/download/v0.53.0/trivy_0.53.0_Linux-ARM64.rpm"
            else:  # Default to x86_64
                download_url = "https://github.com/aquasecurity/trivy/releases/download/v0.53.0/trivy_0.53.0_Linux-64bit.rpm"
            package_type = "rpm"
        else:
            print("Unsupported Linux distribution.")
            return

        # Download package
        package_name = download_url.split('/')[-1]
        try:
            subprocess.run(["wget", download_url, "-O", package_name], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Failed to download the package: {e}")
            return

        # Install package
        try:
            if package_type == "deb":
                subprocess.run(["sudo", "dpkg", "-i", package_name], check=True)
            elif package_type == "rpm":
                subprocess.run(["sudo", "yum", "localinstall", "-y", package_name], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Failed to install the package: {e}")
            return

        # Run Trivy scan
        try:
            subprocess.run(["sudo", "trivy", "filesystem", "/", "--scanners", "vuln", "-q", "--ignore-unfixed"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Failed to run Trivy scan: {e}")
            return

    else:
        print("Unsupported OS type. This script supports only Linux.")
        return

if __name__ == "__main__":
    download_and_install_trivy()