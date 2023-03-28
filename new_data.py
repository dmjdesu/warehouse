import os
import datetime
import subprocess as cmd

#input values
new_date = datetime.datetime.now().strftime('%Y%m%d')
current_dir = os.getcwd()

#Subprocessで自動化
cp = cmd.run(f"git -C {current_dir} add *", check=True, shell=True)
cp = cmd.run(f"git -C {current_dir} commit -m 'scoresheet updated on {new_date}'", check=True, shell=True)
cp = cmd.run(f"git -C {current_dir} push origin master", check=True, shell=True)
print('Githubへのアップ成功!')
