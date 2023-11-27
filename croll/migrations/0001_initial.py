# Generated by Django 4.1 on 2023-11-27 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TbCroll',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('posttitle', models.TextField(db_column='post_title')),
                ('postingdate', models.TextField(db_column='posting_date', null=True)),
                ('blogurl', models.TextField(db_column='blog_url', null=True)),
                ('createdat', models.DateTimeField(db_column='created_at', null=True)),
                ('updatedat', models.DateTimeField(db_column='updated_at', null=True)),
            ],
            options={
                'db_table': 'TB_CROLL',
                'managed': False,
            },
        ),
    ]
