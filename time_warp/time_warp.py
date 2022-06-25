import os
import sys
import shutil
import subprocess
import inspect
from importlib import import_module

import git

class TimeWarp:

    def __init__(self, commit, folder="time_warps"):
        self.repo = git.Repo(search_parent_directories=True)
        self.folder = folder
        self.commit = commit
        self.git_dir = f"{self.folder}/commit_{self.commit}"

        self.old_sys_path = None
        self.old_mods = None
        self.old_cwd = None

        os.makedirs(self.folder, exist_ok=True)
        if not os.path.exists(self.git_dir):
            print(f"cloning {self.repo.remote().url} to {self.git_dir}")
            proc = subprocess.run(["git", "clone", self.repo.remote().url, self.git_dir], capture_output=True)
            proc.check_returncode()

        old_cwd = os.getcwd()        
        os.chdir(self.git_dir)
        print(f"checking out {self.commit}")
        proc = subprocess.run(["git", "checkout", self.commit], capture_output=True)
        proc.check_returncode()
        os.chdir(old_cwd)

    def __enter__(self, chdir=False):

        self.old_sys_path = sys.path
        sys.path = [ os.path.abspath(self.git_dir) ] + sys.path

        self.old_mods = {}
        for key, val in list(sys.modules.items()):
            try:
                if "simplebind" in inspect.getfile(val):
                    old_mods[key] = val
                    del sys.modules[key]
            except TypeError:
                pass

        if chdir:
            self.old_cwd = os.getcwd()
            os.chdir(self.git_dir)
            
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        assert self.old_sys_path is not None and self.old_mods is not None

        if self.old_cwd is not None:
            os.chdir(self.old_cwd)
        sys.path = self.old_sys_path
        for key, val in self.old_mods.items():
            sys.modules[key] = val
    
    def import_module(self, module):
        assert self.old_sys_path is not None and self.old_mods is not None, "A TimeWarp object must be entered before you can start importing modules"
        return import_module(f"{self.folder}.commit_{self.commit}.{module}")
            
