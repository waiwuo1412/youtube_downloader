# Youtube爬取数据说明
## 下载数据链接  
访问[VoxCeleb2数据集官网](https://www.robots.ox.ac.uk/~vgg/data/voxceleb/vox2.html "VoxCeleb2数据集官网")  
找到要下载的数据集  
![image](https://user-images.githubusercontent.com/61792863/176355768-db611be7-ecdf-4960-a45f-a2130dbb7395.png)  
下载并解压  

## 程序准备
### 开启vpn,并将系统代理模式调成全局模式  
![IMG_20220629_145305_edit_51026953673983](https://user-images.githubusercontent.com/61792863/176373720-884d2e51-a569-459e-ac81-68c97a1871af.jpg)  
### 下载yt-dlp
pip install yt_dlp  【注意！此处是下划线】  

## 配置  
![image](https://user-images.githubusercontent.com/61792863/176372232-e27fe745-acaa-430c-ba4b-1f32fa888707.png)  
### 1.设置url获取路径  
将url路径设置为从官网下载的数据链接集合的txt文件  
![image](https://user-images.githubusercontent.com/61792863/176373174-6104751d-1201-454f-bba6-6734d955d6b2.png)  
### 2. 设置保存路径及用户名密码

### 3. 设置爬取视频的线程数量

## 运行程序
程序会在你选定的存储路径生成一个video文件夹、一个audio文件夹和一个log.txt的文件，记载没有成功下载的文件信息  
