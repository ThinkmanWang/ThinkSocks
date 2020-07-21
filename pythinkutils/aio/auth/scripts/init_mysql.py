# -*- coding: UTF-8 -*-

import sys
import os
import pymysql

from pythinkutils.mysql.ThinkMysql import ThinkMysql
from pythinkutils.common.log import g_logger

def create_table_group():
    conn = ThinkMysql.get_conn_pool().connection()
    try:
        cur = conn.cursor(pymysql.cursors.DictCursor)
        szSql = '''
        DROP TABLE IF EXISTS t_thinkauth_group;
        
        CREATE TABLE t_thinkauth_group (
            `id` bigint(0) UNSIGNED NOT NULL AUTO_INCREMENT
            , `name` varchar(256) NOT NULL 
            , PRIMARY KEY (`id`)
            , `date_added` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP 
            , `description` varchar(256) 
        );
            
        alter table t_thinkauth_group AUTO_INCREMENT=10000001;
        ALTER TABLE `t_thinkauth_group` ADD INDEX `IX_group_name`(`name`) USING BTREE;
        
        insert into t_thinkauth_group(name) VALUES ('admin');
        insert into t_thinkauth_group(name) VALUES ('guest');
        '''

        for statement in szSql.split(';'):
            if len(statement.strip()) > 0:
                cur.execute(statement + ';')

        conn.commit()

    except Exception as e:
        g_logger.error(e)
    finally:
        conn.close()

def create_table_user():
    conn = ThinkMysql.get_conn_pool().connection()
    try:
        cur = conn.cursor(pymysql.cursors.DictCursor)
        szSql = '''
                DROP TABLE IF EXISTS t_thinkauth_user;

                CREATE TABLE t_thinkauth_user (
                    `id` bigint(0) UNSIGNED NOT NULL AUTO_INCREMENT
                    , `username` varchar(256) NOT NULL 
                    , `password` varchar(256) NOT NULL 
                    , `is_superuser` INTEGER NOT NULL DEFAULT 0
                    , `is_active` INTEGER NOT NULL DEFAULT 1
                    , `date_added` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP 
                    , PRIMARY KEY (`id`)
                );

                alter table t_thinkauth_user AUTO_INCREMENT=10000001;
                ALTER TABLE `t_thinkauth_user` ADD INDEX `IX_user_name`(`username`) USING BTREE;
                ALTER TABLE `t_thinkauth_user` ADD INDEX `IX_user_active`(`is_active`) USING BTREE;
                ALTER TABLE `t_thinkauth_user` ADD INDEX `IX_user_date_added`(`date_added`) USING BTREE;

                INSERT INTO t_thinkauth_user(username, password, is_superuser) VALUES ('root', 'Ab123145', 1);
                INSERT INTO t_thinkauth_user(username, password) VALUES ('thinkman', 'Ab123145');
          
                '''

        for statement in szSql.split(';'):
            if len(statement.strip()) > 0:
                cur.execute(statement + ';')

        conn.commit()

    except Exception as e:
        pass
    finally:
        conn.close()

def create_table_user_group():
    conn = ThinkMysql.get_conn_pool().connection()
    try:
        cur = conn.cursor(pymysql.cursors.DictCursor)
        szSql = '''
                    DROP TABLE IF EXISTS t_thinkauth_user_group;

                    CREATE TABLE t_thinkauth_user_group (
                        `id` bigint(0) UNSIGNED NOT NULL AUTO_INCREMENT
                        , `user_id` bigint(0) UNSIGNED NOT NULL 
                        , `group_id` bigint(0) UNSIGNED NOT NULL  
                        
                        , PRIMARY KEY (`id`)
                    );

                    ALTER TABLE `t_thinkauth_user_group` ADD INDEX `IX_user_group_uid`(`user_id`) USING BTREE;
                    ALTER TABLE `t_thinkauth_user_group` ADD INDEX `IX_user_group_gid`(`group_id`) USING BTREE;
                    
                    insert INTO t_thinkauth_user_group(user_id, group_id) VALUES (10000001, 10000001);
                    '''

        for statement in szSql.split(';'):
            if len(statement.strip()) > 0:
                cur.execute(statement + ';')

        conn.commit()

    except Exception as e:
        pass
    finally:
        conn.close()

