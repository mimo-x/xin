# URL 设计最佳实践指南

> 基于 Kyle Neath 的《URL Design》及行业最佳实践整理

## 核心原则

### 1. URL 是为人类设计的
- URL 应该易读、易记、易理解
- 用户应该能够通过 URL 推断页面内容
- 避免复杂的编码和难以理解的参数

### 2. URL 是一种约定
- 一旦发布，URL 就是一个长期承诺
- 不要轻易更改已发布的 URL
- 如果必须更改，务必添加 301 重定向

### 3. URL 是通用的
- 在所有浏览器、设备、工具中都能工作
- 可以被复制、粘贴、分享
- 甚至可以写在纸上传递

---

## 一、结构设计原则

### 1.1 顶级路径设计

**重要性：** 顶级路径是 URL 中最宝贵的部分，决定网站的基本结构。

**最佳实践：**
```
✅ 好的设计
https://example.com/products
https://example.com/blog
https://example.com/docs

❌ 避免
https://example.com/p
https://example.com/content/blog/posts
```

**建议：**
- 在产品设计初期就确定顶级路径
- 使用简短、清晰、描述性的词语
- 保留常用词汇作为黑名单（如 admin, api, help, about 等）
- 考虑未来扩展性

### 1.2 命名空间（Namespace）

**概念：** 命名空间是 URL 中用于区分不同实体的部分。

**示例：**
```
https://github.com/用户名/仓库名/issues
https://medium.com/@作者/文章标题
https://example.com/店铺ID/产品/详情
```

**原则：**
- 保持命名空间的一致性和统一性
- 不要混合不同的命名空间模式
- 命名空间后的路径应该可以复用

**实例对比：**
```
✅ 一致的设计
/user/john/posts
/user/john/comments
/user/mary/posts

❌ 不一致的设计
/user/john/posts
/posts/user/mary
/feature/user/bob/comments
```

### 1.3 层级深度

**建议：**
- 保持 URL 层级在 3-5 层为最佳
- 避免过深的嵌套（超过 6 层）
- 每一层都应该有明确的语义

**示例：**
```
✅ 合理的层级
/blog/2024/05/article-title
/products/electronics/phones/iphone-15

❌ 过深的层级
/content/site/region/country/city/category/subcategory/item
```

---

## 二、命名规范

### 2.1 使用小写字母

```
✅ 推荐
/user-profile
/api/products

❌ 避免
/User-Profile
/API/Products
```

**原因：**
- 某些服务器区分大小写
- 小写更易输入和记忆
- 避免混淆（如 `/User` vs `/user`）

### 2.2 使用连字符（-）而非下划线（_）

```
✅ 推荐
/user-profile
/product-details

❌ 避免
/user_profile
/product_details
```

**原因：**
- 连字符更符合 URL 规范
- 搜索引擎将连字符视为单词分隔符
- 下划线在某些显示中可能被下划线遮挡

### 2.3 使用有意义的词汇

```
✅ 清晰的语义
/products/laptops
/users/settings
/blog/how-to-design-urls

❌ 含糊的缩写
/prod/lpt
/usr/cfg
/b/htdu
```

**原则：**
- 使用完整、常见的英文单词
- 避免过度缩写
- 保持词语简短但清晰
- 单词不应包含特殊字符

### 2.4 避免非 ASCII 字符

```
✅ 推荐
/products/coffee-maker
/blog/traveling-tips

❌ 避免
/产品/咖啡机
/blog/tråvëlïng-tîps
```

**原因：**
- 非 ASCII 字符会被编码（如 `%E4%BA%A7%E5%93%81`）
- 难以输入和记忆
- 可能在某些系统中出现问题

**例外：** 如果目标用户主要使用非英语，可以考虑使用本地语言，但要确保正确编码。

---

## 三、参数与查询字符串

### 3.1 查询字符串的适用场景

**适合使用查询字符串的场景：**
- 过滤（filter）
- 排序（sort）
- 分页（page）
- 搜索关键词（query/search）
- 视图模式切换（view）

