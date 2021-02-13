# LYNX-DIGITAL
---------------------
## Getting the code
1. git clone https://github.com/dbajollari1/lynx.git  //clone repository into local workspace
2. cd lynx // change directory into repository
3. git branch --all  //verify all remote branches were cloned
4. git worktree add ../lynx-<branch> <branch>   // create worktree for branch you want to work in *example: git worktree add ../lynx-Dev Dev*
5. cd ../lynx-<branch>  //change into created worktree

*if running from VS Code, open in"lynx-Dev/lynx" folder (not just lynx-Dev)*

## Pushing your changes
1. cd <your branch folder>
2. git status
3. git add --all
4. git commit -m <"your comments">
5. git push -u origin

## fetching updates from other developers
1. git remote update
2. git status  //check if local repo is behind
3. git pull   //pull remote updates if behind

## Merge from branch to master
1. cd .../lynx     //go to master branch
2. git merge <branch>  //git merge Dev
3. git push
--------------------------
## Run app
1. cd lynx                      //      *lynx-<branch>\lynx*
2. python --version              //         *must be higher then 3.7.3*
3. python -m venv venv              //create environment
4. venv\Scripts\Activate.ps1           // activate environment
5. pip install -r ./requirements.txt   // install packages (copy requirements.txt to root)
6. flask run                           // run application
---



