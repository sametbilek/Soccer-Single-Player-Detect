import subprocess
import sys

def run_script(script_name):
    result = subprocess.run([sys.executable, script_name], capture_output=True, text=True)
    print(f"Running {script_name}...")
    print(f"Output:\n{result.stdout}")
    if result.stderr:
        print(f"Errors:\n{result.stderr}")

if __name__ == "__main__":
    run_script('process/process1/fotodaki4nokta.py')
    run_script('process/process2/videodaki4nokta.py')
    run_script('process/process3/takip_koordi_kayit.py')
    run_script('process/process4/map_of_the_player.py')
    run_script('process/process5/homographic_poses.py')
    run_script('process/process6/speed_data.py')
