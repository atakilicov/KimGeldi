Bu proje yapay zeka destekli bir Telegram botudur. RaspberryPi 4 üzerinde çalışmaktadır. API'ler vasıtasıyla çalıştığı için işlem yükü oldukça hafiftir.
Manuel olarak oluşturulmuş özel bir dataset ile eğitilmiş YOLOv8 modeli, 
RTSP yayınından çekilen görüntü Roboflow'un REST API'si kullanarak modele gönderilir, 
API JSON olarak tahminini detaylıca gönderir,
program gerekli kontrolleri yapıp insan olup olmadığını belirler.
ayrıca istenirse anlık olarak görüntüyü de iletebilir.
eğer insan tespit ederse Telegram botu aracılığıyla kullanıcılara görüntüyü mesaj olarak gönderir. 
örnek kullanım videosu geliştirme tamamamlanınca eklenecek.
API anahtarları ve diğer hassas bilgiler repoda yoktur. gerekli değerleri kendiniz girip deneyebilirsiniz. benim çalışan botumu denemek için mesaj atarsanız yetki verebilirim.                        
