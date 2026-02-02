<h1 align="center">黑塔终端 XAML 编写说明</h1>

> 正在持续更新中...

## 前置教程
> 已经学习过前端基础知识请跳过
- 详情请见[XAML 入门教程](./learn_xaml.md)

## 非自闭合元素
- `<Page>`: 根元素
  - `path`: 识别每个页面的不同描述 (每个页面必须不同)
  - `icon`: 显示在侧边栏的图标 (支持 Base64 显示)
  - `name`: 显示在侧边栏的描述
  - `title`: 显示在主内容区域的顶部内容 (文字大小为24px)
  - `app`: 按钮向后端读取指令的程序标题
- `<Text>`: 描述文字
  - `type`: 类型
    - `title`: 将文字大小设置24px
    - `description`: 将文字颜色设置为灰色并设置大小12px
  - `url`: 跳转的链接 (超链接)
  - `margin`: 外边距 (设置方法与 [CSS margin](https://developer.mozilla.org/zh-CN/docs/Web/CSS/Reference/Properties/margin) 相同)
  - `color`: 文字颜色 (设置方法与 [CSS color](https://developer.mozilla.org/zh-CN/docs/Web/CSS/Reference/Properties/color) 相同)
  - `size`: 文字大小 (设置方法与 [CSS font-size](https://developer.mozilla.org/zh-CN/docs/Web/CSS/Reference/Properties/font-size) 相同)
- `<Box>`: 类卡片组件
  - `gap`: 间隔 (设置方法与 [CSS gap](https://developer.mozilla.org/zh-CN/docs/Web/CSS/Reference/Properties/gap) 相同)
  - `round`: 圆角半径 (设置方法与 [CSS border-radius](https://developer.mozilla.org/zh-CN/docs/Web/CSS/Reference/Properties/border-radius) 相同)
  - `border`: 边框宽度 (设置方法与 [CSS border-width](https://developer.mozilla.org/zh-CN/docs/Web/CSS/Reference/Properties/border-width) 相同)
  - `margin`: 外边距 (设置方法与 [CSS margin](https://developer.mozilla.org/zh-CN/docs/Web/CSS/Reference/Properties/margin) 相同)
  - `padding`: 内边距 (设置方法与 [CSS padding](https://developer.mozilla.org/zh-CN/docs/Web/CSS/Reference/Properties/padding) 相同)
  - `background`: 背景颜色 (设置方法与 [CSS background-color](https://developer.mozilla.org/zh-CN/docs/Web/CSS/Reference/Properties/background-color) 相同)
  - `align`: 内容位置 (设置方法与 [CSS align-items](https://developer.mozilla.org/zh-CN/docs/Web/CSS/Reference/Properties/align-items) 相同)
- `<Vertical>`: 垂直布局
  - `gap`: 间隔 (设置方法与 [CSS gap](https://developer.mozilla.org/zh-CN/docs/Web/CSS/Reference/Properties/gap) 相同)
  - `margin`: 外边距 (设置方法与 [CSS margin](https://developer.mozilla.org/zh-CN/docs/Web/CSS/Reference/Properties/margin) 相同)
  - `padding`: 内边距 (设置方法与 [CSS padding](https://developer.mozilla.org/zh-CN/docs/Web/CSS/Reference/Properties/padding) 相同)
  - `background`: 背景颜色 (设置方法与 [CSS background-color](https://developer.mozilla.org/zh-CN/docs/Web/CSS/Reference/Properties/background-color) 相同)
  - `align`: 内容位置 (设置方法与 [CSS align-items](https://developer.mozilla.org/zh-CN/docs/Web/CSS/Reference/Properties/align-items) 相同)
- `<Horizontal>`: 纵向布局
  - `gap`: 间隔 (设置方法与 [CSS gap](https://developer.mozilla.org/zh-CN/docs/Web/CSS/Reference/Properties/gap) 相同)
  - `margin`: 外边距 (设置方法与 [CSS margin](https://developer.mozilla.org/zh-CN/docs/Web/CSS/Reference/Properties/margin) 相同)
  - `padding`: 内边距 (设置方法与 [CSS padding](https://developer.mozilla.org/zh-CN/docs/Web/CSS/Reference/Properties/padding) 相同)
  - `background`: 背景颜色 (设置方法与 [CSS background-color](https://developer.mozilla.org/zh-CN/docs/Web/CSS/Reference/Properties/background-color) 相同)
  - `align`: 内容位置 (设置方法与 [CSS align-items](https://developer.mozilla.org/zh-CN/docs/Web/CSS/Reference/Properties/align-items) 相同)
- `<Button>`: 按钮
  - `type`: 类型
    - `toggle`: 点击会返回 true 或 false
    - `link`: 跳转的链接 (超链接) (需要搭配 `url`)
    - `click`: 点击只会返回 true
  - `disabled`: 是否禁用
    - `true`: 禁用
    - `false`: 启用
  - `command`: 向后端返回的命令
    - `slash-命令`: 输入命令前按下<kbd>右Ctrl+/</kbd>
    - `wave-命令`: 输入命令前下按下<kbd>~</kbd>
    - `命令`: 直接输入命令
  - `value`: 向后端公开的字符串 (用于后端读取)
  - `url`: 跳转的链接 (超链接) (当 `type` 为 `link` 时)
  - `margin`: 外边距 (设置方法与 [CSS margin](https://developer.mozilla.org/zh-CN/docs/Web/CSS/Reference/Properties/margin) 相同)
  - `width`: 宽度 (设置方法与 [CSS width](https://developer.mozilla.org/zh-CN/docs/Web/CSS/Reference/Properties/width) 相同)
  - `height`: 高度 (设置方法与 [CSS height](https://developer.mozilla.org/zh-CN/docs/Web/CSS/Reference/Properties/height) 相同)
- `<Switch>`: 滑块开关
  - `disabled`: 是否禁用
    - `true`: 禁用
    - `false`: 启用
  - `align`: ON/OFF 前后顺序
    - `left`: ON/OFF 在前
    - `right`: ON/OFF 在后
  - `value`: 向后端公开的字符串 (用于后端读取)

# 自闭合元素
- `<Line>`: 水平线
  - `margin`: 设置外边距 (设置方法与 [CSS margin](https://developer.mozilla.org/zh-CN/docs/Web/CSS/Reference/Properties/margin) 相同)
  - `size`: 设置边框宽度 (设置方法与 [CSS border-width](https://developer.mozilla.org/zh-CN/docs/Web/CSS/Reference/Properties/border-width) 相同)
  - `color`: 设置边框颜色 (设置方法与 [CSS border-color](https://developer.mozilla.org/zh-CN/docs/Web/CSS/Reference/Properties/border-color) 相同)
- `<Space>`: 增长系数 ([CSS flex-grow](https://developer.mozilla.org/zh-CN/docs/Web/CSS/Reference/Properties/flex-grow))
  - `factor`: 增长系数 (设置方法与 [CSS flex-grow](https://developer.mozilla.org/zh-CN/docs/Web/CSS/Reference/Properties/flex-grow) 相同)
- `<Input>`: 输入元素
  - `type`: 类型
    - `password`: 单行的文本区域，其值会被遮盖
    - `number`: 用于输入数字的控件
    - 更多: 详情请见 [HTML input](https://developer.mozilla.org/zh-CN/docs/Web/HTML/Reference/Elements/input)
  - `disabled`: 是否禁用
    - `true`: 禁用
    - `false`: 启用
  - `text`: 默认显示的内容
  - `value`: 向后端公开的字符串 (用于后端读取)
  - `margin`: 外边距 (设置方法与 [CSS margin](https://developer.mozilla.org/zh-CN/docs/Web/CSS/Reference/Properties/margin) 相同)
  - `width`: 宽度 (设置方法与 [CSS width](https://developer.mozilla.org/zh-CN/docs/Web/CSS/Reference/Properties/width) 相同)
  - `height`: 高度 (设置方法与 [CSS height](https://developer.mozilla.org/zh-CN/docs/Web/CSS/Reference/Properties/height) 相同)
  - `min`: 详情请见 [HTML input](https://developer.mozilla.org/zh-CN/docs/Web/HTML/Reference/Elements/input)
  - `max`: 详情请见 [HTML input](https://developer.mozilla.org/zh-CN/docs/Web/HTML/Reference/Elements/input)