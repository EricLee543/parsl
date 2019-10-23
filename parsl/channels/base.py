from abc import ABCMeta, abstractmethod, abstractproperty

from typing import Any, Dict, Optional, Tuple

class Channel(metaclass=ABCMeta):
    """ Define the interface to all channels. Channels are usually called via the execute_wait function.
    For channels that execute remotely, a push_file function allows you to copy over files.

    .. code:: python

                                +------------------
                                |
          cmd, wtime    ------->|  execute_wait
          (ec, stdout, stderr)<-|---+
                                |
          cmd, wtime    ------->|  execute_no_wait
          (ec, stdout, stderr)<-|---+
                                |
          src, dst_dir  ------->|  push_file
             dst_path  <--------|----+
                                |
          dst_script_dir <------|  script_dir
                                |
                                +-------------------

    """

    @abstractmethod
    def execute_wait(self, cmd: str, walltime: int, envs: Dict[str,str] ={}) -> Tuple[int, Optional[str], Optional[str]]:
        ''' Executes the cmd, with a defined walltime.

        Args:
            - cmd (string): Command string to execute over the channel
            - walltime (int) : Timeout in seconds - TODO: or string? check this

        KWargs:
            - envs (Dict[str, str]) : Environment variables to push to the remote side

        Returns:
            - (exit_code, stdout, stderr) (int, optional string, optional string)
              If the exit code is a failure code, the stdout and stderr return values
              may be None.
        '''
        pass

    @abstractproperty
    def script_dir(self) -> str:
        ''' This is a property. Returns the directory assigned for storing all internal scripts such as
        scheduler submit scripts. This is usually where error logs from the scheduler would reside on the
        channel destination side.

        Args:
            - None

        Returns:
            - Channel script dir
        '''
        pass

    # DFK expects to be able to modify this, so it needs to be in the abstract class
    @script_dir.setter
    def script_dir(self, value: str) -> None:
        pass

    @abstractmethod
    def execute_no_wait(self, cmd: str, walltime: int, envs: Dict[str,str] = {}) -> Any:
        ''' Optional. This is infrequently used.

        Args:
            - cmd (string): Command string to execute over the channel
            - walltime (int) : Timeout in seconds

        KWargs:
            - envs (dict) : Environment variables to push to the remote side

        Returns:
            - the type of return value is channel specific
        '''
        pass

    @abstractmethod
    def push_file(self, source: str, dest_dir: str) -> str:
        ''' Channel will take care of moving the file from source to the destination
        directory

        Args:
            source (string) : Full filepath of the file to be moved
            dest_dir (string) : Absolute path of the directory to move to

        Returns:
            destination_path (string)
        '''
        pass

    @abstractmethod
    def close(self) -> bool:
        ''' Closes the channel. Clean out any auth credentials.

        Args:
            None

        Returns:
            Bool

        '''
        pass

    # probable bug here - that mode default should maybe be octal 511?
    @abstractmethod
    def makedirs(self, path: str, mode: int=511, exist_ok: bool=False) -> None:
        """Create a directory.

        If intermediate directories do not exist, they will be created.

        Parameters
        ----------
        path : str
            Path of directory to create.
        mode : int
            Permissions (posix-style) for the newly-created directory.
        exist_ok : bool
            If False, raise an OSError if the target directory already exists.
        """
        pass

    @abstractmethod
    def isdir(self, path: str) -> bool:
        """Return true if the path refers to an existing directory.

        Parameters
        ----------
        path : str
            Path of directory to check.
        """
        pass

    @abstractmethod
    def abspath(self, path: str) -> str:
        """Return the absolute path.

        Parameters
        ----------
        path : str
            Path for which the absolute path will be returned.
        """
        pass
