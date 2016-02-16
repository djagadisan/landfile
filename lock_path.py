def lock_file(filename, timeout=10, append=False, unlink=True):
    """                                                                                                                                                                                                                                       
    Context manager that acquires a lock on a file.  This will block until                                                                                                                                                                    
    the lock can be acquired, or the timeout time has expired (whichever occurs                                                                                                                                                               
    first).                                                                                                                                                                                                                                   
                                                                                                                                                                                                                                              
    :param filename: file to be locked                                                                                                                                                                                                        
    :param timeout: timeout (in seconds)                                                                                                                                                                                                      
    :param append: True if file should be opened in append mode                                                                                                                                                                               
    :param unlink: True if the file should be unlinked at the end                                                                                                                                                                             
    """
    flags = os.O_CREAT | os.O_RDWR
    if append:
        flags |= os.O_APPEND
        mode = 'a+'
    else:
        mode = 'r+'
    fd = os.open(filename, flags)
    file_obj = os.fdopen(fd, mode)
    try:
        with LockTimeout(timeout, filename):
            while True:
                try:
                    fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                    break
                except IOError as err:
                    if err.errno != errno.EAGAIN:
                        raise
            sleep(0.01)
    yield file_obj
    finally:
        try:
            file_obj.close()
        except UnboundLocalError:
            pass  # may have not actually opened the file                                                                                                                                                                                     
        if unlink:
            os.unlink(filename)

