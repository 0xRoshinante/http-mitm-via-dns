# http-mitm-via-dns
DNS Tabanlı HTTP/HTTPS MITM Aracı

Bu araç, DNS yanıltması ile gelen HTTP isteklerini replike ederek harici bir istemciyle orijinal sunucuya proxyden geçirerek ileten dns tabanlı basit bir mitm aracıdır.

## Özellikler

- HTTP ve HTTPS protokollerini destekler.
- İsteğe bağlı olarak başka bir proxy sunucu üzerinden bağlantı kurabilir.

## Gereksinimler

- Python 3.6 veya üzeri
- `requests` kütüphanesi

Gereksinimleri yüklemek için:

```bash
pip install requests
```

## Kurulum

Projeyi klonlayın:
```bash
git clone https://github.com/0xRoshinante/http-mitm-via-dns
cd http-mitm-via-dns
```

Trigger-server için sertifikalarınızı oluşturun:
```bash
openssl genrsa -out mitm-key.pem 2048
openssl req -new -x509 -key mitm-key.pem -out mitm-cert.pem -days 365
```

## Kullanım

Secure bağlantılar için:
```bash
python http-mitm-via-dns.py --port PORT_NUMARASI [--proxy-host PROXY_IP] [--proxy-port PROXY_PORT] [--certfile CERT_DOSYASI] [--keyfile KEY_DOSYASI]
```

Secure olmayan bağlantılar için:
```bash
python http-mitm-via-dns.py --port PORT_NUMARASI [--proxy-host PROXY_IP] [--proxy-port PROXY_PORT]
```