**示例：**
```
/products?category=laptop&sort=price&order=asc
/search?q=url+design&page=2
/articles?tag=tech&lang=zh
```

### 3.2 查询字符串命名规范

**保持一致性：**
```
✅ 一致的命名
?sort=price&order=desc
?filter=active&type=user

❌ 不一致的命名
?sort=price&sortOrder=desc
?filterBy=active&type=user
```

**常用参数命名建议：**
```
page, per_page, limit, offset     # 分页
sort, order, sort_by, order_by    # 排序
q, query, search, keyword         # 搜索
filter, category, type, status    # 过滤
view, mode, display               # 显示模式
```

### 3.3 页面无查询字符串时应该可用

**原则：** 去掉查询字符串后，URL 应该返回有效页面（通常是默认状态）

```
✅ 正确的设计
/products                    # 显示所有产品（默认排序）
/products?sort=price         # 按价格排序

❌ 错误的设计
/products                    # 返回 400 错误
/products?view=list          # 必须有参数才能访问
```

### 3.4 RESTful 路径 vs 查询字符串

**使用路径：** 用于标识资源
```
/users/123
/products/laptop-xyz
/articles/2024/05/url-design
```

**使用查询字符串：** 用于资源的筛选和操作
```
/users?role=admin
/products?category=laptop
/articles?year=2024&month=05
```

---

## 四、RESTful API 设计

### 4.1 资源命名

**使用名词复数形式：**
```
✅ 推荐
GET    /users
GET    /users/123
POST   /users
PUT    /users/123
DELETE /users/123

❌ 避免
GET    /getUsers
GET    /user/123
POST   /createUser
```

### 4.2 资源关系表达

**嵌套资源：**
```
/users/123/posts              # 用户的所有文章
/users/123/posts/456          # 用户的特定文章
/posts/456/comments           # 文章的所有评论
/posts/456/comments/789       # 文章的特定评论
```

**避免过深嵌套：**
```
✅ 推荐（最多 2-3 层）
/users/123/posts

❌ 避免（过深）
/organizations/1/departments/2/teams/3/users/4/posts/5
```

### 4.3 操作与动作

**特殊操作使用动词：**
```
POST /users/123/follow          # 关注用户
POST /articles/456/publish      # 发布文章
POST /orders/789/cancel         # 取消订单
GET  /reports/generate          # 生成报告
```

### 4.4 版本控制

**方式一：路径版本**
```
/api/v1/users
/api/v2/users
```

**方式二：子域名**
```
https://api-v1.example.com/users
https://api-v2.example.com/users
```

**方式三：请求头（推荐用于成熟 API）**
```
GET /users
Header: Accept: application/vnd.example.v2+json
```

---

## 五、特殊场景处理

### 5.1 多语言支持

**方式一：路径前缀（推荐）**
```
/en/products
/zh/products
/ja/products
```

**方式二：子域名**
```
https://en.example.com/products
https://zh.example.com/products
```

**方式三：查询参数**
```
/products?lang=en
/products?lang=zh
```

**建议：** 使用路径前缀，对 SEO 友好且清晰明确。

### 5.2 移动端适配

**响应式设计（推荐）：**
```
https://example.com/products    # 同一 URL，响应式布局
```

**独立移动站点：**
```
https://m.example.com/products
```

**建议：** 优先使用响应式设计，避免内容重复和 SEO 问题。

### 5.3 文件格式支持

**方式一：扩展名**
```
/api/users/123.json
/api/users/123.xml
/reports/2024-05.pdf
```

**方式二：查询参数**
```
/api/users/123?format=json
/reports/2024-05?format=pdf
```

**方式三：Content Negotiation（HTTP Header）**
```
GET /api/users/123
Header: Accept: application/json
```

**GitHub 示例：**
```
https://github.com/user/repo/pull/123
https://github.com/user/repo/pull/123.patch
https://github.com/user/repo/pull/123.diff
```

### 5.4 日期处理

