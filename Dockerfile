# استخدم Python 3.13 (عشان يتطابق مع الـ Pipfile)
FROM python:3.13-slim

# ضبط المتغيرات
ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

# تثبيت pipenv + cron
RUN apt-get update && apt-get install -y --no-install-recommends \
    pipenv \
    cron \
    && rm -rf /var/lib/apt/lists/*

# تحديد فولدر العمل
WORKDIR /app

# نسخ ملفات المشروع
COPY . /app

# تثبيت الـ dependencies بناءً على Pipfile.lock
RUN pipenv install --deploy --ignore-pipfile

# إضافة ملف الكرون (مثلاً customer_cleanup_crontab.txt) للـ cron
COPY customer_cleanup_crontab.txt /etc/cron.d/customer_cleanup

# إعطاء صلاحيات للكرون فايل
RUN chmod 0644 /etc/cron.d/customer_cleanup && \
    crontab /etc/cron.d/customer_cleanup

# تشغيل الكرون مع التطبيق
CMD ["cron", "-f"]
