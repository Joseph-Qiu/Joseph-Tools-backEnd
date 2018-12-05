# Generated by Django 2.0.4 on 2018-10-16 00:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='blogs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(max_length=100, verbose_name='标题')),
                ('content', models.TextField(max_length=300, verbose_name='内容')),
                ('edit_date', models.DateField(auto_now_add=True, verbose_name='编辑时间')),
            ],
        ),
        migrations.CreateModel(
            name='categories',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='分类名称')),
                ('name_des', models.CharField(max_length=20, verbose_name='分类描述')),
            ],
        ),
        migrations.CreateModel(
            name='comments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=3000, verbose_name='内容')),
                ('edit_date', models.DateField(verbose_name='评论时间')),
            ],
        ),
        migrations.CreateModel(
            name='users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.TextField(max_length=20, verbose_name='用户名')),
                ('user_pwd', models.TextField(max_length=400, verbose_name='密码')),
                ('user_name', models.TextField(max_length=20, verbose_name='昵称')),
                ('head_img', models.CharField(max_length=100, verbose_name='头像')),
            ],
        ),
        migrations.AddField(
            model_name='comments',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.users'),
        ),
        migrations.AddField(
            model_name='blogs',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.categories'),
        ),
        migrations.AddField(
            model_name='blogs',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.users', verbose_name='作者'),
        ),
    ]
