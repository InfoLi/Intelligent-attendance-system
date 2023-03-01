# Intelligent attendance system
 软院大三实训《智能考勤系统》  
/models:下放训练好的人脸识别模型
/template:存放前端网页的静态模板
/static:存放构成网页的静态资源（css,js,图片等）

runserver.py为项目运行py文件

（其余文件为项目的其他构成文件）

1. constValue.py部分待渲染模板的特征值
2. enhanceTool.py包括去噪函数，可以用于人脸识别增强
3. onnxSever.py封装了人脸检测与人脸识别算法
4. runsever.py是服务器端代码，整合了所有功能
5. routerGet.py包含各个路由的具体函数设置
6. sqlFunction.py包含SQL调用，用于与SQL数据库交互
7. tool.py含有各个工具函数，不影响正常使用

可以通过`python runserver.py`进行测试
