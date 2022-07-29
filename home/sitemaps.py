from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse
class StaticViewSitemap(Sitemap):
    def items(self):
        return ['home', 'maze', 'part_two']
    def location(self, item):
        return reverse(item)