校园博客改进版

运行说明：
1. 解压后进入 campus_blog_improved 文件夹。
2. 安装依赖：pip install -r requirements.txt
3. 首次运行如没有数据库，可执行：flask --app app init-db
4. 启动项目：python app.py

本版本已包含：
- forms.py 表单文件
- 用户头像上传与显示
- 文章发布时间、更新时间
- 未登录点赞按钮禁用
- 页面整体美化
- 密码显示/隐藏

说明：如果你已有旧 data.db，直接放在项目根目录运行即可，程序会自动补充新增字段，不会清空旧数据。
