# Generated by Django 2.0.2 on 2018-05-22 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('teacher_id', models.IntegerField()),
                ('classname', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='kaoqing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('signtime', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='S_class',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Class_id', models.ForeignKey(on_delete=True, to='user.Class')),
            ],
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stasus', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=32)),
                ('pwd', models.CharField(max_length=32)),
                ('realname', models.CharField(max_length=32)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=12)),
                ('user_role', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Yanzheng',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.ImageField(upload_to='')),
                ('time', models.DateField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='s_class',
            name='Student_id',
            field=models.ForeignKey(on_delete=True, to='user.User'),
        ),
        migrations.AddField(
            model_name='kaoqing',
            name='Student_id',
            field=models.ForeignKey(on_delete=True, to='user.User'),
        ),
        migrations.AddField(
            model_name='kaoqing',
            name='class_id',
            field=models.ForeignKey(on_delete=True, to='user.Class'),
        ),
        migrations.AddField(
            model_name='kaoqing',
            name='s',
            field=models.ForeignKey(default=2, on_delete=True, to='user.Status'),
        ),
    ]
