# Youtube爬取数据说明
## 下载数据链接  
访问[VoxCeleb2数据集官网](https://www.robots.ox.ac.uk/~vgg/data/voxceleb/vox2.html "VoxCeleb2数据集官网")  
找到要下载的数据集链接  
![image](https://user-images.githubusercontent.com/61792863/176355768-db611be7-ecdf-4960-a45f-a2130dbb7395.png)  
下载并解压  

## 程序准备
### 开启vpn,并将系统代理模式调成全局模式  
![IMG_20220629_145305_edit_51026953673983](https://user-images.githubusercontent.com/61792863/176373720-884d2e51-a569-459e-ac81-68c97a1871af.jpg)  
### 下载yt-dlp
pip install yt_dlp  【注意！此处是下划线】   
![image](https://user-images.githubusercontent.com/61792863/176421634-79282626-40b1-41b9-b90f-0197686c1431.png)  

## 配置  
![image](https://user-images.githubusercontent.com/61792863/176422261-440288ac-0475-49e7-8fea-5853f4231889.png)  
### 1.设置url获取路径  
将url路径设置为从官网下载的数据链接集合的txt文件  
![image](https://user-images.githubusercontent.com/61792863/176373174-6104751d-1201-454f-bba6-6734d955d6b2.png)  
### 2. 设置保存路径及用户名密码
![image](https://user-images.githubusercontent.com/61792863/176422303-f9963300-242b-4adc-9421-582b769a87d4.png)  
### 3. 设置爬取视频的线程数量  
![image](https://user-images.githubusercontent.com/61792863/176422109-53f91cf1-cecc-43e8-8165-5daf41f998a4.png)


## 运行程序
程序会在你选定的存储路径生成一个video文件夹、一个audio文件夹和一个log.txt的文件，记载没有成功下载的文件信息  

## 运行结果
![image](https://user-images.githubusercontent.com/61792863/176422493-06dfc30f-7f83-4a95-b3e8-be66250f94ac.png)  
![image](https://user-images.githubusercontent.com/61792863/176422635-4dac0f40-62ee-4572-aecd-ce3bc18ad3e7.png)  
![image](https://user-images.githubusercontent.com/61792863/176422794-f54a7490-82c8-4fb4-9311-faef9da9fd8d.png)  
![image](https://user-images.githubusercontent.com/61792863/176422882-325bbdec-aead-44a3-ba40-c5855de45f71.png)  
![image](https://user-images.githubusercontent.com/61792863/176423247-9af780a7-228c-48b6-bcd2-8474467f3340.png)  
