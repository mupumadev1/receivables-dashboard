# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class AllowedIp(models.Model):
    address = models.CharField(max_length=255)
    authkey = models.TextField(db_column='authKey')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'allowed_ip'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Banklist(models.Model):
    index = models.BigIntegerField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    bankcode = models.TextField(db_column='bankCode', blank=True, null=True)  # Field name made lowercase.
    bankname = models.TextField(db_column='bankName', blank=True, null=True)  # Field name made lowercase.
    biccode = models.TextField(db_column='bicCode', blank=True, null=True)  # Field name made lowercase.
    branchdesc = models.TextField(db_column='branchDesc', blank=True, null=True)  # Field name made lowercase.
    cntrycode = models.TextField(db_column='cntryCode', blank=True, null=True)  # Field name made lowercase.
    sortcode = models.TextField(db_column='sortCode', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'bankList'


class BankTransactions(models.Model):
    tdate = models.CharField(max_length=255)
    customer_no = models.IntegerField()
    name = models.CharField(max_length=100, blank=True, null=True)
    amount = models.FloatField()
    transid = models.CharField(db_column='transId', max_length=100)  # Field name made lowercase.
    account = models.CharField(max_length=255, blank=True, null=True)
    transdate = models.CharField(db_column='transDate', max_length=255)  # Field name made lowercase.
    transremarks = models.CharField(db_column='transRemarks', max_length=255)  # Field name made lowercase.
    currency = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'bank_transactions'


class DepositErrors(models.Model):
    service = models.CharField(max_length=255)
    transactiontype = models.CharField(db_column='transactionType', max_length=255)  # Field name made lowercase.
    status = models.CharField(max_length=255)
    error_list = models.TextField()
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'deposit_errors'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class InvoicesPaid(models.Model):
    invoicecode = models.CharField(db_column='invoiceCode', max_length=255, blank=True, null=True)  # Field name made lowercase.
    clientid = models.CharField(db_column='clientID', max_length=11, blank=True, null=True)  # Field name made lowercase.
    datetime = models.DateTimeField(db_column='dateTime', blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(max_length=255, blank=True, null=True)
    invoicedesc = models.CharField(db_column='invoiceDesc', max_length=255, blank=True, null=True)  # Field name made lowercase.
    amount = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'invoices_paid'


class PaymentTransaction(models.Model):
    destacc = models.CharField(max_length=255)
    amount = models.CharField(max_length=255)
    service = models.CharField(max_length=255)
    remarks = models.CharField(max_length=255)
    referenceno = models.CharField(db_column='referenceNo', max_length=255)  # Field name made lowercase.
    transactiontype = models.CharField(db_column='transactionType', max_length=255)  # Field name made lowercase.
    status = models.CharField(max_length=255)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'payment_transaction'


class ProcessedTransactions(models.Model):
    processed = models.TextField()
    status = models.IntegerField(blank=True, null=True)
    customername = models.CharField(db_column='customerName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    customer_no = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    amount = models.CharField(max_length=255)
    transid = models.CharField(db_column='transId', max_length=255)  # Field name made lowercase.
    transdate = models.CharField(db_column='transDate', max_length=255)  # Field name made lowercase.
    entrydate = models.DateTimeField(db_column='entryDate')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'processed_transactions'