**推荐格式：**
```
/blog/2024/05/15/article-title          # 年/月/日
/events/2024-05-15                       # ISO 8601
/archive/2024/05                         # 年/月
```

**避免：**
```
/blog/05-15-2024          # 美式格式，不够国际化
/blog/20240515            # 难以阅读
```

---

## 六、安全与隐私

### 6.1 避免敏感信息泄露

**不要在 URL 中暴露：**
```
❌ 危险
/admin/users?api_key=abc123
/account?password=secret
/private-doc?token=xyz789
```

**应该使用：**
- HTTP Headers（Authorization）
- 请求体（POST/PUT）
- Cookie/Session
- 加密令牌

### 6.2 可预测性风险

**避免顺序 ID：**
```
❌ 可能不安全
/orders/1001    # 攻击者可以尝试 1000, 1002...
/users/123      # 可以遍历所有用户
```

**解决方案：**
```
✅ 更安全
/orders/a8f5c9d2-4b3a-4e5f-9c1b-2d3e4f5a6b7c    # UUID
/users/k8sj29x                                  # 短 ID + 随机
```

**注意：** 对于公开资源（如博客文章），使用顺序 ID 是可以接受的。

### 6.3 权限验证

**原则：**
- 不要依赖 URL 隐藏来保护资源
- 始终在服务端验证权限
- 即使 URL 不可预测，也要验证访问权限

---

## 七、现代 Web 应用实践

### 7.1 单页应用（SPA）URL 管理

**使用 HTML5 History API：**

```javascript
// pushState - 添加新的历史记录（影响后退按钮）
window.history.pushState(null, "Page Title", "/new-url");

// replaceState - 替换当前历史记录（不影响后退按钮）
window.history.replaceState(null, "Page Title", "/updated-url");
```

**使用场景：**
- **pushState**：导航到新页面、分页、新内容
- **replaceState**：过滤、排序、视图切换

### 7.2 保持链接的标准行为

**正确的实现：**

```javascript
$('a.ajax-link').click(function(e){
  // 不支持 History API 的浏览器降级处理
  if (!('pushState' in window.history)) return true;

  // 中键点击、Ctrl/Cmd+点击 正常打开新窗口
  if (e.which === 2 || e.metaKey || e.ctrlKey) {
    return true;
  }

  // AJAX 加载内容
  loadContent(this.href);

  // 更新 URL
  window.history.pushState(null, "Title", this.href);

  // 阻止默认跳转
  return false;
});
```

**原则：**
- `<a>` 标签的 `href` 应包含完整的 URL
- 支持右键"在新标签页打开"
- 浏览器状态栏应显示目标 URL
- 支持复制链接地址

### 7.3 每个状态都应该有 URL

**原则：** 用户看到的每个独特界面状态都应该有唯一的 URL

**示例：**
```
✅ 好的设计
/products                    # 列表视图
/products?view=grid          # 网格视图
/products/123                # 详情视图
/products/123/edit           # 编辑视图
/products?category=laptop    # 过滤后的视图
```

**好处：**
- 可以收藏当前状态
- 可以分享给他人
- 可以在新标签页打开
- 浏览器后退/前进正常工作

### 7.4 避免 POST 专用 URL

**问题：**
```
❌ POST 专用 URL
提交表单后显示 /form/submit
复制粘贴到新标签 → 错误页面或警告
```

**解决方案：**
```
✅ PRG 模式（Post-Redirect-Get）
POST /orders/create
  → 302 Redirect
    → GET /orders/123

用户看到 /orders/123，可以安全刷新和分享
```

---

## 八、SEO 优化建议

### 8.1 语义化 URL

**好的 URL 对 SEO 的影响：**
```
✅ 有利于 SEO
/blog/ultimate-guide-to-url-design
/products/electronics/laptop-macbook-pro-16

❌ 不利于 SEO
/blog/post?id=12345
/products/view.php?cat=3&pid=456
```

### 8.2 避免关键词堆砌

