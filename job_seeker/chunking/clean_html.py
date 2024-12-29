from bs4 import BeautifulSoup


def clean_html(html):
    soup = BeautifulSoup(html)
    unused_tags = ["script", "style", "svg", "image", "iframe"]
    for tag_name in unused_tags:
        for tag in soup.find_all(tag_name):
            tag.decompose()
    for tag in soup.find_all(True):
        tag.attrs.clear()
    return "".join(str(soup).splitlines())
