from tropical.html import tag_html_generator, type_page_html_generator
from tropical.constants import SCRIPT_WRAPPER_HTML

class SnippetHtmlGenerator:
    def __init__(self, snippets_template):
        self._snippets_template = snippets_template

    def get_snippets_html(self, content_json, config_json):
        """Get the HTML snippets for all content items."""
        html_snippets = []

        num_items = len(content_json) # max
        if "itemsOnHomePage" in config_json:
            num_items = config_json["itemsOnHomePage"]
            print(f"Showing {num_items} snippets on the home page.")

        for i in range(num_items):
            # Get the most recent num_items items. Yes, really, this formula is weird.
            # Well, anyway, we reverse the snippets in tropical.py, so ... yeah.
            item = content_json[len(content_json) - num_items + i]
            item_html = self.get_snippet_html(item, config_json)
            html_snippets.append(item_html)
            
        return html_snippets

    # item is a dictionary of item attributes e.g. { "title": ..., "url": ...}
    # NB: keep in synch with search.html (JS rendering)
    def get_snippet_html(self, item, config_json):
        """Generate the actual HTML for a single snippet."""
        root_url = ""

        if "siteRootUrl" in config_json:
            root_url = config_json["siteRootUrl"]

        item_html = self._snippets_template
        title_html = "<a href='{}'>{}</a>".format(item["url"], item["title"])

        if "type" in item:
            type = item["type"]
            type_link = "{}/{}".format(root_url, type_page_html_generator.get_link_for(type))
            title_html += "<a href='{}'><img class='icon' src='{}/images/{}.png' title={} /></a>".format(type_link, root_url, type, type)

        item_html = item_html.replace("{title}", title_html)
        item_html = item_html.replace("{url}", "<a href='{}'>{}</a>".format(item["url"], item["url"]))

        tags_html = ""
        for tag in item["tags"]:
            # The space after tags is crucial, it allows line-breaking (tags go to the next line, not break half-way).
            tags_html += tag_html_generator.get_html_for_tag(tag, config_json)

        item_html = item_html.replace("{tags}", tags_html)

        item_html = item_html.replace("{blurb}", item["blurb"])
        return item_html

    # We embed this in a single-quoted script in JS, so replace all single-quotes with double-quotes. And minify, sort of.
    def get_snippet_template_for_javascript(self):
        # Match where we do tag normalization
        html = self._snippets_template.replace("'", '"').replace("  ", "").replace("\n", "").replace("\r", "")
        # window.snippet = html
        snippet_script = SCRIPT_WRAPPER_HTML.format("snippet", html)
        return snippet_script
