#!/bin/bash

# カレントディレクトリをプロジェクトのルートに変更
cd /path/to/your/django/project

# Gitコマンドで変更を追跡、コミット、プッシュ
git add .
git commit -m "Automated backup: $(date +"%Y-%m-%d %H:%M:%S")"
git push origin master
