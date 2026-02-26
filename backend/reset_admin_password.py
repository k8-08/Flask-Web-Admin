import sys
sys.path.insert(0, '.')
from app.utils.security import hash_password
import sqlalchemy as sa

# 使用同步连接字符串
SYNC_URI = "mysql+pymysql://root:1234@localhost:3306/fastapiwebadmin?charset=utf8mb4"

engine = sa.create_engine(SYNC_URI)
new_hash = hash_password('admin123456')
print('新 hash:', new_hash)
with engine.connect() as conn:
    result = conn.execute(
        sa.text("UPDATE sys_user SET password=:pwd WHERE username='admin'"),
        {'pwd': new_hash}
    )
    conn.commit()
    print('更新行数:', result.rowcount)
print('密码重置成功！admin 密码已设置为 admin123456')
