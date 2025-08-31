#!/bin/bash

LOGFILE="/tmp/customer_cleanup_log.txt"
PROJECT_DIR="/home/osboxes/alx/alx-backend-graphql_crm"

deleted_count=$(python3 $PROJECT_DIR/manage.py shell -c "
from django.utils import timezone
from crm.models import Customer
from datetime import timedelta

one_year_ago = timezone.now() - timedelta(days=365)
qs = Customer.objects.filter(last_order_date__lt=one_year_ago)
count = qs.count()
qs.delete()
print(count)
")
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Deleted customers: $deleted_count" >> $LOGFILE
