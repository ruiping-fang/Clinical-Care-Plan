# 🐛 调试指南 - Clinical Care Plan

## 📋 目录
1. [VSCode 调试器（推荐）](#方法-1-vscode-调试器推荐)
2. [Postman 测试接口](#方法-2-postman-测试接口)
3. [Python 日志调试](#方法-3-python-日志调试)

---

## 方法 1: VSCode 调试器（推荐）

### 🎯 调试点位置（已标记 🔴）

| 断点位置 | 文件:行号 | 作用 |
|---------|----------|------|
| BREAKPOINT 1 | [views.py:21](app/views.py#L21) | 请求进入，查看 request 对象 |
| BREAKPOINT 2 | [views.py:24](app/views.py#L24) | 查看解析后的 JSON 参数 |
| BREAKPOINT 3 | [views.py:30](app/views.py#L30) | 查看生成的 prompt 内容 |
| BREAKPOINT 4 | [views.py:45](app/views.py#L45) | OpenAI API 调用前 |
| BREAKPOINT 5 | [views.py:54](app/views.py#L54) | API 返回后，查看 response |
| BREAKPOINT 6 | [views.py:57](app/views.py#L57) | 数据存储前 |
| BREAKPOINT 7 | [views.py:63](app/views.py#L63) | 最终响应前 |

### 📝 操作步骤

#### Step 1: 安装 Python 调试扩展
1. 打开 VSCode
2. 按 `Cmd+Shift+X` 打开扩展商店
3. 搜索 "Python" 或 "Debugpy"
4. 安装 Microsoft 官方的 Python 扩展

#### Step 2: 设置断点
1. 打开 [app/views.py](app/views.py)
2. 找到标记 🔴 的位置
3. 点击行号左侧，会出现红色圆点（断点）
4. 推荐设置的断点：
   - 第 21 行：请求入口
   - 第 24 行：参数解析后
   - 第 45 行：API 调用前
   - 第 54 行：API 调用后

#### Step 3: 启动调试
1. 按 `F5` 或点击左侧 "Run and Debug" 图标
2. 选择 "Django: Debug Server"
3. 等待服务启动，看到：
   ```
   Starting development server at http://0.0.0.0:8000/
   ```

#### Step 4: 发送请求触发断点
打开浏览器访问 `http://localhost:8000`，填写表单并提交，或使用 Postman（见下方）

#### Step 5: 调试操作
- **继续执行**: `F5`
- **单步跳过**: `F10`
- **单步进入**: `F11`
- **单步跳出**: `Shift+F11`
- **停止调试**: `Shift+F5`

#### Step 6: 查看变量
- 左侧 "Variables" 面板查看所有局部变量
- 鼠标悬停在变量上查看值
- 在 "Debug Console" 输入变量名查看详情

---

## 方法 2: Postman 测试接口

### 📥 安装 Postman
1. 访问 https://www.postman.com/downloads/
2. 下载 Mac 版本并安装
3. 打开 Postman（可以跳过登录）

### 🚀 配置请求

#### 创建新请求
1. 点击 "New" → "HTTP Request"
2. 配置如下：

**基本信息：**
- **Method**: POST
- **URL**: `http://localhost:8000/generate/`

**Headers 设置：**
点击 "Headers" 标签，添加：
```
Content-Type: application/json
```

**Body 设置：**
1. 点击 "Body" 标签
2. 选择 "raw"
3. 右侧下拉选择 "JSON"
4. 输入测试数据：

```json
{
  "name": "张三",
  "diagnosis": "2型糖尿病",
  "medication": "二甲双胍 500mg bid",
  "history": "高血压病史5年"
}
```

#### 发送请求
1. 确保 Django 服务正在运行：
   ```bash
   python manage.py runserver
   ```
2. 点击 Postman 中的 "Send" 按钮
3. 查看下方 Response 区域的返回结果

### 📦 保存 Postman Collection
我已经为你准备了一个 Collection，可以导入使用：

**Collection JSON** (保存为 `Clinical-Care-Plan.postman_collection.json`)：
```json
{
  "info": {
    "name": "Clinical Care Plan API",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Generate Care Plan",
      "request": {
        "method": "POST",
        "header": [
          {
            "key": "Content-Type",
            "value": "application/json"
          }
        ],
        "body": {
          "mode": "raw",
          "raw": "{\n  \"name\": \"张三\",\n  \"diagnosis\": \"2型糖尿病\",\n  \"medication\": \"二甲双胍 500mg bid\",\n  \"history\": \"高血压病史5年\"\n}"
        },
        "url": {
          "raw": "http://localhost:8000/generate/",
          "protocol": "http",
          "host": ["localhost"],
          "port": "8000",
          "path": ["generate", ""]
        }
      }
    }
  ]
}
```

**导入方法：**
1. Postman → Import → 选择上述 JSON 文件
2. 直接使用保存的请求

---

## 方法 3: Python 日志调试

如果不想用调试器，可以添加 print 语句：

### 修改 views.py 添加日志

```python
import logging
logger = logging.getLogger(__name__)

@csrf_exempt
def generate_careplan(request):
    if request.method == "POST":
        logger.info("=" * 50)
        logger.info("🔵 Step 1: Request received")
        
        body = json.loads(request.body)
        logger.info(f"🔵 Step 2: Parsed body: {body}")
        
        patient_name = body.get("name")
        logger.info(f"🔵 Step 3: Patient: {patient_name}")
        
        # ... 其他步骤
        
        logger.info(f"🔵 Step 4: Calling OpenAI API...")
        response = client.chat.completions.create(...)
        
        logger.info(f"🔵 Step 5: API returned, length: {len(careplan)}")
        
        return JsonResponse({"careplan": careplan})
```

在终端运行服务时会看到这些日志输出。

---

## 🎯 快速开始流程

### 完整调试流程（推荐新手）

```bash
# 1. 启动 Django 服务（调试模式）
# 在 VSCode 按 F5，选择 "Django: Debug Server"

# 2. 在 views.py 第 21 行设置断点

# 3. 打开 Postman，发送测试请求

# 4. 代码会在断点处暂停，查看变量

# 5. 按 F10 逐行执行，观察数据流转
```

---

## 🔍 常见问题

### Q1: 断点不生效？
**A**: 确保：
- Python 扩展已安装
- 使用 F5 启动（不是 `python manage.py runserver`）
- 断点设置在会执行的代码行上

### Q2: Postman 报错 Connection refused？
**A**: 确保 Django 服务正在运行：
```bash
python manage.py runserver
```

### Q3: 看不到请求参数？
**A**: 在断点处，查看：
- `request.body` - 原始请求体
- `body` 变量 - 解析后的 JSON
- Variables 面板中的所有局部变量

### Q4: 想看 OpenAI 返回的原始数据？
**A**: 在第 54 行设置断点，查看 `response` 对象：
```python
response.choices[0].message.content  # 返回的文本
response.usage  # token 使用情况
```

---

## 📚 学习资源

- [VSCode Python 调试文档](https://code.visualstudio.com/docs/python/debugging)
- [Postman 入门教程](https://learning.postman.com/docs/getting-started/introduction/)
- [Django 调试技巧](https://docs.djangoproject.com/en/stable/topics/logging/)

---

**提示**: 建议从 VSCode 调试器开始，它能让你清楚地看到代码执行的每一步！
