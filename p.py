import datetime
import sys
import asyncio
import platform

if platform.system().lower() == 'windows':
    OS = 'w'
elif platform.system().lower() == 'linux':
    OS = 'l'


def deltatime(func):
    async def wrap(path):
        start = datetime.datetime.now()
        await  func(path)
        print('finish: ', datetime.datetime.now() - start)
    return wrap

async def ping(ip, timeout: int = 1):
    global gc
    proc = await asyncio.create_subprocess_exec('ping', '-n' if OS == 'w' else '-c', str(timeout), '-w', '1', ip,
                                                stdout=asyncio.subprocess.PIPE)
    stdout = await proc.communicate()
    res = str(stdout[0])  # , encoding='GBK')
    with open('result.txt','a') as f:
        gc -= 1
        if res.find('%') != -1 and res.find('100%') == -1:
            f.write(ip + ' True' + '\n')
            return True
        f.write(ip + ' False' + '\n')
        return False

@deltatime
async def main(path):
    global gc
    with open('result.txt', 'w') as f:
        f.write('')
        f.close()
        print('Create file with result')
    with open(path, 'r') as f:
        for k,i in enumerate(f.readlines()):
            while gc >= 1000:
                await asyncio.sleep(2)
            if i[-1] == '\n':
                i = i[0:-1]
            if i.count('.') == 3 or i.count(':') >= 2:
                main_loop.create_task(ping(i))
                gc += 1
    while gc > 0:
        await asyncio.sleep(1)

gc = 0



if __name__ == '__main__':
    try:
        path = sys.argv[1]
        main_loop = asyncio.new_event_loop()
        main_loop.run_until_complete(main(path))
    except IndexError:
        print('Must specify a file')


