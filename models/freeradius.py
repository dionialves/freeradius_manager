import pymysql

FREERADIUS_SERVER_HOST = 'localhost'
FREERADIUS_SERVER_USER = 'root'
FREERADIUS_SERVER_PASSWORD = ''
FREERADIUS_SERVER_PORT = '22'

FREERADIUS_DB_USER = 'root'
FREERADIUS_DB_PASSWORD = ''
FREERADIUS_DB_PORT = '22'
FREERADIUS_DB_NAME = 'freeradius'

MIKROTIK_USER = 'admin'
MIKROTIK_PASSWORD = ''


class FreeRadius(object):
    def __init__(self):
        self.connect = self.connect_freeradius()

    @staticmethod
    def connect_freeradius():
        try:
            con = pymysql.connect(FREERADIUS_SERVER_HOST,
                                  FREERADIUS_DB_USER,
                                  FREERADIUS_DB_PASSWORD,
                                  FREERADIUS_DB_NAME)
            c = con.cursor()

            return c
        except ValueError:
            return -1

    def add_user(self, user, password):

        if self.connect != -1:
            sql = "INSERT INTO radcheck (username, attribute, op, value, enable) " \
                  "VALUES ('%s', 'User-Password', ':=', '%s', 'Y')" % (user, password)
            self.connect.execute(sql)

    def update_user(self, user, password):

        if self.connect != -1:
            sql = "UPDATE radcheck SET value='%s', enable='%s' WHERE attribute='User-Password' AND username='%s'" % \
                  (password, 'Y', user)
            self.connect.execute(sql)

    def delete_user(self, user):

        if self.connect != -1:
            sql = "DELETE FROM radcheck WHERE username='%s'" % user
            self.connect.execute(sql)

            sql = "DELETE FROM radreply WHERE username='%s'" % user
            self.connect.execute(sql)

    def delete_pk(self, pk, table):

        if self.connect != -1:
            sql = "DELETE FROM %s WHERE id='%s'" % (table, pk)

            self.connect.execute(sql)

    def add_ip(self, user, ip_address):

        if self.connect != -1:
            sql = "INSERT INTO radreply (username, attribute, op, value) " \
                  "VALUES ('%s', 'Framed-IP-Address', ':=', '%s')" % (user, ip_address)
            self.connect.execute(sql)

    def update_ip(self, user, new_ip):

        if self.connect != -1:
            sql = "UPDATE radreply SET value='%s' WHERE username='%s' AND attribute='Framed-IP-Address'" % (
                new_ip, user)
            self.connect.execute(sql)

    def add_speed_control(self, user, upload, download):

        if self.connect != -1:
            banda = "%sk/%sk" % (upload, download)
            sql = "INSERT INTO radreply (username, attribute, op, value) " \
                  "VALUES ('%s', 'Mikrotik-Rate-Limit', ':=','%s')" % (user, banda)
            self.connect.execute(sql)

    def update_speed_control(self, user, upload, download):

        if self.connect != -1:
            banda = "%sk/%sk" % (upload, download)
            sql = "UPDATE radreply SET value='%s' WHERE username='%s' AND attribute='Mikrotik-Rate-Limit'" % (
                banda, user)
            self.connect.execute(sql)
