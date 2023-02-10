import psutil
import requests


def memory_check():
    virt_mem = psutil.virtual_memory()
    swap_mem = psutil.swap_memory()
    print(f'System memory: {virt_mem}')
    if virt_mem.percent > 90:
        memory_alarm("virtual memory")

    print(f'System swap memory: {swap_mem}\n')
    if swap_mem.percent > 90:
        memory_alarm("swap memory")

    for _ in range(100):
        cpu_info = psutil.cpu_percent(interval=1, percpu=True)
        print(f'CPU percent (interval=1, percpu=True): {cpu_info}')
        if max(cpu_info) > 20.0:
            for count, cpu in enumerate(cpu_info):
                if cpu > 20.0:
                    memory_alarm(f"{count + 1} cpu")

        break

    print('Logical CPUs:', psutil.cpu_count())


def memory_alarm(problem_point):
    api_request = requests.post(url="http://127.0.0.1:8080/alarms",
                                json={
                                    'Point': problem_point,
                                    'Status': "Exceeding the critical operating mark"
                                })
    output = api_request.text
    return output


memory_check()
