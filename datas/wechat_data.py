import pymysql
import uuid


def get_conn():
    conn = pymysql.connect(
        host='aliyun.yawujia.cn',
        port=3306,
        user='root',
        password='root',
        database='temp_zhichi',
    )
    if conn:
        return conn
    return None


def get_data():
    conn = get_conn()
    user_data = []
    sql = "SELECT * FROM `zc_blacksand_user`"
    cursor = conn.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    user_data += data
    for i in range(1, 6):
        cursor.execute("SELECT * FROM `zc_blacksand_user_{}`".format(i))
        data = cursor.fetchall()
        user_data += data
    count = 0
    fail_num = 0
    html = ""
    sql_str = """"""
    for user in user_data:
        img = user[7]
        try:

            if img:
                img.replace("'", "#").replace("\"", "!")
        except:
            print("error {}".format(img))
            pass
        img = img if img else "http:\\\pic_not_found_" + str(uuid.uuid4()).replace("-", "")
        insert_sql = """
            INSERT INTO `temp_zhichi`.`user`( `account`, `account_alias`, `form_name`,
            `f_account`, `f_account_alias`, `name`, `thumb`, `sex`, `area`, `description`,
             `account_info`, `wechat_user_phone`) VALUES ( '{}', '{}',
              '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}');
            """.format(user[1], user[2], user[3], user[4], user[5], user[6], img, user[8], user[9], user[10], user[11],
                       user[12])
        # print(insert_sql)
        sql_str += insert_sql
        sql_str += "\n"
        div = """
        <div class="perimg">
		<p>所属微信号:{}&nbsp;&nbsp;&nbsp;所属微信id:{}</p>
		<p>备注:{}&nbsp;&nbsp;微信号:{}&nbsp;&nbsp;微信id:{}</p>
		<p>姓名:{}</p>
		<p>性别:{}&nbsp;&nbsp;&nbsp;地区:{}</p>
		<p>微信签名:{}</p>
		<p>所属者手机号:{}</p>
		<p><img src="{}" width="300" height="300"></p>
	</div>
        """.format(user[1], user[2], user[3], user[4], user[5], user[6], user[8], user[9], user[10],
                   user[12], img)
        html += div
        html += "\n"
        # insert_res = cursor.execute(insert_sql)
        # cursor.fetchall()
        # print(insert_res)
        count += 1
        print("left : {}".format(len(user_data) - count))
    with open("sql.sql", 'w', encoding="utf-8") as f:
        f.write(sql_str)
    f.close()
    with open("微信好友.html", 'w', encoding="utf-8") as f:
        front = """
        <!doctype html>
<html lang="zh" data-hairline="true" data-theme="light">
<head>
	<style>
		.perimg{
			text-align: center;
			display: inline-block;
			width:30%;
			margin-bottom:30%;
		}
	</style>
	</head>
	<body>
	
	<div class="image">
        """
        end = """
        </div></body></html>
        """
        f.write(front + html + end)
    f.close()
    print(user_data[0])
    print("fail {}".format(fail_num))


if __name__ == '__main__':
    get_data()
