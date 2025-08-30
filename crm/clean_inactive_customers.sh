#!/bin/bash

LOGFILE="/tmp/customer_cleanup_log.txt"
#  shell
deleted_count=$(python3 manage.py shell -c "
from django.utils import timezone
from crm.models import Customer
from datetime import timedelta

one_year_ago = timezone.now() - timedelta(days=365)
qs = Customer.objects.filter(last_order_date__lt=one_year_ago)
count = qs.count()
qs.delete()
print(count)
")

# سجل النتيجة في اللوج مع الوقت
echo \"[\$(date '+%Y-%m-%d %H:%M:%S')] Deleted customers: \$deleted_count\" >> \$LOGFILE
