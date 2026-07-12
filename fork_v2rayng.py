#!/usr/bin/env python3
"""
اسکریپت تبدیل پروژه اصلی v2rayNG به اپ اختصاصی هلند شما
کار: 
1. کلون v2rayNG
2. تغییر نام و آیکون به Netherlands VPN
3. اضافه کردن کانفیگ هلند به عنوان سرور پیش‌فرض
"""
import os, sys, json, shutil, subprocess, argparse, base64, re

def run(cmd):
    print(f"> {cmd}")
    subprocess.run(cmd, shell=True, check=True)

def parse_vless(uri):
    # ساده برای نمایش
    try:
        # vless://uuid@host:port?params#name
        m = re.match(r'vless://([^@]+)@([^:]+):(\d+)\?([^#]+)#?(.*)', uri)
        if m:
            uuid, host, port, params, name = m.groups()
            return {"uuid": uuid, "host": host, "port": int(port), "params": params, "name": name or "Netherlands"}
    except: pass
    return None

def main():
    parser = argparse.ArgumentParser(description="تبدیل v2rayNG به Netherlands VPN")
    parser.add_argument("--config", required=True, help="لینک vmess/vless/trojan سرور هلند")
    parser.add_argument("--out", default="V2rayNG-Netherlands", help="پوشه خروجی")
    args = parser.parse_args()

    config_uri = args.config.strip()
    print(f"🚀 شروع ساخت اپ هلند با کانفیگ: {config_uri[:60]}...")

    # 1. Clone
    if os.path.exists(args.out):
        print(f"⚠️ پوشه {args.out} وجود دارد - حذف و کلون دوباره")
        shutil.rmtree(args.out)
    
    run(f"git clone https://github.com/2dust/v2rayNG.git {args.out}")

    # 2. Change app name
    strings_path = os.path.join(args.out, "V2rayNG/app/src/main/res/values-zh-rCN/strings.xml")
    # انگلیسی
    en_strings = os.path.join(args.out, "V2rayNG/app/src/main/res/values/strings.xml")
    if os.path.exists(en_strings):
        with open(en_strings, 'r', encoding='utf-8') as f:
            content = f.read()
        content = content.replace(">v2rayNG<", ">Netherlands VPN 🇳🇱<")
        with open(en_strings, 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ نام اپ تغییر کرد")

    # 3. Change applicationId? - اختیاری
    build_gradle = os.path.join(args.out, "V2rayNG/app/build.gradle")
    if os.path.exists(build_gradle):
        with open(build_gradle, 'r') as f:
            gradle_content = f.read()
        # کامنت برای راهنما
        if "com.netherlands.vpn" not in gradle_content:
            gradle_content += "\n// برای تغییر پکیج اختصاصی خود: applicationId \"com.netherlands.vpn\"\n"
        with open(build_gradle, 'w') as f:
            f.write(gradle_content)

    # 4. Inject default server
    # v2rayNG سرور ها را در SharedPreferences نگه می‌دارد
    # ما یک فایل assets جدید می‌سازیم که در اولین اجرا import شود
    # روش ساده: فایل v2ray_config.json را با کانفیگ هلند جایگزین می‌کنیم؟ نه - آن کانفیگ داخلی socks است
    # بهترین روش: یک subscription file یا یک فایل initial config

    assets_dir = os.path.join(args.out, "V2rayNG/app/src/main/assets")
    os.makedirs(assets_dir, exist_ok=True)

    # یک فایل راهنما برای کاربر بساز که کانفیگش کجاست
    with open(os.path.join(assets_dir, "netherlands_server.txt"), 'w', encoding='utf-8') as f:
        f.write(config_uri + "\n")
        f.write(f"# Netherlands Server injected at build time\n")
    
    # یک کلاس کمکی بسازیم که در MainActivity سرور را اضافه کند
    # فایل کمکی: DefaultServers.kt
    default_server_code = f'''
package com.v2ray.ang

// این فایل خودکار توسط fork_v2rayng.py ساخته شده
object DefaultNetherlandsServers {{
    const val NETHERLANDS_URI = "{config_uri}"
    const val SERVER_REMARK = "Netherlands 🇳🇱 - Amsterdam"
}}
'''
    kt_path = os.path.join(args.out, "V2rayNG/app/src/main/java/com/v2ray/ang/dto")
    os.makedirs(kt_path, exist_ok=True)
    with open(os.path.join(args.out, "V2rayNG/app/src/main/java/com/v2ray/ang/DefaultNetherlandsServers.kt"), 'w') as f:
        f.write(default_server_code)

    print("✅ کانفیگ هلند در پروژه قرار گرفت")
    print("""
    📝 کار تمام نشد - برای اتوماتیک Import شدن کانفیگ:
    
    1. فایل زیر را باز کن:
       V2rayNG/app/src/main/java/com/v2ray/ang/ui/MainActivity.kt
    
    2. در onCreate بعد از super.onCreate این خط را اضافه کن:
    
        // Auto import Netherlands server on first run
        val prefs = getSharedPreferences(\"first_run\", MODE_PRIVATE)
        if (!prefs.getBoolean(\"nl_imported\", false)) {{
            try {{
                val uri = DefaultNetherlandsServers.NETHERLANDS_URI
                // از متد موجود v2rayNG برای import استفاده کن
                // importBatchConfig(uri) 
                prefs.edit().putBoolean(\"nl_imported\", true).apply()
            }} catch (e: Exception) {{}}
        }}
    
    این بخش به خاطر تغییرات مداوم v2rayNG به صورت دستی باید انجام شود، اما من فایل asset را آماده کردم.
    """)

    # 5. Create README for builds
    with open(os.path.join(args.out, "BUILD_NETHERLANDS.md"), 'w', encoding='utf-8') as f:
        f.write(f"""
# Netherlands VPN - Build Guide

کانفیگ تو: {config_uri}

## چطور APK بسازی؟

1. Android Studio را باز کن
2. پوشه {args.out}/V2rayNG را به عنوان پروژه باز کن
3. صبر کن Gradle sync شود
4. Build -> Build APK

## چه تغییراتی دادیم؟

- نام برنامه به Netherlands VPN تغییر کرد
- فایل assets/netherlands_server.txt حاوی لینک سرور هلند شما اضافه شد
- کلاس DefaultNetherlandsServers.kt ساخته شد
- برای Import خودکار، دستورالعمل بالا را در MainActivity اضافه کن

یا ساده‌تر: از اپ سفارشی ما در NetherlandsVPN/ استفاده کن که همین کار را با یک دکمه انجام می‌دهد.
""")

    print(f"\n✅ تمام شد! پروژه در {args.out} آماده است")
    print("👉 برای ساخت اپ ساده یک دکمه‌ای، از پوشه NetherlandsVPN استفاده کن")

if __name__ == "__main__":
    main()
