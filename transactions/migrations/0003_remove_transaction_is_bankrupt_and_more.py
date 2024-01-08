# Generated by Django 5.0 on 2024-01-07 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0002_transaction_is_bankrupt_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='is_bankrupt',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='transfer_money_id',
        ),
        migrations.AlterField(
            model_name='transaction',
            name='transaction_type',
            field=models.IntegerField(choices=[(1, 'Deposite'), (2, 'Withdrawal'), (3, 'Loan'), (4, 'Loan Paid'), (5, 'Transfer'), (6, 'Received')], null=True),
        ),
    ]