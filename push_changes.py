import subprocess, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

git = r"C:\Program Files\Git\cmd\git.exe"
if not os.path.isfile(git):
    git = "git"

subprocess.run([git, "add", "-A"])
subprocess.run([git, "commit", "-m", "v2.0.1: Ikon, out klasoru fix, antivirus aciklamasi",
                "--author=melih58g <melih58g@users.noreply.github.com>"])
result = subprocess.run([git, "push", "origin", "main"], capture_output=True, text=True)
print("STDOUT:", result.stdout)
print("STDERR:", result.stderr)
print("RC:", result.returncode)
