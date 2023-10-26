#!/bin/bash

# カレントディレクトリをプロジェクトのルートに変更
cd /var/www/os3-381-23528.vs.sakura.ne.jp/html/warehouse

# Gitコマンドで変更を追跡、コミット、プッシュ
git add .
git commit -m "Automated backup: $(date +"%Y-%m-%d %H:%M:%S")"
git push origin main -f