def create_table_permission():
    conn = ThinkMysql.get_conn_pool().connection()
    try:
        cur = conn.cursor(pymysql.cursors.DictCursor)
        szSql = '''
                        DROP TABLE IF EXISTS t_thinkauth_permission;

                        CREATE TABLE t_thinkauth_permission (
                            `id` bigint(0) UNSIGNED NOT NULL AUTO_INCREMENT
                            , `permission_name` varchar(256) NOT NULL 
                            , `description` varchar(256) 
                            , PRIMARY KEY (`id`)
                        );

                        ALTER TABLE `t_thinkauth_permission` ADD INDEX `IX_permission_name`(`permission_name`) USING BTREE;

                        insert INTO t_thinkauth_permission(permission_name) VALUES 
                            ('permission_add_logentry')
                            , ('permission_change_logentry')
                            , ('permission_delete_logentry')
                            , ('permission_view_logentry')
                            , ('permission_add_permission')
                            , ('permission_change_permission')
                            , ('permission_delete_permission')
                            , ('permission_view_permission')
                            , ('permission_add_group')
                            , ('permission_change_group')
                            , ('permission_delete_group')
                            , ('permission_view_group')
                            , ('permission_add_user')
                            , ('permission_change_user')
                            , ('permission_delete_user')
                            , ('permission_view_user')
                            , ('permission_add_contenttype')
                            , ('permission_change_contenttype')
                            , ('permission_delete_contenttype')
                            , ('permission_view_contenttype')
                            , ('permission_add_session')
                            , ('permission_change_session')
                            , ('permission_delete_session')
                            , ('permission_view_session');
                        '''

        for statement in szSql.split(';'):
            if len(statement.strip()) > 0:
                cur.execute(statement + ';')

        conn.commit()

    except Exception as e:
        pass
    finally:
        conn.close()


def create_table_user_permission():
    conn = ThinkMysql.get_conn_pool().connection()
    try:
        cur = conn.cursor(pymysql.cursors.DictCursor)
        szSql = '''
                    DROP TABLE IF EXISTS t_thinkauth_user_permission;

                    CREATE TABLE t_thinkauth_user_permission (
                        `id` bigint(0) UNSIGNED NOT NULL AUTO_INCREMENT
                        , `user_id` bigint(0) UNSIGNED NOT NULL 
                        , `permission_id` bigint(0) UNSIGNED NOT NULL  

                        , PRIMARY KEY (`id`)
                    );

                    ALTER TABLE `t_thinkauth_user_permission` ADD INDEX `IX_user_permission_uid`(`user_id`) USING BTREE;
                    ALTER TABLE `t_thinkauth_user_permission` ADD INDEX `IX_user_permission_pid`(`permission_id`) USING BTREE;

                    insert INTO t_thinkauth_user_permission(user_id, permission_id) 
                    VALUES 
                    (10000001, 1)
                    , (10000001, 2)
                    , (10000001, 3)
                    , (10000001, 4)
                    , (10000001, 5)
                    , (10000001, 6)
                    , (10000001, 7)
                    , (10000001, 8)
                    , (10000001, 9)
                    , (10000001, 10)
                    , (10000001, 11)
                    , (10000001, 12)
                    , (10000001, 13)
                    , (10000001, 14)
                    , (10000001, 15)
                    , (10000001, 16)
                    , (10000001, 17)
                    , (10000001, 18)
                    , (10000001, 19)
                    , (10000001, 20)
                    , (10000001, 21)
                    , (10000001, 22)
                    , (10000001, 23)
                    , (10000001, 24)
                    ;
                    '''

        for statement in szSql.split(';'):
            if len(statement.strip()) > 0:
                cur.execute(statement + ';')

        conn.commit()

    except Exception as e:
        pass
    finally:
        conn.close()

