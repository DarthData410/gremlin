# ---> https://pypi.org/project/mem-edit/
# --- TODO: Currently throwing a 'not found' on mem_edit library

import ctypes
import mem_edit

def loadpid(pid):
    p = mem_edit.Process(pid)
    print(p.get_path())

def listpids():
    pl = mem_edit.Process.list_available_pids()
    for l in pl:
        loadpid(l)

def help_process():  
    help(mem_edit.Process)

def bypid():
    magic_number = ctypes.ulong(1234567890)

    pid = mem_edit.Process.get_pid_by_name('magic.exe')
    with mem_edit.Process.open_process(pid) as p:
        addrs = p.search_all_memory(magic_number)

        # We don't want to edit if there's more than one result...
        assert(len(addrs) == 1)

        # We don't actually have to read the value here, but let's do so anyways...
        num_ulong = p.read_memory(addrs[0], ctypes.c_ulong())
        num = num_ulong.value

        p.write_memory(addrs[0], ctypes.c_ulong(num + 1))

def lookup():
    initial_value = 40
    final_value = 55

    pid = mem_edit.Process.get_pid_by_name('monitor_me.exe')
    with mem_edit.Process.open_process(pid) as p:
        addrs = p.search_all_memory(ctypes.c_int(initial_value))

        input('Press enter when value has changed to ' + str(final_value))

        filtered_addrs = p.search_addresses(addrs, ctypes.c_int(final_value))

        print('Found addresses:')
        for addr in filtered_addrs:
            print(hex(addr))


def modify():
    class MyStruct(ctypes.Structure):
        _fields_ = [
               ('first_member', ctypes.c_ulong),
               ('second_member', ctypes.c_void_p),
               ]

    pid = mem_edit.Process.get_pid_by_name('something.exe')

    with mem_edit.Process.open_process(pid) as p:
        s = MyStruct()
        s.first_member = 1234567890
        s.second_member = 0x1234

        addrs = p.search_all_memory(s)
        print(addrs)

        p.write_memory(0xafbfe0, s)


if __name__ == '__main__':
    listpids()