#!/usr/bin/env bash
set -euo pipefail

# Создание нового ключа подписи Release APK прямо в GitHub Codespaces.
# Ключ и пароли НЕ записываются в Git-репозиторий.
# Скрипт использует JDK keytool и GitHub CLI (gh), доступные в Codespaces.

REPO="$(gh repo view --json nameWithOwner --jq .nameWithOwner)"
KEYSTORE="release.keystore"
ALIAS="chronicles-release"

if ! command -v keytool >/dev/null 2>&1; then
  echo "ОШИБКА: keytool не найден. В Codespaces должен быть установлен JDK."
  exit 1
fi

if ! command -v gh >/dev/null 2>&1; then
  echo "ОШИБКА: GitHub CLI (gh) не найден."
  exit 1
fi

if ! command -v openssl >/dev/null 2>&1; then
  echo "ОШИБКА: openssl не найден."
  exit 1
fi

if ! gh auth status >/dev/null 2>&1; then
  echo "ОШИБКА: GitHub CLI не авторизован в Codespaces."
  exit 1
fi

if [ -e "$KEYSTORE" ]; then
  echo "ОШИБКА: $KEYSTORE уже существует в Codespaces."
  echo "Если нужен новый ключ, удалите старый локальный файл и запустите скрипт снова."
  exit 1
fi

# Случайный пароль: одинаковый для keystore и ключа.
# Пароль не выводится в консоль.
STORE_PASS="$(openssl rand -hex 32)"
KEY_PASS="$STORE_PASS"

keytool -genkeypair \
  -keystore "$KEYSTORE" \
  -storetype PKCS12 \
  -storepass "$STORE_PASS" \
  -keypass "$KEY_PASS" \
  -alias "$ALIAS" \
  -keyalg RSA \
  -keysize 4096 \
  -validity 10000 \
  -dname "CN=Chronicles of the Abyss, OU=Indie, O=Chronicles of the Abyss, C=DE"

KEYSTORE_BASE64="$(base64 -w 0 "$KEYSTORE")"

# Секреты передаются непосредственно GitHub CLI и не коммитятся в репозиторий.
printf '%s' "$KEYSTORE_BASE64" | gh secret set ANDROID_KEYSTORE_BASE64 --repo "$REPO"
printf '%s' "$STORE_PASS" | gh secret set ANDROID_KEYSTORE_PASSWORD --repo "$REPO"
printf '%s' "$ALIAS" | gh secret set ANDROID_KEY_ALIAS --repo "$REPO"
printf '%s' "$KEY_PASS" | gh secret set ANDROID_KEY_PASSWORD --repo "$REPO"

chmod 600 "$KEYSTORE"
unset KEYSTORE_BASE64 STORE_PASS KEY_PASS

echo
echo "ГОТОВО."
echo "Репозиторий: $REPO"
echo "Alias: $ALIAS"
echo "Все 4 GitHub Secrets установлены."
echo "Keystore: $KEYSTORE (только локально в Codespaces, не коммитить)"
echo
echo "Теперь запустите GitHub Actions workflow: Build Release APK."
