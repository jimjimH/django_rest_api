# Technical exam for backend engineer
## 

### 簡介：
Implement User and Blog APIs by using token authentication on Django and Django_REST_Framework.
***
### 技術：
* python
* django
* django_rest_framework(DRF)
  * serializer
  * validation
  * authentication
  * request, response
* sqlite
* pipenv（建立專案環境）

***
### API：
`除了建立帳號，其餘API皆需驗證Token`  
`於http header帶入`    
`Authorization: Token <user token>`

所有API範例可用postman測試：  
postman連結  
https://www.getpostman.com/collections/4b768b5c0e36fac74333

***
第一部分：User app 和 token authentication

此部分選擇使用django原有user model, 並額外加開一個profile model作為資料補充。
Token authentication 部分使用 DRF的authentication模組

1. 建立帳號（不需驗證Token）（任何人）
```
POST http://127.0.0.1:8000/api/user_profile/create/

JSON_BODY
{
    "username": "hi64852",
    "password": "password123",
    "email": "123@hotmail.com",
    "first_name": "",
    "last_name": "",
    "age": 10,
    "gender": "M",
    "phone": "0919000001"
}
```
2. 更改帳號（身份驗證本人才可以操作）
```
PUT http://127.0.0.1:8000/api/user_profile/75/update/

JSON_BODY
{
    "username":"hi64852_1",
    "password":"password123",
    "email":"123@hotmail.com",
    "first_name":"Huang",
    "last_name":"Jim123",
    "age": 21,
    "gender": "M",
    "phone": "091900000111"
}
```
3. 刪除帳號（身份驗證本人才可以操作）
```
DELETE http://127.0.0.1:8000/api/user_profile/75/delete/
```
4. 取得帳號資訊（任何人）
```
GET http://127.0.0.1:8000/api/user_profile/75/
```
5. 登入帳號後取得身份驗證Token
```
POST http://127.0.0.1:8000/api/user_profile/login/

JSON_BODY
{
    "username": "hi64852_1",
    "password": "password123"
}
```

第二部分：Blog app
1. 建立文章（身份驗證建立屬於本人文章）
```
POST http://127.0.0.1:8000/api/blog/create/

JSON_BODY
{
    "title": "title3",
    "body": "12345",
    "tags": [1,2,3,1,2,4]
}
```
2. 更改文章（身份驗證本人才可以操作）
```
PUT http://127.0.0.1:8000/api/blog/40/update/

JSON_BODY
{
    "title": "ahhahahah",
    "body": "ahhahahah",
    "tags": [
        3,2
    ]
}
```
3. 刪除文章（身份驗證本人才可以操作）
```
DELETE http://127.0.0.1:8000/api/blog/40/delete/
```
4. 取得指定文章資訊（任何人）
```
GET http://127.0.0.1:8000/api/blog/40
```
5. 取得一天之內的文章列表（任何人）
```
GET http://127.0.0.1:8000/api/blog/latest/
```
6. 取得某標籤文章列表（任何人）
```
GET http://127.0.0.1:8000/api/blog/tag/2
```
7. 搜尋包含某文字的主題的文章列表（任何人）
```
GET http://127.0.0.1:8000/api/blog/list/?search=any_word

search可輸入你想尋搜尋的文字，會去尋找文章主題
```

***
### 安裝步驟
1. 安裝python3.7  
   `（略）`
2. 安裝pip3  
   `$ apt-get update`  
   `$ apt-get install python3-pip -y`
3. 安裝pipenv   
   `$ pip3 install pipenv`
4. 先git clone下來  
    `$ git clone https://github.com/jimjimH/django_rest_api.git`
5. cd至想要的目錄後，初始一個虛擬環境   
   `$ pipenv --python 3.7 # 本專案用python3.7`
6. 根據pipfile安裝必要的套件  
   `$ pipenv install --dev`

### 啟用步驟
1. enter pipenv environment  
 `$ pipenv shell`

2. do the table migration  
 `$ python3 manage.py makemigrations`   
 `$ python3 manage.py migrate ` 
3. run server  
`$ python3 manage.py runserver`  
註：sqlite裡面應該有一些資料
4. 刪除專案  
`$pipenv --rm`