def create_table_group_permission():
    conn = ThinkMysql.get_conn_pool().connection()
    try:
        cur = conn.cursor(pymysql.cursors.DictCursor)
        szSql = '''
                    DROP TABLE IF EXISTS t_thinkauth_group_permission;

                    CREATE TABLE t_thinkauth_group_permission (
                        `id` bigint(0) UNSIGNED NOT NULL AUTO_INCREMENT
                        , `group_id` bigint(0) UNSIGNED NOT NULL 
                        , `permission_id` bigint(0) UNSIGNED NOT NULL  

                        , PRIMARY KEY (`id`)
                    );

                    ALTER TABLE `t_thinkauth_group_permission` ADD INDEX `IX_group_permission_uid`(`group_id`) USING BTREE;
                    ALTER TABLE `t_thinkauth_group_permission` ADD INDEX `IX_group_permission_pid`(`permission_id`) USING BTREE;

                    insert INTO t_thinkauth_group_permission(group_id, permission_id) 
                    VALUES 
                    (10000001, 1)
                    , (10000001, 2)
                    , (10000001, 3)
                    , (10000001, 4)
                    , (10000001, 5)
                    , (10000001, 6)
                    , (10000001, 7)
                    , (10000001, 8)
                    , (10000001, 9)
                    , (10000001, 10)
                    , (10000001, 11)
                    , (10000001, 12)
                    , (10000001, 13)
                    , (10000001, 14)
                    , (10000001, 15)
                    , (10000001, 16)
                    , (10000001, 17)
                    , (10000001, 18)
                    , (10000001, 19)
                    , (10000001, 20)
                    , (10000001, 21)
                    , (10000001, 22)
                    , (10000001, 23)
                    , (10000001, 24);
                    '''

        for statement in szSql.split(';'):
            if len(statement.strip()) > 0:
                cur.execute(statement + ';')

        conn.commit()

    except Exception as e:
        pass
    finally:
        conn.close()

def create_table_token():
    conn = ThinkMysql.get_conn_pool().connection()
    try:
        cur = conn.cursor(pymysql.cursors.DictCursor)
        szSql = '''
                    DROP TABLE IF EXISTS t_thinkauth_user_token;

                    CREATE TABLE t_thinkauth_user_token (
                        `user_id` bigint(0) UNSIGNED NOT NULL 
                        , `token` varchar(256) NOT NULL  
                        , `date_added` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP 
                        , `date_expire` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP 
                    );

                    ALTER TABLE `t_thinkauth_user_token` ADD INDEX `IX_user_token_uid`(`user_id`) USING BTREE;
                    ALTER TABLE `t_thinkauth_user_token` ADD INDEX `IX_user_token_token`(`token`) USING BTREE;
                    ALTER TABLE `t_thinkauth_user_token` ADD INDEX `IX_user_token_date_add`(`date_added`) USING BTREE;
                    ALTER TABLE `t_thinkauth_user_token` ADD INDEX `IX_user_token_date_expire`(`date_expire`) USING BTREE;

                    insert INTO t_thinkauth_user_token(user_id, token, date_expire) VALUES (10000001, '00000000000000000000000000000000', '2030-12-31 23:59:59');
                    '''

        for statement in szSql.split(';'):
            if len(statement.strip()) > 0:
                cur.execute(statement + ';')

        conn.commit()

    except Exception as e:
        pass
    finally:
        conn.close()

def main():
    create_table_group()
    create_table_user()
    create_table_user_group()
    create_table_permission()
    create_table_user_permission()
    create_table_group_permission()
    create_table_token()

if __name__ == '__main__':
    main()