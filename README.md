# 一个从Nyaa磁链到PikPak网盘的搬运工具

这是一个自动化工具,用于将Nyaa上的磁力链接搬运到PikPak网盘。

## 功能特点

- 自动抓取磁力链接（也可以替换成其它网站）
- 将磁力链接添加到PikPak网盘进行下载
- 支持代理设置
- 定期执行任务
- 记录已处理的链接,避免重复添加

## 配置说明

在使用本工具之前,请确保正确配置以下参数:

1. `HTTP_PROXY`: 设置HTTP代理地址 (例如: `"http://your-internal-proxy:PORT"`)
2. `PROCESSED_LINKS_FILE`: 已处理链接的存储文件名 (默认为 `"processed_links.txt"`)
3. PikPak账号信息:
   - `username`: 您的PikPak用户名
   - `password`: 您的PikPak密码
4. `pages_to_scrape`: 要抓取的Nyaa页面数量 (默认为5)
5. 任务执行间隔: 通过修改 `schedule.every(15).minutes.do(run_main_task)` 中的数值来调整 (默认为15分钟)

## 使用方法

1. 确保已安装所有必要的Python库:
   ```
   pip install asyncio httpx requests beautifulsoup4 pikpakapi schedule
   ```

2. 根据您的需求修改配置参数

3. 运行脚本:
   ```
   python nyaa2pikpak.py
   ```

4. 程序将自动运行并定期执行任务

## 注意事项

1. 本工具依赖于第三方服务(Nyaa和PikPak),使用时请遵守相关服务条款。
2. 请确保您的网络环境能够正常访问Nyaa和PikPak。
3. 如果遇到网络问题,程序会等待10分钟后重试。

## 已知问题

1. 程序可能存在异常处理不完善的问题,在网络不稳定时可能会意外退出。
2. 没有对PikPak API的错误响应进行详细处理,可能会在某些情况下遇到未预期的行为。
3. 程序没有实现优雅的退出机制,可能需要手动强制终止。
4. 对于大量磁力链接的情况,可能会触发PikPak的API限制,需要进一步优化请求频率。

请根据实际使用情况对程序进行进一步的测试和优化。
如有任何问题或建议,欢迎提出issue或PR。
