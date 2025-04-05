import requests
import re
import argparse

def extract_comments_from_html(url):
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        html = response.text
    except requests.exceptions.RequestException as e:
        print(f"[!] Error fetching the URL: {e}")
        return[]
    
    # コメントアウト抽出
    comments = re.findall(r'<!--(.*?)-->', html, re.DOTALL)
    return [c.strip() for c in comments]

def save_comments_to_file(comments, filepath):
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            for i, comment in enumerate(comments, 1):
                f.write(f"[{i}] {comment}\n\n")
            print(f"✅ Comments saved to: {filepath}")
    except Exception as e:
        print(f"[!] Error saving file: {e}")

def main():
    parser = argparse.ArgumentParser(description="Extract HTML comments from a given URL.")
    parser.add_argument("url", help="Target URL (e.g., https://examle.com)")
    parser.add_argument("-o", "--output", help="Save output to a file")

    args = parser.parse_args()
    url = args.url.strip()

    # http/https自動補正
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "http://" + url

    print("\n🔍 Extracting HTML comments from:", url, "\n")
    comments = extract_comments_from_html(url)

    if comments:
        for i, comment in enumerate(comments, 1):
            print(f"[{i}] {comment}\n")

        if args.output:
            save_comments_to_file(comments, args.output)

    else:
        print("❌ No HTML comments found.")

if __name__ == "__main__":
    main()