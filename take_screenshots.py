from playwright.sync_api import sync_playwright

def take_screenshots():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={'width': 1280, 'height': 720})
        
        print("正在访问应用...")
        page.goto('http://localhost:3000')
        page.wait_for_load_state('networkidle')
        
        # 截图1：主界面
        print("截取主界面...")
        page.screenshot(path='/workspace/screenshots/01_main_page.png', full_page=True)
        
        # 截图2：添加任务后的界面
        print("添加测试任务...")
        page.fill('input[placeholder="任务标题"]', '测试任务：完成项目文档')
        page.select_option('select', '工作')
        page.fill('input[placeholder="任务详情（可选）"]', '这是测试任务的详情描述')
        page.click('button:has-text("添加任务")')
        page.wait_for_timeout(1000)
        
        # 截图3：任务列表
        print("截取任务列表...")
        page.screenshot(path='/workspace/screenshots/02_with_task.png', full_page=True)
        
        # 截图4：筛选功能
        print("测试筛选功能...")
        page.click('button:has-text("工作")')
        page.wait_for_timeout(500)
        page.screenshot(path='/workspace/screenshots/03_filter_work.png', full_page=True)
        
        # 截图5：全部任务
        page.click('button:has-text("全部")')
        page.wait_for_timeout(500)
        page.click('button:has-text("未完成")')
        page.wait_for_timeout(500)
        page.screenshot(path='/workspace/screenshots/04_filter_pending.png', full_page=True)
        
        # 截图6：编辑界面
        print("测试编辑功能...")
        page.click('button:has-text("全部")')
        page.wait_for_timeout(500)
        page.click('text=✏️')
        page.wait_for_timeout(500)
        page.screenshot(path='/workspace/screenshots/05_edit_mode.png', full_page=True)
        
        # 取消编辑
        page.click('button:has-text("取消")')
        page.wait_for_timeout(500)
        
        print("所有截图已完成！")
        print("截图保存在 /workspace/screenshots/ 目录")
        
        browser.close()

if __name__ == '__main__':
    take_screenshots()
