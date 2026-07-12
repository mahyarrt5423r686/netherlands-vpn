# چطور کانفیگ هلند را اضافه کنم تا IP واقعا عوض شود؟

## حالت 1: لینک VLESS / VMess / Trojan داری (رایج‌ترین)

مثال:
```
vless://a3482e88-686a-4a58-8126-99c9df64b7bf@142.132.144.23:443?encryption=none&flow=xtls-rprx-vision&security=tls&sni=example.com&type=tcp#Netherlands
```

### قدم:
1. فایل `app/src/main/java/com/netherlands/vpn/V2RayConfig.kt` را باز کن
2. خط 15:
   const val NETHERLANDS_SERVER_URI = "لینک خودت را اینجا بذار"
3. فایل `app/src/main/assets/netherlands_config.json` را هم باید دستی بسازی:

برای VLESS مثال بالا، JSON اش می‌شود (من برایت می‌سازم اگر لینک را بفرستی):

```json
{
  "outbounds": [{
    "protocol": "vless",
    "settings": {
      "vnext": [{"address": "142.132.144.23", "port": 443, "users": [{"id": "uuid", "flow": "xtls-rprx-vision"}]}]
    },
    "streamSettings": {"network": "tcp", "security": "tls", "tlsSettings": {"serverName": "example.com"}}
  }]
}
```

## حالت 2: از پنل X-UI / Marzban / Hiddify JSON می‌گیری

1. در پنل روی سرور هلند کلیک کن -> Export Config -> Export as Xray JSON
2. آن JSON کامل را کپی کن و در `netherlands_config.json` پیست کن (جایگزین کل فایل)
3. آماده!

## حالت 3: می‌خواهی من انجام بدهم

فقط لینک را در چت بفرست. مثلا بگو:

> این کانفیگ منه: vless://...

من همین الان:
- آن را پارس می‌کنم
- JSON کامل v2ray می‌سازم
- داخل پروژه جایگذاری می‌کنم
- یک APK تستی guide می‌دهم

## تست اتصال واقعی

بعد از Build و نصب:

1. دکمه "اتصال به هلند" را بزن
2. تایید VPN را بده
3. صبر کن 2 ثانیه
4. دکمه "بررسی مجدد IP" را بزن
5. باید ببینی: "Amsterdam, Netherlands" و IP هلندت
6. برو به https://whatismyipaddress.com - باید هلند باشد

اگر نشد، Logcat را در Android Studio ببین یا `tvLog` در اپ را بخوان.
