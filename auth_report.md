Звіт\_ПЗ\_8

Тема: Security & Auth — JWT, OAuth2, Roles
Виконавець: Олександр Бабарика

---

1. Мета завдання

- Реалізувати базовий REST API з автентифікацією через JWT.
- Додати авторизацію на основі ролей (RBAC).
- Зрозуміти потік OAuth2 (Authorization Code → Access Token → виклик API).

---

2. Стек технологій

- Мова: Python 3.13
- Фреймворк: Flask
- Бібліотеки: Flask, PyJWT, python-dotenv
- Тестування: curl, Postman
- ОС: Arch Linux

---

3. Реалізація

3.1 Ініціалізація проєкту

- Структура:

```
PPPI/
├── src/
│   ├── app.py                # Головний файл додатку
│   ├── users.py              # База користувачів (in-memory)
│   ├── auth_middleware.py    # Middleware для перевірки JWT
│   └── role_middleware.py    # Middleware для перевірки ролей
├── .env                      # Змінні оточення (створити вручну)
└── README.md
```

- Встановлення залежностей:

```bash
python -m venv .venv
source .venv/bin/activate
pip install Flask PyJWT python-dotenv
```

- Сервер запущено на [http://127.0.0.1:3000](http://127.0.0.1:3000)

3.2 JWT Authentication

- Псевдо-база користувачів:

| id | email                                          | password | role  |
| -- | ---------------------------------------------- | -------- | ----- |
| 1  | [admin@example.com](mailto\:admin@example.com) | admin123 | admin |
| 2  | [user@example.com](mailto\:user@example.com)   | user123  | user  |

- Маршрути:

| Endpoint    | Метод  | Доступ     |
| ----------- | ------ | ---------- |
| /login      | POST   | public     |
| /profile    | GET    | токен JWT  |
| /users/\:id | DELETE | admin only |

- JWT payload:

```json
{
  "sub": "user.id",
  "role": "user.role",
  "exp": "<15 хв>"
}
```

- Middleware:
  - require\_auth — перевірка токена (401 Unauthorized)
  - check\_role(['admin']) — RBAC (403 Forbidden)

3.3 RBAC / ролі

- DELETE `/users/:id` доступний тільки для admin.
- Логи та тестування:

```
# User token
set U_TOKEN (curl -s -X POST http://localhost:3000/login \
-H "Content-Type: application/json" \
-d '{"email":"user@example.com","password":"user123"}' | jq -r .access_token)

# Profile user
curl -H "Authorization: Bearer $U_TOKEN" http://localhost:3000/profile
{
  "role": "user",
  "user_id": "2"
}

# DELETE /users/5 user
curl -i -X DELETE http://localhost:3000/users/5 -H "Authorization: Bearer $U_TOKEN"
HTTP/1.1 403 FORBIDDEN
{
  "error": "Forbidden"
}
```

3.4 OAuth2 (демо)

- Google OAuth2 Playground
- Scope: userinfo.email, userinfo.profile
- Потік: Authorize → Authorization Code → Access Token → API call
- Приклад запиту до Google API:

```
curl -H "Authorization: Bearer <SECRET TOKEN>" \
https://www.googleapis.com/oauth2/v2/userinfo
```

Відповідь:

```json
{
  "id": "110766801840415585346",
  "email": "babaimal2006@gmail.com",
  "verified_email": true,
  "name": "Олександр Бабарика",
  "given_name": "Олександр",
  "family_name": "Бабарика",
  "picture": "https://lh3.googleusercontent.com/a/ACg8ocKG42Uu6vVjdi6G2n7Krgik-MvscVMEWgp0G9iPO8nkt76O8Dhr=s96-c"
}
```

---

4. Результати тестування

| Тест                   | Очікувано      | Фактично       |
| ---------------------- | -------------- | -------------- |
| /login user            | 200 + токен    | 200 + токен    |
| /profile user          | 200 + user\_id | 200 + user\_id |
| DELETE /users/5 user   | 403            | 403            |
| OAuth2 Google API call | 200 + JSON     | 200 + JSON     |

---

5. Висновок

- Реалізовано базовий REST API з JWT authentication.
- Додано RBAC для ролей admin/user.
- Проведено тестування через curl та Postman.
- Продемонстровано роботу OAuth2 Authorization Code flow.



