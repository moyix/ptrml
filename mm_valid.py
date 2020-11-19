from pandare import Panda, blocking, ffi
panda = Panda(generic="x86_64")
num_ptrs = 0
num_not_ptrs = 0

@blocking
def record_cmd():
  panda.record_cmd("uname -a ; ls /bin ; find /usr/bin", recording_name="valid")
  panda.stop_run()

panda.queue_async(record_cmd)
panda.run()

pos = open('valid_pos.txt','w')
neg = open('valid_neg.txt','w')
@panda.cb_virt_mem_after_write()
def virt_mem_after_write(env, pc, addr, size, buf):
  global num_ptrs
  global num_not_ptrs 
  if size == 8:
    ptr = int(ffi.cast(f"uint64_t[1]", buf)[0])
    try:
      b = panda.virtual_memory_read(env, ptr, 1)
      print ("0x%x" % ptr,file=pos)
      num_ptrs += 1
    except:
      print ("0x%x" % ptr,file=neg)
      num_not_ptrs += 1
    print ("%d ptrs %d not ptrs" % (num_ptrs, num_not_ptrs))
       
panda.enable_memcb()
panda.run_replay("valid")
pos.close()
neg.close()
