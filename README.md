# git-timewarp

Oftentimes it's neccessary to go back to a previous commit. Perhaps you broke sometime and want to see where, or perhaps you want to benchmark an old version of a function. It's easy to `git checkout`, but what if you want to use two different versions of a function _in the same script_? Or use your latest testing/benchmarking code to run your old function? Fear not! `git-timewarp` allows you to temporarily import modules from a specified commit, performing all the git magic under the hood.

Here's how you use it. First, import the `GitTimeWarp` object. And the (current) version of a function you want to test.


```python
from git_timewarp import GitTimeWarp
from test import test_func
```

Let's see the output of the current function


```python
print(test_func())
```

    new function output


Great. But what was the output of that function at an earlier commit? By entering a `GitTimeWarp` object, we can time travel to discover what it was. All in the same script!


```python
with GitTimeWarp("a704acc5f651331645ee5850ff1cda0539cc23df") as tw:
    from test import test_func
    print(test_func())
```

    old function output


Zounds! A ghost has appeared!

How does this work, you ask? The `GitTimeWarp` object simply checks out the old code in the `timewarps/` folder (remember to add to your `.gitignore`!). It then modifies `sys.path` and does some more spicy python magic to ensure all imports in the block will reference the code in this other folder.
