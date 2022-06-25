import os
import sys
import subprocess
import inspect
from importlib import import_module

import git

class GitTimeWarp:

    def __init__(self, commit, chdir=False, folder="timewarps", verbose=True):
        self.repo = git.Repo(search_parent_directories=True)
        self.folder = folder
        self.commit = commit
        self.git_dir = f"{self.folder}/commit_{self.commit}"
        self.chdir = chdir
        
        self.old_sys_path = None
        self.old_mods = None
        self.old_cwd = None

        os.makedirs(self.folder, exist_ok=True)
        if not os.path.exists(self.git_dir):
            if verbose:
                print(f"cloning {self.repo.remote().url} to {self.git_dir}")
            proc = subprocess.run(["git", "clone", self.repo.remote().url, self.git_dir], capture_output=True)
            proc.check_returncode()

            old_cwd = os.getcwd()
            try:
                os.chdir(self.git_dir)
                
                if verbose:
                    print(f"checking out {self.commit}")
                proc = subprocess.run(["git", "checkout", self.commit], capture_output=True)
                proc.check_returncode()
            finally:
                os.chdir(old_cwd)

    def __enter__(self):

        self.old_sys_path = sys.path
        sys.path = [ os.path.abspath(self.git_dir) ] + sys.path

        repo_folder = self.repo.git.rev_parse("--show-toplevel")
        self.old_mods = {}
        for key, val in list(sys.modules.items()):
            try:
                if repo_folder in inspect.getfile(val):
                    self.old_mods[key] = val
                    # print(f"Removing imported module {key} ({val})")
                    del sys.modules[key]
            except TypeError:
                pass

        if self.chdir:
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

        self.old_sys_path = None
        self.old_mods = None
        self.old_cwd = None
    
try:
    import wandb

    class WandBTimeWarp(GitTimeWarp):
        
        def __init__(self, project, run_id, **kwargs):
            self.api = wandb.Api()
            self.project = project
            self.run = self.api.run(f"{project}/{run_id}")
            super().__init__(self.run.commit, **kwargs)

except ImportError:
    pass
