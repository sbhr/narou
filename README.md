# narou

## Git-flow

### init
```
$ git flow init
```

### make Feature branch
```
$ git flow feature start <branch_name>
$ git flow feature publish <branch_name>
$ git flow feature pull origin <branche_name>
```

### リモートのブランチをローカルに持ってくる
```
$ git branch new-branch origin/new-branch
```

## Django

### model
```sh
# マイグレートファイル作成
$ python manage.py makemigrations <application_name>
# SQLの確認
$ python manage.py sqlmigrate <application_name> <number>
# 反映
$ python manage.py migrate
```

#### reference
[Git-flowって何？](http://qiita.com/KosukeSone/items/514dd24828b485c69a05)
