#!/bin/bash


PROJECT_DIR="/home/osboxes/alx/alx-backend-graphql_crm"
LOGFILE="$PROJECT_DIR/crm/cron_jobs/clean_inactive_customers.log"


cd $PROJECT_DIR || exit


if [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
fi


deleted_count=$(python3 manage.py shell -c "
from django.utils import timezone
from crm.models import Customer
from datetime import timedelta

one_year_ago = timezone.now() - timedelta(days=365)
qs = Customer.objects.filter(last_active__lt=one_year_ago)
count = qs.count()
qs.delete()
print(count)
")


echo "[$(date '+%Y-%m-%d %H:%M:%S')] Deleted customers: $deleted_count" >> $LOGFILE
