# Auth Workshop — Python Flask JWT & OAuth2

Навчальний проект для демонстрації автентифікації та авторизації у Flask з використанням JWT та RBAC.

## Стек технологій
- **Python 3.x**
- **Flask** — веб-фреймворк
- **PyJWT** — робота з JSON Web Tokens
- **python-dotenv** — управління змінними оточення
- **RBAC** — Role-Based Access Control (ролі: admin/user)

## Структура проекту
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

## Налаштування та запуск

### 1. Створення віртуального оточення
```bash
python -m venv .venv
source .venv/bin/activate  # Для Linux/macOS
# .venv\Scripts\activate   # Для Windows
```

### 2. Встановлення залежностей
```bash
pip install Flask PyJWT python-dotenv
```

### 3. Налаштування .env файлу
Створіть файл `.env` у кореневій папці проекту:
```env
JWT_SECRET=your-super-secret-key-change-me
```

### 4. Запуск сервера
```bash
python src/app.py
```

Сервер запуститься на `http://localhost:3000`

## API Endpoints

### POST /login
Автентифікація користувача та отримання JWT токена.

**Доступні облікові записи:**
- **User:** `user@example.com` / `user123` (роль: user)
- **Admin:** `admin@example.com` / `admin123` (роль: admin)

**Відповідь:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "Bearer",
  "expires_in": 900
}
```

### GET /profile
Отримання профілю поточного користувача (потрібен JWT токен).

### DELETE /users/:id
Видалення користувача (тільки для ролі admin).

## Приклади використання

### 1. Логін як звичайний користувач
```bash
curl -X POST http://localhost:3000/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"user123"}'
```

### 2. Логін як адміністратор
```bash
curl -X POST http://localhost:3000/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"admin123"}'
```

### 3. Отримання профілю без токена (401 Unauthorized)
```bash
curl -i http://localhost:3000/profile
```

### 4. Отримання профілю з токеном
```bash
curl http://localhost:3000/profile \
  -H "Authorization: Bearer <ВАШ_ТОКЕН>"
```

### 5. Спроба видалення як user (403 Forbidden)
```bash
curl -i -X DELETE http://localhost:3000/users/5 \
  -H "Authorization: Bearer <USER_TOKEN>"
```

### 6. Видалення як admin (200 OK)
```bash
curl -X DELETE http://localhost:3000/users/5 \
  -H "Authorization: Bearer <ADMIN_TOKEN>"
```

## OAuth2 Demo (Google)

Демонстрація роботи з OAuth2 через Google OAuth Playground:

1. Відкрити [Google OAuth Playground](https://developers.google.com/oauthplayground/)
2. Вибрати необхідні scopes:
   - `https://www.googleapis.com/auth/userinfo.email`
   - `https://www.googleapis.com/auth/userinfo.profile`
3. Натиснути **Authorize APIs** → отримати authorization code
4. **Exchange authorization code for tokens** → отримати access token
5. Використати токен для отримання даних користувача:
   ```bash
   curl -H "Authorization: Bearer <GOOGLE_ACCESS_TOKEN>" \
     https://www.googleapis.com/oauth2/v2/userinfo
   ```

## Безпека

⚠️ **ВАЖЛИВО:** Це навчальний проект!

- Паролі зберігаються у відкритому вигляді (у production використовуйте bcrypt/argon2)
- JWT secret має бути складним та унікальним
- Користувачі зберігаються в пам'яті (у production використовуйте базу даних)
- Не використовуйте цей код у production без належних змін безпеки!

## Особливості реалізації

- **JWT токени** мають термін дії 15 хвилин (expires_in: 900 секунд)
- **Декоратори middleware** для автентифікації та авторизації
- **RBAC** — перевірка ролей через декоратор `@check_role()`
- **Debug логи** для відстеження помилок JWT (див. консоль сервера)