**不要过度优化：**
```
❌ 关键词堆砌（2003年的做法）
/best-cheap-affordable-budget-laptops-computers-for-sale

✅ 自然且有意义
/laptops/budget-friendly
```

### 8.3 规范化 URL

**使用 canonical 标签：**
```html
<!-- 如果有多个 URL 指向相同内容 -->
<link rel="canonical" href="https://example.com/products/laptop" />
```

**一致的 URL 形式：**
```
✅ 选择一种并保持一致
https://example.com/products
https://www.example.com/products

❌ 混合使用
有时用 www，有时不用
有时结尾有 /，有时没有
```

### 8.4 URL 长度

**建议：**
- 保持在 75-100 字符以内（在搜索结果中完整显示）
- 最长不超过 2048 字符（浏览器限制）
- 简短、有意义优于冗长

---

## 九、性能与技术考虑

### 9.1 URL 重写与重定向

**301 永久重定向：**
```
旧 URL 已永久移动到新位置
使用场景：网站重构、URL 规范化
```

**302 临时重定向：**
```
临时性的跳转
使用场景：维护页面、临时替换
```

**307/308：**
```
保持原始 HTTP 方法的重定向
使用场景：API 重定向，保持 POST/PUT 等方法
```

### 9.2 URL 编码

**需要编码的字符：**
```
空格    → %20 或 +
中文    → %E4%B8%AD%E6%96%87
特殊字符 → & → %26, ? → %3F
```

**不需要编码的字符（URL 安全字符）：**
```
字母：A-Z a-z
数字：0-9
安全符号：- _ . ~
```

### 9.3 URL 长度限制

**各浏览器限制：**
- IE: 2083 字符
- Chrome: 32,779 字符
- Firefox: 65,536 字符
- Safari: 80,000 字符

**实践建议：**
- 保持 URL 在 2000 字符以内（兼容所有浏览器）
- 过长的参数考虑使用 POST 方法

---

## 十、测试与验证

### 10.1 URL 设计检查清单

**设计阶段：**
- [ ] URL 结构是否符合逻辑且一致？
- [ ] 是否易于理解和记忆？
- [ ] 是否考虑了未来的扩展性？
- [ ] 是否有保留关键词黑名单？

**技术实现：**
- [ ] 是否所有 URL 都有对应的页面？
- [ ] 重定向是否正确配置？
- [ ] 是否支持 HTTPS？
- [ ] 移动端 URL 是否正确处理？

**SEO 检查：**
- [ ] URL 是否语义化？
- [ ] 是否避免了重复内容？
- [ ] canonical 标签是否正确？
- [ ] sitemap 是否包含所有 URL？

**用户体验：**
- [ ] 链接是否按预期工作？
- [ ] 中键/Ctrl+点击能否正常打开新窗口？
- [ ] 后退按钮是否按预期工作？
- [ ] 每个状态是否都可以通过 URL 访问？

### 10.2 常见错误检查

**避免这些常见问题：**

```
❌ 尾随斜杠不一致
/products  和 /products/  被视为不同页面

❌ 大小写混乱
/Products 和 /products 不同

❌ 参数顺序依赖
/search?a=1&b=2 和 /search?b=2&a=1 不同

❌ 会话 ID 在 URL 中
/page?sessionid=xyz123

❌ 框架默认 URL
/index.php?page=about
/default.aspx?id=123
```

---

## 十一、工具与资源

### 11.1 URL 设计工具

**在线工具：**
- URL Encoder/Decoder
- Redirect Checker
- Canonical Tag Checker

**开发工具：**
- Chrome DevTools - Network 面板
- Postman - API 测试
- Screaming Frog - SEO 爬虫

### 11.2 推荐阅读

**规范文档：**
- RFC 3986: URI Generic Syntax
- REST API Design Best Practices
- Google Search Central - URL Structure

**相关文章：**
- "URL Design" by Kyle Neath
- "RESTful API Design Guidelines"
- "The Art of URL Design"

---

## 十二、实战案例分析

