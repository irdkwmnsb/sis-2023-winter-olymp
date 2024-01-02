#!/bin/bash
(cd ../init && python3 init.py)
rm db.sqlite3
python3 manage.py migrate
cp ../init/init_script.py olymp/init_script.py
DJANGO_SETTINGS_MODULE=olymp.settings python3 -m olymp.init_script
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('irdkwmnsb', 'admin@lksh.ru', '^Cx7Okpd4zFC1e#3')" | python manage.py shell