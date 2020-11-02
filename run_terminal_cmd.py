import subprocess

"""
Execute a command prompt from Python
https://geeksforgeeks.org/python-execute-and-parse-linux-commands
"""


def run_cmd(cmd, args):
    data = subprocess.Popen([cmd, args], stdout=subprocess.PIPE)
    my_ip = str(data.communicate())
    my_ip = my_ip.split('\n')
    my_ip = my_ip[0].split('\\')

    res = []
    for line in my_ip:
        res.append(line)
    my_ip = res[0][3:]
    print("local IP is: ", my_ip)


if __name__ == '__main__':
    run_cmd('hostname', '-I')
