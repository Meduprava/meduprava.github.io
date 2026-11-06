#!/usr/bin/env bash
# Выгрузка собранного сайта в бакет Yandex Object Storage.
# Использование: tools/deploy_yc.sh <папка> <бакет> [исключения через пробел]
# Ключ доступа берется из переменных AWS_ACCESS_KEY_ID и AWS_SECRET_ACCESS_KEY (секреты репозитория).
set -euo pipefail
SRC="$1"; BUCKET="$2"; shift 2
EP="--endpoint-url=https://storage.yandexcloud.net"
export AWS_DEFAULT_REGION=ru-central1
EXCL=(--exclude ".git/*" --exclude ".github/*" --exclude "tools/*" --exclude "README.md" --exclude ".nojekyll" --exclude "*.py" --exclude "published.json")
for x in "$@"; do EXCL+=(--exclude "$x"); done

put() { # шаблон, тип, кэш
  # порядок важен: в aws cli побеждает последний фильтр, поэтому исключения идут после --include
  aws s3 sync "$SRC" "s3://$BUCKET" $EP --exclude "*" --include "$1" "${EXCL[@]}" \
    --content-type "$2" --cache-control "$3" --only-show-errors
}
put "*.html" "text/html; charset=utf-8" "max-age=300"
put "*.css"  "text/css; charset=utf-8" "max-age=86400"
put "*.js"   "application/javascript; charset=utf-8" "max-age=86400"
put "*.txt"  "text/plain; charset=utf-8" "max-age=300"
put "*.xml"  "application/xml; charset=utf-8" "max-age=300"
put "*.svg"  "image/svg+xml" "max-age=86400"
# остальное (картинки, шрифты) - тип по расширению; удаление файлов, которых больше нет в репозитории
aws s3 sync "$SRC" "s3://$BUCKET" $EP "${EXCL[@]}" --cache-control "max-age=86400" --delete --only-show-errors
# убрать из бакета то, что попасть в него не должно (если попало раньше)
for x in "$@"; do case "$x" in */\*) aws s3 rm "s3://$BUCKET/${x%\*}" $EP --recursive --only-show-errors || true;; esac; done
echo "Выгружено: $SRC -> $BUCKET"