### 案例 1: GitHub URL 设计

**分析：**
```
https://github.com/facebook/react/pull/12345#issuecomment-67890

✅ 优点：
- 清晰的命名空间：用户名/仓库名
- 语义化路径：pull（Pull Request）
- 简短的资源 ID：12345
- 锚点定位：#issuecomment-67890
- 支持多格式：.patch, .diff

命名空间设计：
/用户名/仓库名/issues     # 所有仓库都有此路径
/用户名/仓库名/pulls      # 统一的结构
/用户名/仓库名/wiki       # 可预测的模式
```

### 案例 2: Airbnb URL 设计

**分析：**
```
https://airbnb.com/rooms/12345678?adults=2&checkin=2024-05-01

✅ 优点：
- 简洁的资源路径：/rooms/ID
- 查询参数用于过滤：adults, checkin
- 国际化通过子域名：zh.airbnb.com

路径设计：
/rooms/123       # 房源详情
/experiences/456 # 体验详情
/wishlists/789   # 心愿单
```

### 案例 3: Medium URL 设计

**分析：**
```
https://medium.com/@author/article-title-abc123

✅ 优点：
- @ 符号标识用户
- 可读的文章标题
- 唯一 ID 后缀避免冲突

URL 演化：
早期：/p/abc123（短但不友好）
现在：/@author/title-abc123（语义化且唯一）
```

---

## 十三、总结

### 核心原则回顾

1. **简洁明了** - 简短、清晰、有意义
2. **一致性** - 遵循统一的命名和结构规范
3. **可预测** - 用户能够推断 URL 的含义和导航
4. **持久性** - 一旦发布，尽量不变
5. **语义化** - URL 应该描述资源的含义
6. **可分享** - 每个状态都有独立的 URL
7. **对人友好** - 为人类设计，不是机器
8. **RESTful** - 遵循 REST 设计原则（API）

### 快速参考表

| 场景 | 推荐做法 | 避免 |
|------|---------|------|
| 分隔符 | 使用连字符 `-` | 下划线 `_` |
| 字母 | 小写 | 大小写混用 |
| 资源名 | 名词复数 `/users` | 动词 `/getUser` |
| 嵌套 | 2-3 层 | 超过 5 层 |
| 查询参数 | 过滤/排序 | 标识资源 |
| 版本 | `/api/v1/` | 参数 `?v=1` |
| 日期 | ISO 8601 | 地区格式 |
| ID | UUID/短码 | 顺序数字（敏感资源） |

### 设计流程建议

1. **规划阶段**
   - 定义顶级路径结构
   - 确定命名空间策略
   - 预留关键词黑名单

2. **设计阶段**
   - 绘制 URL 结构图
   - 定义命名规范
   - 设计 URL 模式文档

3. **开发阶段**
   - 实现 URL 路由
   - 配置重定向规则
   - 添加 canonical 标签

4. **测试阶段**
   - 测试所有路由
   - 检查 SEO 友好性
   - 验证用户体验

5. **维护阶段**
   - 监控 404 错误
   - 定期审查 URL 结构
   - 记录 URL 变更

---

## 附录：URL 解剖

```
https://www.example.com:443/path/to/resource?key=value&foo=bar#section

[协议] [子域] [域名] [端口] [路径] [查询字符串] [片段/锚点]
```

**各部分说明：**
- **协议（Scheme）**: https, http, ftp
- **子域（Subdomain）**: www, api, cdn
- **域名（Domain）**: example.com
- **端口（Port）**: 443（HTTPS 默认）, 80（HTTP 默认）
- **路径（Path）**: /path/to/resource
- **查询字符串（Query String）**: ?key=value&foo=bar
- **片段（Fragment）**: #section

---

**参考文献：**
- Kyle Neath - "URL Design" (2010)
- Roy Fielding - "REST Architectural Style"
- RFC 3986 - Uniform Resource Identifier (URI)
- Google Search Central - URL Structure Guidelines

**最后更新：** 2025-10-13
